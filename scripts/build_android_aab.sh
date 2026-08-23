#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../android"
: "${ANDROID_HOME:?ANDROID_HOME is required}"
: "${SINERGY_KEYSTORE_FILE:?SINERGY_KEYSTORE_FILE is required for signed release}"
: "${SINERGY_KEYSTORE_PASSWORD:?SINERGY_KEYSTORE_PASSWORD is required}"
: "${SINERGY_KEY_ALIAS:?SINERGY_KEY_ALIAS is required}"
: "${SINERGY_KEY_PASSWORD:?SINERGY_KEY_PASSWORD is required}"
gradle --no-daemon clean :app:bundleRelease
AAB=app/build/outputs/bundle/release/app-release.aab
sha256sum "$AAB" > "$AAB.sha256"
echo "SIGNED AAB: $AAB"
