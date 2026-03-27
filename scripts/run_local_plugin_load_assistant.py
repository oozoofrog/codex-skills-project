#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'reports'


def main() -> int:
    parser = argparse.ArgumentParser(description='Prepare a local Codex plugin load checklist and optional docs open step.')
    parser.add_argument('--open-docs', action='store_true', help='Open the testing doc and generated checklist on macOS')
    parser.add_argument('--run-smoke', action='store_true', help='Run static smoke checks before generating the checklist')
    args = parser.parse_args()

    if args.run_smoke:
        result = subprocess.run(['python3', 'scripts/run_local_plugin_smoke_checks.py', '--skip-regenerate'], cwd=ROOT)
        if result.returncode != 0:
            print('정적 스모크 체크가 실패했습니다. 체크리스트 생성은 계속하지만 먼저 실패 원인을 확인하세요.')

    marketplace = json.loads((ROOT / '.agents' / 'plugins' / 'marketplace.json').read_text())
    plugins = marketplace.get('plugins', [])

    REPORTS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y-%m-%d-%H%M%S')
    report_path = REPORTS / f'local-plugin-load-checklist-{ts}.md'

    lines = [
        '# Local Plugin Load Checklist',
        '',
        f'- Generated: {datetime.now().isoformat(timespec="seconds")}',
        f'- Root: `{ROOT}`',
        '',
        '## Preflight',
        '',
        '1. `python3 scripts/sync_packaged_plugins.py` 실행',
        '2. `python3 scripts/run_local_plugin_smoke_checks.py` 실행',
        '3. Codex를 현재 저장소 루트에서 재시작',
        '',
        '## Plugins to verify',
        '',
    ]

    for entry in plugins:
        name = entry['name']
        plugin_manifest = ROOT / 'plugins' / name / '.codex-plugin' / 'plugin.json'
        manifest = json.loads(plugin_manifest.read_text())
        interface = manifest.get('interface', {})
        prompts = interface.get('defaultPrompt', [])
        lines.append(f'### {name}')
        lines.append(f'- Display: `{interface.get("displayName", name)}`')
        lines.append(f'- Source: `plugins/{name}`')
        lines.append(f'- Category: `{entry.get("category", "N/A")}`')
        lines.append('- Manual checks:')
        lines.append('  - [ ] catalog에 보이는지 확인')
        lines.append('  - [ ] 상세 패널에서 아이콘/로고/스크린샷이 보이는지 확인')
        lines.append('  - [ ] starter prompt 1개 실행')
        if prompts:
            lines.append(f'  - Example prompt: `{prompts[0]}`')
        lines.append('')

    lines.extend([
        '## Notes',
        '',
        '- 현재 packaged screenshot은 representative preview이며, live Codex UI capture는 아닙니다.',
        '- 실제 live capture로 교체하려면 plugin 로딩 후 수동 캡처 또는 별도 UI 자동화가 필요합니다.',
        '',
        '## References',
        '',
        '- `docs/local-plugin-testing.md`',
        '- `plugins/README.md`',
    ])

    report_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'체크리스트 생성: {report_path}')

    if args.open_docs:
        subprocess.run(['open', str(ROOT / 'docs' / 'local-plugin-testing.md')], cwd=ROOT)
        subprocess.run(['open', str(report_path)], cwd=ROOT)
        print('문서를 열었습니다.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
