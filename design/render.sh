#!/usr/bin/env bash
# Render banner.html to a print-ready PDF.
# Chrome headless writes the PDF but does not always exit, so poll the output
# file and stop the browser once its size has settled.
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE/banner.pdf}"
SRC="${2:-$HERE/banner.html}"
PROFILE="$(mktemp -d)"

rm -f "$OUT"

google-chrome \
  --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --user-data-dir="$PROFILE" \
  --allow-file-access-from-files \
  --no-pdf-header-footer --no-first-run \
  --disable-sync --disable-background-networking \
  --disable-component-update --disable-extensions --disable-default-apps \
  --virtual-time-budget=12000 \
  --print-to-pdf="$OUT" "file://$SRC" >/dev/null 2>&1 &
PID=$!

prev=-1
stable=0
for _ in $(seq 1 240); do
  sleep 2
  size=$(stat -c%s "$OUT" 2>/dev/null || echo 0)
  if [ "$size" -gt 0 ] && [ "$size" -eq "$prev" ]; then
    stable=$((stable + 1))
    [ "$stable" -ge 2 ] && break
  else
    stable=0
  fi
  prev=$size
  kill -0 "$PID" 2>/dev/null || break
done

kill "$PID" 2>/dev/null
sleep 1
kill -9 "$PID" 2>/dev/null
rm -rf "$PROFILE"

if [ -s "$OUT" ]; then
  echo "wrote $OUT ($(stat -c%s "$OUT") bytes)"
  pdfinfo "$OUT" | grep -E "Pages|Page size"
else
  echo "render failed"
  exit 1
fi
