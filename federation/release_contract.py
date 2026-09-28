from __future__ import annotations
from hashlib import sha256
import re
from pathlib import Path
from typing import Any

CONTRACT_ID="synergy.app.store-source-evidence/v1"
AUTHORITY="mobile_source_integrity"
ROOT=Path(__file__).resolve().parents[1]

def _digest(path:Path)->str:
    return sha256(path.read_bytes()).hexdigest()

def store_source_evidence_payload() -> dict[str, Any]:
    gradle=ROOT/"android/app/build.gradle"
    manifest=ROOT/"android/app/src/main/AndroidManifest.xml"
    iosproj=ROOT/"ios/SinergyFinance.xcodeproj/project.pbxproj"
    privacy=ROOT/"ios/SinergyFinance/PrivacyInfo.xcprivacy"
    for p in (gradle,manifest,iosproj,privacy):
        if not p.is_file(): raise ValueError(f"missing source surface: {p.relative_to(ROOT)}")
    g=gradle.read_text(encoding="utf-8")
    m=manifest.read_text(encoding="utf-8")
    version=re.search(r"versionName\s+'([^']+)'",g)
    if not version: raise ValueError("versionName missing")
    if "targetSdk 36" not in g or "compileSdk 36" not in g:
        raise ValueError("Android SDK baseline mismatch")
    if 'android:usesCleartextTraffic="false"' not in m or 'android:allowBackup="false"' not in m:
        raise ValueError("Android security baseline missing")
    forbidden=["CAMERA","RECORD_AUDIO","READ_CONTACTS","ACCESS_FINE_LOCATION","READ_SMS"]
    if any(x in m for x in forbidden):
        raise ValueError("dangerous permission present")
    return {
        "app_id":"ai.sinergy.finance",
        "version":version.group(1),
        "android_gradle_sha256":_digest(gradle),
        "android_manifest_sha256":_digest(manifest),
        "ios_project_sha256":_digest(iosproj),
        "ios_privacy_sha256":_digest(privacy),
        "source_verified":True,
        "artifact_built":False,
        "store_published":False,
        "deployment_authority":False,
    }
