#!/usr/bin/env bash

set -euo pipefail

export NO_MKDOCS_2_WARNING=1

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly repo_dir
cd "$repo_dir"

source source_me.sh

readonly PREVIEW_SECONDS=300
server_pid=""

stop_server() {
	if [[ -z "$server_pid" ]]; then
		return 0
	fi

	if kill -0 "$server_pid" 2>/dev/null; then
		kill "$server_pid" 2>/dev/null || true
	fi
	wait "$server_pid" 2>/dev/null || true
	server_pid=""
}

trap stop_server EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# ASVS 16.5.3: do not start a preview with a stale important-dates table.
python3 pipeline/sync_important_dates.py
printf 'Starting the syllabus preview; it will stop automatically after five minutes.\n'
python3 -m mkdocs serve --open &
server_pid=$!
deadline=$((SECONDS + PREVIEW_SECONDS))

# Polling keeps the timeout portable on macOS, where GNU timeout is not included.
while kill -0 "$server_pid" 2>/dev/null; do
	if ((SECONDS >= deadline)); then
		printf 'Five-minute preview limit reached; stopping MkDocs.\n'
		stop_server
		exit 0
	fi
	sleep 1
done

# Preserve an early MkDocs failure so callers can detect startup errors.
if wait "$server_pid"; then
	server_status=0
else
	server_status=$?
fi
server_pid=""
exit "$server_status"
