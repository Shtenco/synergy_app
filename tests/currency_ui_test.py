#!/usr/bin/env python3
from pathlib import Path
text=(Path(__file__).resolve().parents[1]/'www/index.html').read_text(encoding='utf-8')
assert 'SINERGY Finance' in text
print('currency/UI smoke: PASS')
