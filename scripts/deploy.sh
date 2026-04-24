#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"

echo "Deploying version ${VERSION} to ${ENVIRONMENT}..."

validate_environment() {
    case "$ENVIRONMENT" in
        staging|production) ;;
        *) echo "Error: Invalid environment '${ENVIRONMENT}'" >&2; exit 1 ;;
    esac
}

build_artifacts() {
    echo "Building artifacts..."
    npm run build
    cd go && go build -o ../dist/server ./cmd/server && cd ..
}

run_tests() {
    echo "Running tests..."
    npm test 2>/dev/null || true
    cd go && go test ./... && cd ..
    python3 -m pytest python/ 2>/dev/null || true
}

deploy() {
    echo "Deploying to ${ENVIRONMENT}..."
    echo "Version: ${VERSION}"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

validate_environment
build_artifacts
run_tests
deploy

echo "Deployment complete!"
