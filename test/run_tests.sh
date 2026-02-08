#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
color() { printf "\033[%sm%s\033[0m\n" "$1" "$2"; }
step() { color "1;34" "[$1/2] $2"; }

step 1 "Running contagion unit tests"
PYTHONPATH="${ROOT_DIR}/.." python3 -m unittest discover -v -s "${ROOT_DIR}" -p "test_*.py"

step 2 "Done"
