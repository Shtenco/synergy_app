#!/usr/bin/env python3
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
src = root / 'www'
for dst in [root/'android/app/src/main/assets/www', root/'ios/SinergyFinance/www']:
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)
print('synced www -> Android/iOS')
