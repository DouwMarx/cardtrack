# Cloudflare setup

## systemcards.org (done 2026-08-31)

Live at https://systemcards.org and https://www.systemcards.org. Both are custom
domains on the `cardtrack` Pages project (proxied CNAMEs → `cardtrack-aar.pages.dev`,
edge HTTPS active); `cards.douwmarx.com` stays attached and serving, so old links keep
working. `site.base_url` is now `https://systemcards.org`. Daily deploys update all
three domains automatically (same Pages project).

**One optional manual step — the 301 from the old domain.** Automation couldn't create
it: the `cardtrack-deploy` API token lacks `Zone | Dynamic Redirect | Edit`. Both domains
serve today, so this is purely canonicalization. To add it (≈2 min, no token change):
Cloudflare dashboard → **douwmarx.com** → **Rules → Redirect Rules → Create rule** →
When incoming requests match **Hostname equals `cards.douwmarx.com`** → Then **Static/
Dynamic redirect**, type **301**, target `https://systemcards.org` with **Preserve path
and query string** enabled. (Or grant the token that permission and tell Claude to create
it via the Rulesets API — the exact call is in the session history.)

## Original move plan (for reference)

The site is domain-agnostic (all internal URLs relative), so the move was registrar +
DNS only; deploys kept going to the same Pages project throughout.

### Steps required from you (~10 minutes)

1. Buy the domain on Cloudflare Registrar (at-cost pricing, ~$11/yr for .org; the zone
   is created on your account automatically, no nameserver dance):
   - https://dash.cloudflare.com/?to=/:account/registrar/register
   - Search `systemcards.org` > Purchase. Enable auto-renew.
   - (Porkbun et al. are ~$3 cheaper the first year but then need a manual
     nameserver move to Cloudflare; not worth it.)
2. Extend the `cardtrack-deploy` API token so automation can finish the job:
   - https://dash.cloudflare.com/profile/api-tokens > `cardtrack-deploy` > Edit
   - Zone Resources: change to Include | Specific zone | **add `systemcards.org`**
     (keep `douwmarx.com` — it is needed for the old-domain redirect)
   - Permissions: keep `Account | Cloudflare Pages | Edit` and `Zone | DNS | Edit`;
     **add `Zone | Dynamic Redirect | Edit`** (powers the 301 from the old domain)
   - Save. The token value does not change, so `.env` needs no edit.
3. Tell Claude the domain is bought — everything below is automated from here.

### What happens after (automated, for reference)

- CNAME `systemcards.org` (apex, proxied) and `www` → `cardtrack.pages.dev` via DNS API
- Custom domains `systemcards.org` + `www.systemcards.org` attached to the Pages
  project (`wrangler`/API); HTTPS cert auto-issued
- Redirect Rule on the `douwmarx.com` zone: `cards.douwmarx.com/*` → 301
  `https://systemcards.org/$1` (the existing CNAME must stay proxied/orange-cloud
  for the rule to fire); old links and search results keep resolving
- `config/settings.yaml` `site.base_url` flipped to `https://systemcards.org`
- End-to-end check: new domain serves the site, old domain 301s with path preserved

## Original setup for cards.douwmarx.com

Your DNS is already on Cloudflare (chad/mimi nameservers), so this is a one-time, ~5 minute job. Everything else (project creation, deploys, CNAME, domain attach, HTTPS verification) is automated once the token exists.

## Steps required from you

1. Create an API token
   - Go to https://dash.cloudflare.com/profile/api-tokens
   - Create Token > Create Custom Token
   - Name: `cardtrack-deploy`
   - Permissions:
     - Account | Cloudflare Pages | Edit
     - Zone | DNS | Edit
   - Zone Resources: Include | Specific zone | douwmarx.com
   - Continue to summary > Create Token > copy the token

2. Find your Account ID
   - Open https://dash.cloudflare.com, click douwmarx.com
   - Account ID is in the right sidebar of the zone overview page

3. Add both to `~/.config/secrets.env`:
   ```
   CLOUDFLARE_API_TOKEN=<token>
   CLOUDFLARE_ACCOUNT_ID=<account id>
   ```

4. GitHub (for the public repo and the issues loop)
   - Confirm `gh auth status` works in a terminal (`! gh auth status` in a Claude session)
   - Tell Claude the repo name to create under your account (default suggestion: `cardtrack`)

## What happens after (automated, for reference)

- `wrangler pages project create cardtrack`
- `wrangler pages deploy site/` at the end of every daily run
- CNAME `cards` → `cardtrack.pages.dev` created via the DNS API
- Custom domain `cards.douwmarx.com` attached to the Pages project
- End-to-end check: https://cards.douwmarx.com serves the built site
