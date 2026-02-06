#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 BASEDIR BASENAME IDENTIFIER [DEPTH] [MANUSCRIPT_DIR] [PROTECTION_FILE] [NUM_PROTECTED] [PROTECTION_METRIC]"
  exit 1
fi

base_dir="$1"
base_name="$2"
identifier="$3"
depth="${4:-6}"
manuscript_dir="${5:-}"
protection_file="${6:-}"
num_protected="${7:-}"
protection_metric="${8:-}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
data_dir="${base_dir%/}/${base_name}/"
output_dir="${data_dir}"

if [ -n "${manuscript_dir}" ]; then
  output_dir="${manuscript_dir%/}"
fi

"${script_dir}/200_compute_importance.py" \
  "${data_dir}" \
  "${identifier}" \
  "${depth}" \
  --out-dir "${output_dir}"

if [ "${protection_file}" = "centrality" ]; then
  "${script_dir}/200_compute_importance-centrality.py" \
    "${data_dir}" \
    "${identifier}"
  protection_file="centrality_${identifier}.csv"
fi

if [ -n "${protection_file}" ] && [ -n "${num_protected}" ] && [ -n "${protection_metric}" ]; then
  "${script_dir}/201_compute_importance-protected.py" \
    "${data_dir}" \
    "${identifier}" \
    "${protection_file}" \
    "${depth}" \
    "${num_protected}" \
    "${protection_metric}" \
    --out-dir "${output_dir}"
fi
