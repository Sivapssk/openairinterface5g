#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-$HOME/openairinterface5g}"
BUILD_DIR="${BUILD_DIR:-$REPO_DIR/cmake_targets/ran_build/build}"

if [[ ! -d "$BUILD_DIR" ]]; then
  echo "Build directory not found: $BUILD_DIR" >&2
  exit 1
fi

cd "$BUILD_DIR"

sudo ./nr-uesoftmodem -r 106 \
  --numerology 1 \
  --band 78 \
  -C 3619200000 \
  --uicc0.imsi 001010000000001 \
  --rfsim
