#!/usr/bin/env bash
# Off-site copy of the raw archive (data/raw is gitignored, so git holds no copy of
# the original bytes). Cloudflare R2 through rclone's S3 backend, configured purely
# from .env (R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_BUCKET), so no
# rclone.conf exists on disk. No-op when R2 is not configured.
# Restore:  rclone copy :s3,provider=Cloudflare,endpoint=$R2_ENDPOINT:$R2_BUCKET/raw data/raw
set -euo pipefail
ROOT="${1:-${CARDTRACK_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}}"
. "$(dirname "$0")/lib.sh"
[ -n "$(envget R2_BUCKET "$ROOT")" ] || { echo "[backup] R2 not configured; skipping"; exit 0; }
command -v rclone >/dev/null || { echo "[backup] rclone missing"; exit 1; }
(
  export RCLONE_S3_PROVIDER=Cloudflare
  RCLONE_S3_ACCESS_KEY_ID="$(envget R2_ACCESS_KEY_ID "$ROOT")"; export RCLONE_S3_ACCESS_KEY_ID
  RCLONE_S3_SECRET_ACCESS_KEY="$(envget R2_SECRET_ACCESS_KEY "$ROOT")"; export RCLONE_S3_SECRET_ACCESS_KEY
  RCLONE_S3_ENDPOINT="$(envget R2_ENDPOINT "$ROOT")"; export RCLONE_S3_ENDPOINT
  # copy, not sync: a local deletion must never propagate to the only other copy
  rclone copy --immutable --transfers 4 "$ROOT/data/raw" ":s3:$(envget R2_BUCKET "$ROOT")/raw"
)
date -u +%FT%TZ > "$ROOT/state/.backup_last_ok"
echo "[backup] data/raw copied to R2"
