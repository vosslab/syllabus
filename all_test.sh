#!/usr/bin/env bash
# Repository verification front door. Run every local test lane in dependency order.

set -euo pipefail

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
run_step "Live Google Sheets export E2E and strict site build" \
	bash "${REPO_ROOT}/tests/e2e/e2e_syllabus_export.sh"
run_step "Production rebuild and Playwright browser tests" \
	"${REPO_ROOT}/run_playwright_tests.sh" --build

printf '\n=== ALL TESTS PASSED ===\n'
