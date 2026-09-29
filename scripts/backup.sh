#!/usr/bin/env bash
# Off-site copies of the raw archive (data/raw is gitignored, so git holds no copy
# of the original bytes), via rclone's S3 backend on Cloudflare R2. Configured
# purely from .env, so no rclone.conf exists on disk. No-op when R2 is not set.
#
#   R2_BUCKET         private backup: every original, add-only (never deletes)
#   R2_PUBLIC_BUCKET  optional public archive (settings archive.public_base_url):
#                     originals minus config/withheld.txt, plus manifest.json,
#                     urls.txt, cardtrack-dataset.tar.gz. Withheld files are
#                     deleted here only, never from the private bucket.
#
# Restore: rclone copy ":s3:$R2_BUCKET/raw" data/raw   (same RCLONE_S3_* env)
set -euo pipefail
ROOT="${1:-${CARDTRACK_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}}"
SCRIPT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$SCRIPT_ROOT/scripts/lib.sh"
PRIVATE="$(envget R2_BUCKET "$ROOT")"
PUBLIC="$(envget R2_PUBLIC_BUCKET "$ROOT")"
[ -n "$PRIVATE" ] || { echo "[backup] R2 not configured; skipping"; exit 0; }
command -v rclone >/dev/null || { echo "[backup] rclone missing"; exit 1; }
STAGE="$(mktemp -d)"; trap 'rm -rf "$STAGE"' EXIT
(
  export RCLONE_S3_PROVIDER="${R2_PROVIDER:-$(envget R2_PROVIDER "$ROOT")}"
  RCLONE_S3_PROVIDER="${RCLONE_S3_PROVIDER:-Cloudflare}"
  RCLONE_S3_ACCESS_KEY_ID="$(envget R2_ACCESS_KEY_ID "$ROOT")"; export RCLONE_S3_ACCESS_KEY_ID
  RCLONE_S3_SECRET_ACCESS_KEY="$(envget R2_SECRET_ACCESS_KEY "$ROOT")"; export RCLONE_S3_SECRET_ACCESS_KEY
  RCLONE_S3_ENDPOINT="$(envget R2_ENDPOINT "$ROOT")"; export RCLONE_S3_ENDPOINT
  RC=(rclone --transfers 8 --s3-no-check-bucket)
  # copy, not sync: a local deletion must never propagate to the only other copy
  "${RC[@]}" copy --immutable "$ROOT/data/raw" ":s3:$PRIVATE/raw"
  echo "[backup] data/raw copied to private bucket $PRIVATE"
  if [ -n "$PUBLIC" ]; then
    "$ROOT/.venv/bin/python" "$SCRIPT_ROOT/scripts/build_dataset.py" --root "$ROOT" --out "$STAGE" >/dev/null
    "${RC[@]}" copy --immutable --exclude-from "$STAGE/withheld.txt" "$ROOT/data/raw" ":s3:$PUBLIC/raw"
    while IFS= read -r f; do
      [ -n "$f" ] && "${RC[@]}" deletefile ":s3:$PUBLIC/raw/$f" 2>/dev/null || true
    done < "$STAGE/withheld.txt"
    for f in manifest.json urls.txt cardtrack-dataset.tar.gz; do
      "${RC[@]}" copyto "$STAGE/$f" ":s3:$PUBLIC/$f"
    done
    echo "[backup] public archive updated in $PUBLIC ($(wc -l < "$STAGE/urls.txt") originals)"
  fi
)
mkdir -p "$ROOT/state"
date -u +%FT%TZ > "$ROOT/state/.backup_last_ok"
