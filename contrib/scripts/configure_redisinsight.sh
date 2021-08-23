#!/usr/bin/env bash
set -euo pipefail

cat <<EOF | curl -d - -sLk -X POST https://redis.localhost/api/instance/
{
  "name": "Redis DB",
  "connectionType": "STANDALONE",
  "host": "redis",
  "port": 6379
}
EOF
