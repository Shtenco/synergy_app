#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
assert (root/'www/js/app.js').exists()
print('capital curve UI smoke: PASS')
