#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def require(path):
    p=ROOT/path
    assert p.exists(), f"missing: {path}"
    return p

android = require('android/app/build.gradle').read_text(encoding='utf-8')
manifest = require('android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
require('ios/SinergyFinance.xcodeproj/project.pbxproj')
require('ios/SinergyFinance/PrivacyInfo.xcprivacy')
assert "applicationId 'ai.sinergy.finance'" in android
assert 'compileSdk 36' in android and 'targetSdk 36' in android
assert "versionName '8.1.0'" in android and 'versionCode 810' in android
assert 'android:usesCleartextTraffic="false"' in manifest
assert 'android:allowBackup="false"' in manifest
for forbidden in ['CAMERA','RECORD_AUDIO','READ_CONTACTS','ACCESS_FINE_LOCATION','READ_SMS']:
    assert forbidden not in manifest, f"dangerous permission present: {forbidden}"
print('STORE SOURCE VERIFY: PASS')
