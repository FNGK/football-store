#!/usr/bin/env bash
set -euo pipefail
ENV_FILE="${1:-apps/api/.env}"
if [ -f "$ENV_FILE" ]; then
  echo "Exists: $ENV_FILE (not overwriting)"
  exit 0
fi
SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")
PII=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
cp apps/api/.env.example "$ENV_FILE"
sed -i "s|REPLACE_WITH_SECRET_MIN_32_CHARS.*|$SECRET|" "$ENV_FILE"
sed -i "s|^PII_FERNET_KEY=.*|PII_FERNET_KEY=$PII|" "$ENV_FILE"
echo "Created $ENV_FILE with generated secrets."
