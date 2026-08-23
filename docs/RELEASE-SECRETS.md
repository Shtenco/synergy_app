# SINERGY Finance — Store CI/CD secrets

The workflows never commit signing keys or store credentials. Add these in GitHub → Settings → Secrets and variables → Actions.

## Android signing (Google Play + RuStore)

- `SINERGY_KEYSTORE_B64` — base64 of the upload JKS/keystore.
- `SINERGY_KEYSTORE_PASSWORD`
- `SINERGY_KEY_ALIAS`
- `SINERGY_KEY_PASSWORD`

Keep this upload key stable. If Google Play App Signing is enabled, this is the upload key, not Google's app-signing private key.

## Google Play

- `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` — complete JSON for a Google Cloud service account that has access to the app in Play Console.

The workflow uploads to the `internal` track first. Promote to production after review/testing.

Optional repository variable:

- `AUTO_PUBLISH_GOOGLE_PLAY=true` — publish automatically when a `v*` tag is pushed.

## Apple / TestFlight / App Store

- `SINERGY_APPLE_TEAM_ID`
- `APPLE_DISTRIBUTION_CERT_P12_B64` — base64 of Apple Distribution `.p12`.
- `APPLE_DISTRIBUTION_CERT_PASSWORD`
- `APPLE_PROVISIONING_PROFILE_B64` — base64 App Store provisioning profile for `ai.sinergy.finance`.
- `APP_STORE_CONNECT_KEY_ID`
- `APP_STORE_CONNECT_ISSUER_ID`
- `APP_STORE_CONNECT_PRIVATE_KEY` — contents of the App Store Connect `.p8` private key.

Optional repository variable:

- `AUTO_PUBLISH_TESTFLIGHT=true`

The CI uploads a signed IPA to App Store Connect/TestFlight. App Store review/release metadata is still controlled in App Store Connect.

## RuStore

- `RUSTORE_KEY_ID`
- `RUSTORE_PRIVATE_KEY`
- `RUSTORE_VERSION_ID` — id of an existing draft version in RuStore.

Optional repository variable:

- `AUTO_PUBLISH_RUSTORE=true`

Important: RuStore's publication API requires at least one active app version before API-based publication is available. For a brand-new listing, create/activate the first version in RuStore Console, then the CI can automate subsequent binary uploads.

## Release convention

1. Update Android `versionName`/`versionCode` and iOS `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` together.
2. Push and let `Verify store source` pass.
3. Run **Store Release** manually with selected stores, or push a tag such as `v8.1.1` after enabling the corresponding `AUTO_PUBLISH_*` repository variables.
4. GitHub Release contains signed APK, AAB and IPA plus SHA-256 files when both platform builds succeed.
