#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / 'assets' / 'live-captures' / 'codex-live-capture.png'


def main() -> int:
    parser = argparse.ArgumentParser(description='Install a captured Codex UI screenshot as the shared live-capture asset.')
    parser.add_argument('source_image', help='Path to the captured PNG/JPEG image')
    parser.add_argument('--max-width', type=int, default=1440, help='Resize longest edge down to this size with sips')
    args = parser.parse_args()

    src = Path(args.source_image).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f'입력 파일이 없습니다: {src}')

    DEST.parent.mkdir(parents=True, exist_ok=True)
    tmp = DEST.with_suffix(src.suffix if src.suffix else '.png')
    shutil.copy2(src, tmp)
    subprocess.run(['sips', '-Z', str(args.max_width), str(tmp)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp.suffix.lower() != '.png':
        subprocess.run(['sips', '-s', 'format', 'png', str(tmp), '--out', str(DEST)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tmp.unlink(missing_ok=True)
    else:
        if tmp != DEST:
            tmp.replace(DEST)
    print(f'live capture updated: {DEST}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
