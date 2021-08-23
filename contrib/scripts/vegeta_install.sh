#!/usr/bin/env bash
set -euo pipefail

if [ ! -x ./vegeta ]; then
  VERSION=$(curl -s https://api.github.com/repos/tsenart/vegeta/git/refs/tags | jq -r '.[].ref' | cut -d'/' -f3 | tail -n1)
  curl --progress-bar -LO "https://github.com/tsenart/vegeta/releases/download/$VERSION/vegeta_${VERSION/v/}_linux_amd64.tar.gz"
  tar -xf vegeta*.tar.gz vegeta
  rm vegeta*.tar.gz
fi

./vegeta --version
