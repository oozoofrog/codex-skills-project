#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], label: str) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    output = (proc.stdout or '') + (proc.stderr or '')
    ok = proc.returncode == 0
    prefix = '✅' if ok else '❌'
    print(f'{prefix} {label}')
    if output.strip():
        print(output.strip())
    return ok, output


def check_json_files() -> bool:
    print('\n## JSON 검증')
    ok = True
    paths = [ROOT / '.agents' / 'plugins' / 'marketplace.json']
    paths += sorted((ROOT / 'plugins').glob('*/.codex-plugin/plugin.json'))
    paths += sorted((ROOT / 'plugins').glob('*/.mcp.json'))
    for path in paths:
        try:
            json.loads(path.read_text())
            print(f'✅ JSON OK: {path.relative_to(ROOT)}')
        except Exception as exc:
            ok = False
            print(f'❌ JSON FAIL: {path.relative_to(ROOT)} -> {exc}')
    return ok


def check_assets() -> bool:
    print('\n## Asset 검증')
    ok = True
    for plugin_dir in sorted((ROOT / 'plugins').glob('*')):
        if not plugin_dir.is_dir():
            continue
        assets = plugin_dir / 'assets'
        expected = ['icon.svg', 'icon.png', 'logo.svg', 'logo.png', 'screenshot.svg', 'screenshot.png']
        missing = [name for name in expected if not (assets / name).exists()]
        if missing:
            ok = False
            print(f'❌ {plugin_dir.name}: missing {", ".join(missing)}')
        else:
            print(f'✅ {plugin_dir.name}: assets complete')
    return ok


def check_manifest_paths() -> bool:
    print('\n## Manifest 경로 검증')
    ok = True
    for manifest in sorted((ROOT / 'plugins').glob('*/.codex-plugin/plugin.json')):
        data = json.loads(manifest.read_text())
        plugin_root = manifest.parent.parent
        interface = data.get('interface', {})
        refs = []
        for key in ['composerIcon', 'logo']:
            if interface.get(key):
                refs.append(interface[key])
        for shot in interface.get('screenshots', []) or []:
            refs.append(shot)
        if isinstance(data.get('mcpServers'), str):
            refs.append(data['mcpServers'])
        if isinstance(data.get('skills'), str):
            refs.append(data['skills'])
        broken = []
        for rel in refs:
            if not rel.startswith('./'):
                broken.append(rel)
                continue
            if not (plugin_root / rel[2:]).exists():
                broken.append(rel)
        if broken:
            ok = False
            print(f'❌ {plugin_root.name}: broken refs -> {broken}')
        else:
            print(f'✅ {plugin_root.name}: manifest refs valid')
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description='Run static smoke checks for local Codex plugins.')
    parser.add_argument('--skip-regenerate', action='store_true', help='Skip packaged plugin regeneration step')
    args = parser.parse_args()

    overall_ok = True

    print('# Local Codex Plugin Smoke Checks')
    print(f'Root: {ROOT}')

    if not args.skip_regenerate:
        ok, _ = run(['python3', 'scripts/sync_packaged_plugins.py'], 'packaged plugin 재생성')
        overall_ok &= ok

    ok, _ = run(['python3', '-m', 'py_compile', 'scripts/sync_packaged_plugins.py', '.agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py', '.agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py'], 'Python compile')
    overall_ok &= ok

    overall_ok &= check_json_files()
    overall_ok &= check_assets()
    overall_ok &= check_manifest_paths()

    ok, _ = run(['python3', '.agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py', '.'], 'plugin-doctor 감사')
    overall_ok &= ok
    ok, _ = run(['python3', '.agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py', '.'], 'skill audit')
    overall_ok &= ok

    print('\n## 결과')
    if overall_ok:
        print('✅ 모든 정적 스모크 체크를 통과했습니다.')
        print('다음 단계: Codex를 재시작하고 docs/local-plugin-testing.md의 로컬 로딩 확인 절차를 수동 실행하세요.')
        return 0

    print('❌ 실패한 항목이 있습니다. 위 로그를 확인하세요.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
