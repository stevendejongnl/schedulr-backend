#!/usr/bin/env sh

API_URL="https://api.github.com/repos/pre-commit/pre-commit/releases/latest"
PRE_COMMIT_FILE="scripts/pre-commit.pyz"

if [ ! -f "$PRE_COMMIT_FILE" ]; then
  LATEST_RELEASE_JSON=$(curl -s $API_URL)
  PYZ_URL=$(echo "$LATEST_RELEASE_JSON" | jq -r '.assets[] | select(.name | endswith(".pyz")).browser_download_url')
  echo "pre-commit.pyz does not exist. Downloading from $PYZ_URL..."
  curl -L "$PYZ_URL" -o $PRE_COMMIT_FILE
fi

python $PRE_COMMIT_FILE "$@"
