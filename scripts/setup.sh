#!/usr/bin/env bash
set -euo pipefail

echo "Setting up copilot-demo-project..."

# Install Node.js dependencies
if command -v npm &> /dev/null; then
    echo "Installing npm dependencies..."
    npm install
fi

# Set up Python virtual environment
if command -v python3 &> /dev/null; then
    echo "Setting up Python environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r python/requirements.txt 2>/dev/null || true
fi

# Build Go services
if command -v go &> /dev/null; then
    echo "Building Go services..."
    cd go && go build ./... && cd ..
fi

echo "Setup complete!"
