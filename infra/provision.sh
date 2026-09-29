#!/usr/bin/env bash
# Provision ANY fresh Debian 13 server you can SSH into as root: the path for
# providers without an ordering API (netcup, OVH, bare metal). Does over SSH what
# cloud-init does on Hetzner: optional Tailscale join, clone, infra/bootstrap.sh,
# and SSH access for the app user.
#
#   infra/provision.sh <host> [--tailscale-key-file F] [--lockdown] [--repo-url URL]
#
#   --tailscale-key-file  file holding a one-off tagged auth key (sent over stdin,
#                         never in argv or shell history)
#   --lockdown            after Tailscale is up: drop all inbound traffic on the
#                         public interface (keeps loopback, established, tailnet,
#                         and Tailscale's UDP 41641). Break-glass: the provider's
#                         web console. Requires --tailscale-key-file.
# Then continue with infra/push-secrets.sh <tailnet-name or IP>.
set -euo pipefail
HOST="${1:?usage: provision.sh <host> [--tailscale-key-file F] [--lockdown] [--repo-url URL]}"; shift
REPO_URL="https://github.com/DouwMarx/cardtrack.git"; TS_KEY_FILE=""; LOCKDOWN=0; NAME=cardtrack
while [ $# -gt 0 ]; do
  case "$1" in
    --tailscale-key-file) TS_KEY_FILE="$2"; shift 2 ;;
    --lockdown) LOCKDOWN=1; shift ;;
    --repo-url) REPO_URL="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    *) echo "unknown option $1"; exit 2 ;;
  esac
done
[ "$LOCKDOWN" = 1 ] && [ -z "$TS_KEY_FILE" ] && { echo "--lockdown needs --tailscale-key-file"; exit 2; }
SSH=(ssh -o StrictHostKeyChecking=accept-new "root@$HOST")

"${SSH[@]}" "grep -q 'VERSION_ID=\"13\"' /etc/os-release" \
  || { echo "host is not Debian 13; reinstall it with Debian 13 first"; exit 1; }

if [ -n "$TS_KEY_FILE" ]; then
  "${SSH[@]}" "command -v tailscale >/dev/null || curl -fsSL https://tailscale.com/install.sh | sh"
  "${SSH[@]}" "tailscale up --auth-key=\"\$(cat)\" --ssh --hostname='$NAME' --advertise-tags=tag:cardtrack" < "$TS_KEY_FILE"
fi

"${SSH[@]}" bash -s -- "$REPO_URL" <<'REMOTE'
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -q && apt-get install -y -q git ca-certificates curl >/dev/null
rm -rf /opt/cardtrack-bootstrap
git clone -q "$1" /opt/cardtrack-bootstrap
bash /opt/cardtrack-bootstrap/infra/bootstrap.sh "$1" cardtrack
# same keys as root, so `ssh cardtrack@host` works for push-secrets/migrate-data
install -d -m 700 -o cardtrack -g cardtrack /home/cardtrack/.ssh
install -m 600 -o cardtrack -g cardtrack /root/.ssh/authorized_keys /home/cardtrack/.ssh/authorized_keys
REMOTE

if [ "$LOCKDOWN" = 1 ]; then
  "${SSH[@]}" bash -s <<'REMOTE'
set -euo pipefail
apt-get install -y -q nftables >/dev/null
cat > /etc/nftables.conf <<'NFT'
#!/usr/sbin/nft -f
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    iif lo accept
    ct state established,related accept
    iifname "tailscale0" accept
    udp dport 41641 accept
    meta l4proto { icmp, ipv6-icmp } accept
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output priority 0; policy accept; }
}
NFT
nft -c -f /etc/nftables.conf
systemctl enable --now nftables >/dev/null
nft -f /etc/nftables.conf
echo "public inbound closed; reach the host over the tailnet"
REMOTE
fi
echo "provisioned; next: infra/push-secrets.sh <host>"
