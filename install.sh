#!/bin/bash

set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv is not installed. Installing now..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
else
  echo "uv is already installed."
fi

uv venv .venv --python=3.11
uv sync
