#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST_DIR = ROOT / 'assets' / 'browser-captures'


def normalize_png(source: Path, dest: Path, max_width: int) -> None:
    tmp = dest.with_suffix(source.suffix if source.suffix else '.png')
    shutil.copy2(source, tmp)
    subprocess.run(['sips', '-Z', str(max_width), str(tmp)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if tmp.suffix.lower() != '.png':
        subprocess.run(['sips', '-s', 'format', 'png', str(tmp), '--out', str(dest)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tmp.unlink(missing_ok=True)
    elif tmp != dest:
        tmp.replace(dest)


def main() -> int:
    parser = argparse.ArgumentParser(description='Install an external-browser capture for a packaged plugin.')
    parser.add_argument('plugin_name', help='Kebab-case plugin name (e.g. apple-craft)')
    parser.add_argument('source_image', help='Path to the captured PNG/JPEG image')
    parser.add_argument('--max-width', type=int, default=1440, help='Resize longest edge down to this size with sips')
    args = parser.parse_args()

    src = Path(args.source_image).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f'입력 파일이 없습니다: {src}')

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    dest = DEST_DIR / f'{args.plugin_name}.png'
    normalize_png(src, dest, args.max_width)
    print(f'browser capture updated: {dest}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
