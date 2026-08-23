#!/usr/bin/env python3
"""Upload an AAB to an existing RuStore draft version."""
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE = "https://public-api.rustore.ru"


def req(url, *, method="GET", headers=None, data=None):
    r = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            body = resp.read()
            return resp.status, json.loads(body.decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise SystemExit(f"RuStore HTTP {e.code}: {body}")


def auth_token(key_id, private_key):
    payload = json.dumps({"keyId": key_id, "timestamp": int(time.time() * 1000)}).encode()
    status, data = req(
        f"{BASE}/public/auth/",
        method="POST",
        headers={"Content-Type": "application/json"},
        data=payload,
    )
    token = data.get("body", {}).get("jwe") or data.get("jwe") or data.get("token")
    if not token:
        raise SystemExit(f"RuStore auth response did not contain token: {data}")
    return token


def multipart(field, path):
    boundary = "----SinergyRuStoreBoundary"
    filename = os.path.basename(path)
    with open(path, "rb") as f:
        content = f.read()
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n"
    ).encode()
    tail = f"\r\n--{boundary}--\r\n".encode()
    return boundary, head + content + tail


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: rustore_upload.py path/to/app.aab")
    aab = sys.argv[1]
    key_id = os.environ["RUSTORE_KEY_ID"]
    private_key = os.environ["RUSTORE_PRIVATE_KEY"]
    package = os.environ["RUSTORE_PACKAGE_NAME"]
    version_id = os.environ["RUSTORE_VERSION_ID"]
    token = auth_token(key_id, private_key)
    boundary, body = multipart("file", aab)
    url = f"{BASE}/public/v1/application/{package}/version/{version_id}/aab"
    status, data = req(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        data=body,
    )
    print(json.dumps({"status": status, "response": data}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
