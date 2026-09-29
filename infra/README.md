# Production host

One small Debian 13 VM at Hetzner, created and configured from this directory.
Everything is code except the secrets, which you deliver in one command.

| Piece | File | Does |
|---|---|---|
| Infrastructure | `main.tf`, `variables.tf` | server, SSH key, firewall (only key-only SSH inbound) |
| First boot | `cloud-init.yaml.tftpl` | joins the tailnet (optional), runs the bootstrap |
| Machine setup | `bootstrap.sh`, `versions.env` | packages, app user, pinned `uv` and `claude`, clone, `uv sync` |
| Any other provider | `provision.sh` | the cloud-init steps over SSH, for a Debian 13 box you ordered by hand |
| Secrets + switch-on | `push-secrets.sh`, `prod.env.example` | writes `.env`, logs `gh` in, enables the timers |
| Moving production | `migrate-data.sh` | stops the old host, copies `data/raw`, hands over |
| Proof without a VM | `test-bootstrap.sh` | runs the bootstrap + test suite + report build in a Debian 13 container |

Sizing: `cx23` (2 vCPU x86, 4 GB, 40 GB, about 6 EUR/month with IPv4). The pipeline
uses about 3 GB of disk and runs one job at a time. IPv4 stays on because github.com
has no IPv6 address.

## Create a host

You need: [Terraform](https://developer.hashicorp.com/terraform/install) (or OpenTofu),
a Hetzner Cloud project, and an SSH key. The host clones `repo_url` and runs
`infra/bootstrap.sh` from its default branch, so that branch must already contain `infra/`.

1. Hetzner console: create a project, then Security > API tokens > Generate (Read & Write).
2. SSH is key-only (the bootstrap disables password login) and open on port 22, the only
   inbound port. To restrict it, set `admin_cidrs`. Optional: put the host on a Tailscale
   tailnet instead and close port 22 entirely; see "Optional: Tailscale" below.
3. In `infra/`: `cp terraform.tfvars.example terraform.tfvars`, fill it in, then:
   ```sh
   cd infra
   terraform init
   terraform apply
   ```
   Or let `./hetzner-try.sh` pick: it asks the Hetzner API which budget type
   (CX23, then ARM CAX11) is orderable in which location, applies only then, and
   creates nothing (exit 3) when none is, so you can fall back to "Other providers". First boot takes about 10 minutes (TeX Live). Progress:
   `ssh root@<host> tail -F /var/log/cardtrack-bootstrap.log`. With Tailscale, remove an old
   node of the same name in the admin console before re-creating a host.
4. `cp prod.env.example prod.env` and fill it in:
   - `CLAUDE_CODE_OAUTH_TOKEN`: run `claude setup-token` and approve in the browser as
     the pipeline's own Claude account; set `CLAUDE_TOKEN_CREATED` to today.
   - `GH_TOKEN`: fine-grained PAT, this repo only, Contents and Issues read/write.
   - Cloudflare and OpenRouter keys as in the root `env.example`.
5. New deployment: `./push-secrets.sh <host>`. It runs the canary (`ok` means Claude
   answers with the pipeline's credentials) and enables the timers.
6. Moving an existing deployment instead: `./push-secrets.sh <host> --no-enable`, then
   on the old machine `./migrate-data.sh <host>`. It stops the old timers, copies
   `data/raw`, and only then enables the new host's timers, so two machines never
   publish the same day.

## Other providers (netcup, OVH, bare metal)

Only the ordering step differs. `bootstrap.sh` is provider-neutral; `main.tf` is the
Hetzner-specific part, used when that provider has stock (its cost-optimized CX/CAX
line was sold out for much of September 2026).

1. Order a Debian 13 server with 2 cores and 4 GB RAM in the provider's web shop, with
   your SSH key for root (netcup: VPS 500, Nuremberg). netcup has no ordering API; its
   Terraform providers are community-maintained and manage existing servers only.
2. `./provision.sh <public-ip>` (optionally `--tailscale-key-file <file> --lockdown`,
   see below).
3. Continue with step 4 above, with the public IP as `<host>`.

## Optional: Tailscale

Joining a tailnet lets the host close port 22 to the internet. It costs a policy edit
that must keep the host from reaching your other devices; check it against your
existing policy before saving, since replacing the default allow-all rule changes
what your own devices can reach:

```json
"tagOwners": { "tag:cardtrack": ["autogroup:admin"] },
"grants": [
  { "src": ["autogroup:member"], "dst": ["autogroup:member"], "ip": ["*"] },
  { "src": ["autogroup:admin"],  "dst": ["tag:cardtrack"],    "ip": ["*"] }
],
"ssh": [
  { "action": "accept", "src": ["autogroup:admin"], "dst": ["tag:cardtrack"],
    "users": ["root", "cardtrack"] }
]
```

Then generate a one-off, pre-approved auth key tagged `tag:cardtrack` and pass it as
`tailscale_auth_key` (Terraform) or `--tailscale-key-file` (provision.sh, where
`--lockdown` then drops all public inbound traffic).

## Operate

- Deploy code: push to `main`. The host pulls before the next daily run and moves only
  if the test suite passes there; otherwise a `pipeline-alert: deploy-rejected` issue opens.
- Alerts arrive as GitHub issues (`pipeline-alert: *`) and close themselves; see the
  root README, "Alerts".
- Logs: `ssh cardtrack@<host>`, then `ls ~/cardtrack/logs/`, or
  `journalctl --user -u cardtrack -u cardtrack-canary -u cardtrack-report`.
- Run now: `systemctl --user start cardtrack` (or `cardtrack-report`).

### Rotate the Claude token

Run `claude setup-token` as the pipeline's account, update `CLAUDE_CODE_OAUTH_TOKEN` and
`CLAUDE_TOKEN_CREATED` in `prod.env`, and re-run `./push-secrets.sh <host>`. Revoke the
old token at claude.ai/settings/claude-code. The `claude-token-expiring` issue closes on
the next run.

### Upgrade pinned tools

Bump `versions.env`, run the daily pipeline once on a dev checkout with the new
versions, push, let the host pull it, then as root on the host:
`ssh root@<host> bash ~cardtrack/cardtrack/infra/bootstrap.sh <repo-url>` (idempotent).
Not pinned: Debian packages (security updates install automatically), the Tailscale
installer, and `npx` wrangler/pagefind.
