#!/usr/bin/env python3
"""Refresh the configured calendar snapshots."""

# Standard Library
import pathlib
import sys


PIPELINE_PATH = pathlib.Path(__file__).resolve().parents[1] / "pipeline"
sys.path.insert(0, str(PIPELINE_PATH))

# local repo modules
import build_lib.calendar_sync


if __name__ == "__main__":
	build_lib.calendar_sync.main()
