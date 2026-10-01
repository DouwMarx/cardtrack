# Production host

One small Debian 13 server (production: netcup VPS 500, Nuremberg: 2 cores, 4 GB RAM,
64 GB disk, about 7 EUR/month). Everything after ordering it is code run over SSH;
only the secrets file is filled in by hand.

| Piece | File | Does |
|---|---|---|
| Machine setup | `bootstrap.sh`, `versions.env` | packages, app user `cardtrack`, pinned `uv` and Claude Code, repo clone, key-only SSH |
| First contact | `provision.sh` | runs the bootstrap on a fresh server over SSH as root |
| Secrets + switch-on | `push-secrets.sh`, `prod.env.example` | writes `.env`, logs `gh` in, runs the canary, enables the timers |
| Moving production | `migrate-data.sh` | stops the old machine's timers, copies `data/raw` and `state/`, enables the new host |
| Pre-flight on the host | `check-host.sh` | every credential and tool, exercised without changing anything |
| Tests without a server | `test-bootstrap.sh`, `rehearse.sh` | see "Testing" below |

The pipeline only makes outbound connections; SSH (key-only) is the one open port.

## Set up a host

1. Order a Debian 13 server with 2 cores and 4 GB RAM. Any provider works; the
   steps below use only SSH. Keep the root password in your password manager: it is
   needed only for the provider's web console, the break-glass if SSH ever fails.
2. Put your SSH key on it and check the host's identity on first contact: the
   fingerprint `ssh` shows must match the one in the provider's welcome email.
   ```sh
   ssh-copy-id -i ~/.ssh/id_ed25519.pub root@<ip>     # asks for the root password once
   ssh root@<ip> true                                  # must not ask for a password
   ```
3. `./provision.sh <ip>` (about 5 minutes; disables password login).
4. `cp prod.env.example prod.env` and fill it in:
   - `CLAUDE_CODE_OAUTH_TOKEN`: `claude setup-token`, approved in the browser as the
     pipeline's own Claude account; `CLAUDE_TOKEN_CREATED` = that day.
   - `GH_TOKEN`: fine-grained PAT, this repository only, Contents and Issues read/write.
   - Cloudflare, OpenRouter and R2 values as in the root `env.example`.
5. New deployment: `./push-secrets.sh <ip>`. It ends with the canary (`"failing": []`
   means Claude answers with the pipeline's credentials) and enables the timers.
6. Moving an existing deployment instead: `./push-secrets.sh <ip> --no-enable`, then
   `./check-host.sh <ip>` (every line must say ok), then on the old machine
   `./migrate-data.sh <ip>`. It stops the old timers, copies
   `data/raw` and `state/`, and only then enables the new host's timers, so two
   machines never publish the same day.

## Testing

From cheapest to most complete. None of these touch production.

| Layer | Command | Needs | Proves |
|---|---|---|---|
| Unit + integration | `uv run poe test` | uv; bwrap, pandoc, rclone for some tests | code paths, the real sandbox, a real S3 endpoint (`rclone serve s3`), real git for deploys; also runs in CI on every push |
| Clean-machine build | `uv run poe test-bootstrap` | docker | `bootstrap.sh` on a fresh Debian 13, then the full test suite and a report build there |
| Dress rehearsal | `uv run poe rehearse` | docker, `infra/prod.env`, your SSH key | the whole host path on a throwaway Debian 13 "server" (systemd + sshd, reached over SSH): `provision.sh`, `push-secrets.sh` with a dev-role copy of the secrets, the timers, one full daily run under systemd. Costs one agent run on the pipeline's subscription. Clones the default branch from GitHub, so push first. |
| Host pre-flight | `infra/check-host.sh <host>` | SSH to a provisioned host with secrets | on the real host, without changing anything: role, file permissions, pinned versions, the sandbox, git push auth (dry run), gh, a Claude call on the pipeline account, wrangler against the Pages project, OpenRouter, both R2 buckets, the report toolchain. It caught wrangler needing Node 22 on Debian 13, which the rehearsal cannot see because dev never deploys. |
| Live smoke test | `uv run poe smoke` | curl | the public production surface: site pages, the Analysis page and its disclaimer, the archive redirect and sandbox headers, and one archived original against its sha256 in the manifest |

The rehearsal's first run found that the sandbox hid `~/.local/bin/claude` on Debian
(agent exit 127), a failure the NixOS laptop could never show. Run it before changing
`bootstrap.sh`, `provision.sh`, `push-secrets.sh`, the systemd units or the sandbox.

## Operate

- Deploy code: push to `main`. The host pulls before the next daily run and moves only
  if the test suite passes there; otherwise a `pipeline-alert: deploy-rejected` issue opens.
- Alerts arrive as GitHub issues (`pipeline-alert: *`) and close themselves; see the
  root README, "Alerts".
- Logs: `ssh cardtrack@<ip>`, then `ls ~/cardtrack/logs/`, or
  `journalctl --user -u cardtrack -u cardtrack-canary -u cardtrack-report`.
- Run now: `systemctl --user start cardtrack` (or `cardtrack-report`).
- Troubleshoot with Claude Code on the host (uses the pipeline's subscription):
  `cd ~/cardtrack && CLAUDE_CODE_OAUTH_TOKEN="$(. scripts/lib.sh; envget CLAUDE_CODE_OAUTH_TOKEN .)" claude`

### Rotate the Claude token

Run `claude setup-token` as the pipeline's account, update `CLAUDE_CODE_OAUTH_TOKEN` and
`CLAUDE_TOKEN_CREATED` in `prod.env`, and re-run `./push-secrets.sh <ip>`. Revoke the
old token at claude.ai/settings/claude-code. The `claude-token-expiring` issue closes on
the next run.

### Upgrade pinned tools

Bump `versions.env`, run `poe rehearse`, push, let the host pull it, then as root:
`ssh root@<ip> bash ~cardtrack/cardtrack/infra/bootstrap.sh <repo-url>` (idempotent).
Not pinned: Debian packages (security updates install automatically) and `npx`
pagefind (wrangler is pinned in settings.yaml).
