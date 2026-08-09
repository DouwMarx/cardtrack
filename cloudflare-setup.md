# Cloudflare setup for cards.douwmarx.com

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
