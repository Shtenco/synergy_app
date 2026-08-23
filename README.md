# SINERGY Finance

Store release repository for `ai.sinergy.finance`.

## Targets

- Apple App Store / TestFlight
- Google Play
- RuStore
- GitHub Releases (signed APK/AAB/IPA artifacts when platform signing is configured)

## Current release

- Version: `8.1.0`
- Android versionCode: `810`
- Android compile/target SDK: `36`
- iOS bundle ID: `ai.sinergy.finance`
- iOS deployment target: `16.0`

## CI/CD

The primary pipeline is `.github/workflows/store-release.yml`.

It performs:

1. store-source verification;
2. deterministic synchronization of `www/` into Android and iOS bundles;
3. signed Android APK + AAB build;
4. optional Google Play internal-track upload;
5. optional RuStore AAB upload;
6. signed iOS archive + IPA export;
7. optional App Store Connect / TestFlight upload;
8. GitHub Release artifact publication.

Store credentials and signing material are intentionally not committed. See `docs/RELEASE-SECRETS.md`.

## Source layout

- `android/` — Android store project
- `ios/` — Xcode project
- `www/` — shared web UI bundled into both platforms
- `store/` — listing/privacy/review metadata
- `scripts/` — build, asset sync and store upload tooling
- `tests/` — source smoke/regression checks

## Release safety

Do not commit keystores, `.p12`, `.p8`, provisioning profiles or store API credentials. Keep the Android upload key stable across releases.
