#!/usr/bin/env bash

set -euo pipefail

export NO_MKDOCS_2_WARNING=1

cd "$(git rev-parse --show-toplevel)"

if [[ "${1:-}" == "--build" ]]; then
	source source_me.sh
	python3 pipeline/build_site.py
fi

npm run test:playwright
