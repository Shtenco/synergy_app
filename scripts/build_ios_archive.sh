#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../ios"
: "${SINERGY_APPLE_TEAM_ID:?SINERGY_APPLE_TEAM_ID is required}"
xcodebuild -version
xcodebuild -project SinergyFinance.xcodeproj -scheme SinergyFinance -configuration Release -destination 'generic/platform=iOS' -archivePath build/SinergyFinance.xcarchive archive DEVELOPMENT_TEAM="$SINERGY_APPLE_TEAM_ID"
echo "ARCHIVE: ios/build/SinergyFinance.xcarchive"
