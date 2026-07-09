#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Please run this script as root or with sudo." >&2
  exit 1
fi

apt-get update
apt-get install -y \
  autoconf automake build-essential ccache cmake cpufrequtils \
  doxygen ethtool g++ git inetutils-tools libboost-all-dev \
  libncurses-dev libusb-1.0-0 libusb-1.0-0-dev libusb-dev \
  python3-dev python3-mako python3-numpy python3-requests \
  python3-scipy python3-setuptools python3-ruamel.yaml

echo "Prerequisites installation complete."
