#!/usr/bin/env bash
# Repository verification front door. Run every local test lane in dependency order.

set -euo pipefail

export NO_MKDOCS_2_WARNING=1

readonly REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "${REPO_ROOT}"


#============================================
run_step() {
	local label="$1"
	shift
	printf '\n=== %s ===\n' "${label}"
	"$@"
}


source "${REPO_ROOT}/source_me.sh"

run_step "Fast repository tests" \
	python3 -m pytest "${REPO_ROOT}/tests/"
run_step "Live Google Sheets export E2E, strict site build, and include parity" \
	python3 "${REPO_ROOT}/tests/e2e/e2e_include_parity.py"
run_step "Production rebuild and Playwright browser tests" \
	"${REPO_ROOT}/run_playwright_tests.sh" --build

printf '\n=== ALL TESTS PASSED ===\n'
