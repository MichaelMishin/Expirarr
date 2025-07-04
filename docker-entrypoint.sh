#!/bin/sh
set -e

CONFIG_FILE="/app/config/config.yaml"
EXAMPLE_FILE="/app/expirarr/config.example.yaml"

# If config.yaml does not exist, copy the example
if [ ! -f "$CONFIG_FILE" ]; then
    echo "No config.yaml found, copying example config."
    cp "$EXAMPLE_FILE" "$CONFIG_FILE"
fi

cd /app  # Ensure working directory is /app

exec "$@"
