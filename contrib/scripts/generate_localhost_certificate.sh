#!/usr/bin/env bash
set -euo pipefail

if [ ! -f contrib/certs/localhost.key.pem ]; then
  ./mkcert \
    -cert-file contrib/certs/localhost.crt.pem \
    -key-file contrib/certs/localhost.key.pem \
    localhost \
    app.localhost \
    cadvisor.localhost \
    grafana.localhost \
    prometheus.localhost \
    redis.localhost \
    traefik.localhost \
    127.0.0.1 \
    ::1
  chmod 0600 contrib/certs/*.pem
fi
