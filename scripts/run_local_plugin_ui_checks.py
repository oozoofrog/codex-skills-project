#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'reports'


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def build_plugin_rows(selected: set[str] | None):
    marketplace = load_json(ROOT / '.agents' / 'plugins' / 'marketplace.json')
    plugins = marketplace.get('plugins', [])
    rows = []
    findings = []
    for entry in plugins:
        name = entry['name']
        if selected and name not in selected:
            continue
        plugin_root = ROOT / 'plugins' / name
        manifest_path = plugin_root / '.codex-plugin' / 'plugin.json'
        manifest = load_json(manifest_path)
        interface = manifest.get('interface', {})

        screenshots = interface.get('screenshots', []) or []
        prompts = interface.get('defaultPrompt', []) or []
        composer_icon = interface.get('composerIcon')
        logo = interface.get('logo')
        display_name = interface.get('displayName', '')
        short_description = interface.get('shortDescription', '')
        category = interface.get('category', entry.get('category', ''))

        if not display_name:
            findings.append((name, 'displayName missing in plugin interface'))
        if not short_description:
            findings.append((name, 'shortDescription missing in plugin interface'))
        if not category:
            findings.append((name, 'category missing in plugin interface'))
        if not isinstance(prompts, list) or not prompts:
            findings.append((name, 'defaultPrompt list missing or empty'))
        if not isinstance(screenshots, list) or not screenshots:
            findings.append((name, 'screenshots list missing or empty'))

        refs = []
        for label, rel in [('composerIcon', composer_icon), ('logo', logo)]:
            if isinstance(rel, str):
                refs.append((label, rel))
            else:
                findings.append((name, f'{label} missing or invalid'))
        for idx, rel in enumerate(screenshots, start=1):
            refs.append((f'screenshots[{idx}]', rel))

        broken_refs = []
        for label, rel in refs:
            if not isinstance(rel, str) or not rel.startswith('./'):
                broken_refs.append(f'{label}:{rel}')
                continue
            if not (plugin_root / rel[2:]).exists():
                broken_refs.append(f'{label}:{rel}')
        if broken_refs:
            findings.append((name, 'broken UI asset refs -> ' + ', '.join(broken_refs)))

        rows.append({
            'name': name,
            'display_name': display_name,
            'category': category,
            'short_description': short_description,
            'source_path': f'plugins/{name}',
            'screenshot_count': len(screenshots),
            'screenshots': screenshots,
            'prompt_count': len(prompts) if isinstance(prompts, list) else 0,
            'example_prompt': prompts[0] if isinstance(prompts, list) and prompts else '',
            'composer_icon': composer_icon,
            'logo': logo,
            'manual_checks': [
                'catalog에 보이는지 확인',
                'detail panel에서 아이콘/로고/스크린샷이 보이는지 확인',
                'starter prompt 1개 실행',
            ],
        })
    return rows, findings


def render_markdown(rows, findings):
    lines = [
        '# Local Plugin UI Verification Report',
        '',
        f'- Generated: {datetime.now().isoformat(timespec="seconds")}',
        f'- Root: `{ROOT}`',
        f'- Plugins covered: `{len(rows)}`',
        f'- Findings: `{len(findings)}`',
        '',
        '## Summary',
        '- 이 리포트는 로컬 plugin UI에서 확인해야 할 표시명, 카테고리, 아이콘/로고/스크린샷, starter prompt를 구조화합니다.',
        '',
        '## Findings',
    ]
    if not findings:
        lines.append('- None')
    else:
        for plugin_name, message in findings:
            lines.append(f'- [warning] `{plugin_name}` — {message}')

    lines.extend(['', '## Plugins to verify'])
    for row in rows:
        lines.append(f'### {row["name"]}')
        lines.append(f'- Display: `{row["display_name"]}`')
        lines.append(f'- Category: `{row["category"]}`')
        lines.append(f'- Source: `{row["source_path"]}`')
        lines.append(f'- Short description: {row["short_description"]}')
        lines.append(f'- UI assets: composerIcon=`{row["composer_icon"]}`, logo=`{row["logo"]}`')
        lines.append(f'- Screenshots: `{row["screenshot_count"]}`')
        for shot in row['screenshots']:
            lines.append(f'  - `{shot}`')
        lines.append(f'- Starter prompts: `{row["prompt_count"]}`')
        if row['example_prompt']:
            lines.append(f'  - Example prompt: `{row["example_prompt"]}`')
        lines.append('- Manual checks:')
        for item in row['manual_checks']:
            lines.append(f'  - [ ] {item}')
        lines.append('')

    lines.extend([
        '## Next manual steps',
        '1. `python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate` 실행',
        '2. Codex를 현재 저장소 루트에서 재시작',
        '3. local catalog에서 각 plugin card와 detail panel을 확인',
        '4. plugin별 starter prompt 1개 이상 실행',
        '',
        '## Machine summary',
        '```json',
        json.dumps({
            'report_type': 'local-plugin-ui-check',
            'schema_version': 1,
            'root': str(ROOT),
            'plugins_count': len(rows),
            'findings_count': len(findings),
            'findings': [{'plugin': plugin, 'message': message} for plugin, message in findings],
            'plugins': rows,
        }, ensure_ascii=False, indent=2),
        '```',
        '',
    ])
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Build a semi-automated local plugin UI verification report.')
    parser.add_argument('--plugin', action='append', help='특정 plugin만 포함')
    parser.add_argument('--strict', action='store_true', help='finding이 있으면 non-zero 종료')
    parser.add_argument('--write-report', action='store_true', help='reports/ 아래에 markdown/json artifact 저장')
    parser.add_argument('--json-out', help='JSON summary 저장 경로')
    parser.add_argument('--markdown-out', help='Markdown report 저장 경로')
    args = parser.parse_args()

    selected = set(args.plugin) if args.plugin else None
    rows, findings = build_plugin_rows(selected)
    markdown = render_markdown(rows, findings)
    print(markdown, end='')

    payload = {
        'report_type': 'local-plugin-ui-check',
        'schema_version': 1,
        'root': str(ROOT),
        'plugins_count': len(rows),
        'findings_count': len(findings),
        'findings': [{'plugin': plugin, 'message': message} for plugin, message in findings],
        'plugins': rows,
    }

    if args.write_report:
        REPORTS.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        md_path = REPORTS / f'local-plugin-ui-report-{ts}.md'
        json_path = REPORTS / f'local-plugin-ui-report-{ts}.json'
        md_path.write_text(markdown, encoding='utf-8')
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\nreport markdown: {md_path}')
        print(f'report json: {json_path}')

    if args.markdown_out:
        out = Path(args.markdown_out).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding='utf-8')
    if args.json_out:
        out = Path(args.json_out).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    if args.strict and findings:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
