#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-$HOME/openairinterface5g}"

if [[ ! -d "$REPO_DIR" ]]; then
  echo "Repository directory not found: $REPO_DIR" >&2
  exit 1
fi

cd "$REPO_DIR"

if [[ ! -x cmake_targets/build_oai ]]; then
  echo "build_oai script not found under $REPO_DIR/cmake_targets" >&2
  exit 1
fi

cd cmake_targets
./build_oai -I
./build_oai -w USRP --ninja --nrUE --gNB --build-lib "nrscope" -C

echo "Build completed."
