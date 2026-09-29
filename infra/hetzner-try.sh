#!/usr/bin/env bash
# Create the host on Hetzner if any budget server type is orderable right now.
# Asks the API which (type, location) pairs have stock, in preference order, and
# runs `terraform apply` for the first one. Creates nothing when none is in stock
# (exit 3): fall back to a manually ordered server + infra/provision.sh.
#   infra/hetzner-try.sh            (reads hcloud_token from infra/terraform.tfvars)
set -euo pipefail
cd "$(dirname "$0")"
TF="${TF:-terraform}"
PREFS="${PREFS:-cx23:fsn1 cx23:nbg1 cx23:hel1 cax11:fsn1 cax11:nbg1 cax11:hel1}"
TOKEN="$(sed -nE 's/^[[:space:]]*hcloud_token[[:space:]]*=[[:space:]]*"(.*)".*/\1/p' terraform.tfvars)"
[ -n "$TOKEN" ] || { echo "hcloud_token is empty in infra/terraform.tfvars"; exit 1; }

PICK="$(HCLOUD_TOKEN="$TOKEN" PREFS="$PREFS" python3 - <<'PY'
import json, os, urllib.request
def get(path):
    req = urllib.request.Request("https://api.hetzner.cloud/v1/" + path,
                                 headers={"Authorization": "Bearer " + os.environ["HCLOUD_TOKEN"]})
    return json.load(urllib.request.urlopen(req, timeout=30))
types = {t["name"]: t["id"] for t in get("server_types?per_page=50")["server_types"]}
dcs = get("datacenters")["datacenters"]
for pref in os.environ["PREFS"].split():
    name, loc = pref.split(":")
    if any(dc["location"]["name"] == loc and types.get(name) in dc["server_types"]["available"]
           for dc in dcs):
        print(name, loc)
        break
PY
)" || { echo "Hetzner API call failed: check hcloud_token (Read & Write, right project)"; exit 1; }
if [ -z "$PICK" ]; then
  echo "No budget Hetzner type is orderable now ($PREFS). Nothing was created."
  echo "Fallback: order a Debian 13 server by hand, then infra/provision.sh (see README)."
  exit 3
fi
read -r TYPE LOC <<< "$PICK"
echo "In stock: $TYPE in $LOC. Creating."
"$TF" init -input=false >/dev/null
if ! "$TF" apply -input=false -auto-approve -var "server_type=$TYPE" -var "location=$LOC"; then
  echo "Hetzner refused the order (stock gone, or a new-account limit). Removing partial resources."
  "$TF" destroy -input=false -auto-approve -var "server_type=$TYPE" -var "location=$LOC" >/dev/null || true
  exit 3
fi
