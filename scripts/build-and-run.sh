#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

if [[ ! -x cmake_targets/build_oai ]]; then
  echo "build_oai script not found in $REPO_DIR/cmake_targets" >&2
  exit 1
fi

cd cmake_targets
./build_oai -I
./build_oai -w USRP --ninja --nrUE --gNB --build-lib "nrscope" -C

echo "Build completed."
echo "Use the official OAI tutorial commands from doc/NR_SA_Tutorial_OAI_nrUE.md to run nrUE and gNB."
