#!/usr/bin/env bash

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

source source_me.sh
python3 pipeline/build_site.py
node tests/playwright/capture_table_review.mjs
