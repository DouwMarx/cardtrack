#!/usr/bin/env bash
# Smoke test of the live public surface (no secrets, read-only):
#   site pages, the Analysis page and its disclaimer, the archive redirect and
#   sandbox headers, and one archived original checked against the manifest.
#   scripts/smoke_public.sh [site-url] [data-url]
set -uo pipefail
SITE="${1:-https://systemcards.org}"
DATA="${2:-https://data.systemcards.org}"
FAIL=0
check() {  # check <description> <command...>
  local d="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "ok    $d"; else echo "FAIL  $d"; FAIL=1; fi
}
body() { curl -fsSL --max-time 30 "$1"; }

check "site index loads"                 body "$SITE/"
check "About page has the archive section" bash -c "curl -fsSL '$SITE/about' | grep -q 'id=\"archive\"'"
check "Analysis page names model + skill" bash -c "curl -fsSL '$SITE/analysis' | grep -q 'AI-generated report' && curl -fsSL '$SITE/analysis' | grep -q 'SKILL.md'"
check "Analysis page offers no PDF"      bash -c "p=\$(curl -fsSL '$SITE/analysis') && ! printf '%s' \"\$p\" | grep -qi 'report\.pdf\|PDF version'"
check "Analysis page forbids scripts (CSP)" bash -c "curl -fsSL '$SITE/analysis' | grep -q \"script-src 'none'\""
check "archive root redirects to About"  bash -c "curl -fsI --max-time 30 '$DATA/' | grep -qi '^location: .*about#archive'"

MAN="$(mktemp)"; trap 'rm -f "$MAN" "$MAN.f"' EXIT
check "manifest.json downloads"           bash -c "curl -fsSL --max-time 60 '$DATA/manifest.json' -o '$MAN'"
check "dataset tarball is served"         bash -c "curl -fsI --max-time 30 '$DATA/cardtrack-dataset.tar.gz' | grep -q '^HTTP/[0-9.]* 200'"

# one archived web page: sandbox headers; one PDF: no sandbox, hash matches manifest
read -r HTML_URL < <(python3 -c "
import json,sys; m=json.load(open('$MAN'))
print(next(v['url'] for v in m['versions'] if v['url'] and v['url'].endswith('.html')))" 2>/dev/null)
read -r PDF_URL PDF_SHA < <(python3 -c "
import json,sys; m=json.load(open('$MAN'))
v=next(v for v in m['versions'] if v['url'] and v['url'].endswith('.pdf')); print(v['url'], v['sha256'])" 2>/dev/null)
check "archived HTML is sandboxed"        bash -c "curl -fsI --max-time 30 '${HTML_URL:-x}' | grep -qi '^content-security-policy: sandbox'"
check "archived PDF is not sandboxed"     bash -c "h=\$(curl -fsI --max-time 30 '${PDF_URL:-x}') && ! printf '%s' \"\$h\" | grep -qi '^content-security-policy'"
check "archived PDF matches its sha256"   bash -c "curl -fsSL --max-time 120 '${PDF_URL:-x}' -o '$MAN.f' && [ \"\$(sha256sum '$MAN.f' | cut -c1-64)\" = '${PDF_SHA:-x}' ]"
exit "$FAIL"
