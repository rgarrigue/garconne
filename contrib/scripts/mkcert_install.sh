#!/usr/bin/env bash
set -euo pipefail

if ! command -v certutil &>/dev/null; then
  sudo apt install -yq libnss3-tools
fi

if [ ! -x ./mkcert ]; then
  VERSION=$(curl -s https://api.github.com/repos/FiloSottile/mkcert/git/refs/tags | jq -r '.[].ref' | cut -d'/' -f3 | tail -n1)
  curl --progress-bar -L "https://github.com/FiloSottile/mkcert/releases/download/$VERSION/mkcert-${VERSION}-linux-amd64" -o ./mkcert
  chmod +x ./mkcert
fi

./mkcert --version
