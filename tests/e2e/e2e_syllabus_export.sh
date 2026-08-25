#!/usr/bin/env bash

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
source source_me.sh

mkdir -p site_docs/downloads
stale_docx="site_docs/downloads/STALE_SYLLABUS.docx"
stale_pdf="site_docs/downloads/STALE_SYLLABUS.pdf"
printf '%s\n' 'obsolete generated artifact' > "$stale_docx"
printf '%s\n' 'obsolete generated artifact' > "$stale_pdf"

python3 pipeline/build_syllabi.py "$@"

if [[ -e "$stale_docx" || -e "$stale_pdf" ]]; then
	echo "ERROR: stale generated downloads survived the rebuild" >&2
	exit 1
fi

python3 -m mkdocs build --strict

for syllabus_pdf in site_docs/downloads/*.pdf; do
	if ! pdfinfo "$syllabus_pdf" | rg '^Tagged:[[:space:]]+yes$' >/dev/null; then
		printf 'Accessibility advisory: PDF is not tagged: %s\n' "$syllabus_pdf" >&2
	fi
done

if rg -n -i \
	--glob '*.html' \
	--glob 'search_index.json' \
	'zoom\.us/j/|\bpwd=|\b(passcode|password)[[:space:]]*[:=]|discord\.(gg|com/invite)/' \
	site; then
	echo "ERROR: prohibited credential pattern found in built site" >&2
	exit 1
fi

echo "PASS: complete syllabus export and strict site build"
