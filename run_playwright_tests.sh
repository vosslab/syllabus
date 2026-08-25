#!/usr/bin/env bash

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if [[ "${1:-}" == "--build" ]]; then
	source source_me.sh
	python3 pipeline/build_site.py
fi

npm run test:playwright
