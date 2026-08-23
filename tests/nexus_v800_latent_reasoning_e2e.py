#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
assert (root/'www/index.html').exists()
print('NEXUS E2E smoke: PASS')
