#!/usr/bin/env bash
# Dress rehearsal of the whole production path on a throwaway local "server":
# a Debian 13 container running systemd and sshd, reached over SSH like a VPS.
#
#   infra/rehearse.sh [--keep]
#
# Runs, against that container, exactly what a real host gets:
#   1. infra/provision.sh <ip>          (bootstrap: packages, user, pinned tools, clone)
#   2. infra/push-secrets.sh --no-enable  with a COPY of infra/prod.env whose
#      CARDTRACK_ROLE is dev, so nothing is committed, pushed, deployed or filed
#   3. scripts/install_units.sh         (timers, as the app user's systemd)
#   4. systemctl --user start cardtrack  (a full daily run under systemd: monitor,
#      sandboxed agent on the pipeline's Claude account, site build)
# then prints the result and removes the container (--keep leaves it running).
#
# Needs: docker, your SSH key (~/.ssh/id_ed25519.pub), infra/prod.env. The host
# clones the repo's default branch from GitHub, so push what you want to test.
# Cost: one agent run on the pipeline's subscription (about 15 minutes).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KEEP=0; [ "${1:-}" = "--keep" ] && KEEP=1
NAME=cardtrack-rehearsal
PUBKEY="${REHEARSAL_PUBKEY:-$HOME/.ssh/id_ed25519.pub}"
[ -f "$HERE/prod.env" ] || { echo "missing infra/prod.env"; exit 1; }
[ -f "$PUBKEY" ] || { echo "missing $PUBKEY"; exit 1; }

WORK="$(mktemp -d)"
cleanup() {
  rm -rf "$WORK"
  if [ "$KEEP" = 0 ]; then
    docker rm -f "$NAME" >/dev/null 2>&1 || true
    [ -n "${IP:-}" ] && ssh-keygen -R "$IP" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

cat > "$WORK/Dockerfile" <<'EOF'
FROM debian:trixie
RUN apt-get update -q && DEBIAN_FRONTEND=noninteractive apt-get install -y -q \
      systemd systemd-sysv openssh-server dbus-user-session curl ca-certificates git >/dev/null \
 && mkdir -p /root/.ssh && chmod 700 /root/.ssh && systemctl enable ssh
STOPSIGNAL SIGRTMIN+3
CMD ["/sbin/init"]
EOF
docker build -q -t "$NAME" "$WORK" >/dev/null
docker rm -f "$NAME" >/dev/null 2>&1 || true
# systemd as PID 1 needs a writable cgroup tree and tmpfs /run
docker run -d --name "$NAME" --privileged --cgroupns=host \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw --tmpfs /run --tmpfs /run/lock "$NAME" >/dev/null
docker cp "$PUBKEY" "$NAME:/root/.ssh/authorized_keys"
docker exec "$NAME" bash -c 'chown root: /root/.ssh/authorized_keys; chmod 600 /root/.ssh/authorized_keys'
IP="$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$NAME")"
ssh-keygen -R "$IP" >/dev/null 2>&1 || true
for _ in $(seq 30); do
  ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=3 "root@$IP" true 2>/dev/null && break
  sleep 1
done
echo "== rehearsal host $IP (Debian $(ssh "root@$IP" cat /etc/debian_version))"

echo "== 1. provision"
"$HERE/provision.sh" "$IP" > "$WORK/provision.log" 2>&1 \
  || { tail -20 "$WORK/provision.log"; exit 1; }
echo "   ok"

echo "== 2. push secrets (dev-role copy)"
sed 's/^CARDTRACK_ROLE=.*/CARDTRACK_ROLE=dev/' "$HERE/prod.env" > "$WORK/rehearsal.env"
chmod 600 "$WORK/rehearsal.env"
CARDTRACK_PROD_ENV="$WORK/rehearsal.env" "$HERE/push-secrets.sh" "$IP" --no-enable 2>&1 \
  | grep -E '"failing"|Logged in|error|Error' || true

echo "== 3+4. timers, then a full daily run under systemd"
ssh -o BatchMode=yes "cardtrack@$IP" bash -s <<'REMOTE'
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
cd ~/cardtrack
scripts/install_units.sh >/dev/null && echo "   timers: $(systemctl --user list-timers 'cardtrack*' --no-legend | wc -l) installed"
systemctl --user start cardtrack.service || true
echo "   unit: $(systemctl --user show cardtrack.service -p Result --value), exit $(systemctl --user show cardtrack.service -p ExecMainStatus --value)"
L="$(ls -t logs/run-*.log | head -1)"
grep -E '^== |FAILED|agent exited|"failing"' "$L" | sed 's/^/   /'
REMOTE
[ "$KEEP" = 1 ] && echo "kept: ssh cardtrack@$IP   (remove: docker rm -f $NAME)"
