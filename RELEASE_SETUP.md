# SINERGY Finance — Mobile Release Setup

This repository includes `.github/workflows/release.yml` for Android APK/AAB, Google Play, iOS IPA, TestFlight, and GitHub Releases.

## Android

The workflow auto-detects either `./gradlew` or `./android/gradlew`.

### Required GitHub Actions secrets for signed Android releases

- `ANDROID_KEYSTORE_BASE64` — release keystore encoded with Base64
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

The Android Gradle project should read these environment variables when configuring the release signing config:

- `SIGNING_STORE_FILE`
- `SIGNING_STORE_PASSWORD`
- `SIGNING_KEY_ALIAS`
- `SIGNING_KEY_PASSWORD`

### Google Play

Repository variable:

- `ANDROID_PACKAGE_NAME` — e.g. `com.sinergy.finance`

Secret:

- `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` — Google Play service-account JSON with access to the application in Play Console

A manual workflow run can select `internal`, `beta`, or `production`. Tag builds (`v*`) also execute the release workflow.

## iOS / TestFlight

The workflow auto-detects `.xcworkspace` or `.xcodeproj` within four directory levels.

Repository variable:

- `IOS_SCHEME` — shared Xcode scheme to archive

Required secrets:

- `APPLE_TEAM_ID`
- `APPLE_CERTIFICATE_P12_BASE64`
- `APPLE_CERTIFICATE_PASSWORD`
- `APPLE_KEYCHAIN_PASSWORD`
- `APP_STORE_CONNECT_KEY_ID`
- `APP_STORE_CONNECT_ISSUER_ID`
- `APP_STORE_CONNECT_API_KEY_BASE64` — Base64 encoded App Store Connect `.p8` API key

The Xcode project must use an App Store-compatible Bundle ID and signing configuration. The workflow archives the app, exports an App Store Connect IPA, uploads the IPA as a GitHub Actions artifact, and uploads it to TestFlight when App Store Connect credentials are configured.

## GitHub Release

Push a semantic version tag such as:

```bash
git tag v1.0.0
git push origin v1.0.0
```

or run the workflow manually and enable `create_github_release`.

The workflow attaches generated Android/iOS artifacts that were successfully built.

## Recommended repository layout

Either native projects at repository root:

```text
./gradlew
./app/
./SINERGY.xcodeproj
```

or separated projects:

```text
/android/gradlew
/android/app/
/ios/SINERGY.xcodeproj
```

## Security

Never commit keystores, `.p12`, `.p8`, passwords, provisioning credentials, or Google service-account JSON into Git. Store them only as GitHub Actions secrets.
