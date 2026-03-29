#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def execute(cmd: list[str], *, cwd: Path = ROOT) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    output = (proc.stdout or '') + (proc.stderr or '')
    return proc.returncode == 0, output


def run(cmd: list[str], label: str, *, cwd: Path = ROOT) -> tuple[bool, str]:
    ok, output = execute(cmd, cwd=cwd)
    prefix = '✅' if ok else '❌'
    print(f'{prefix} {label}')
    if output.strip():
        print(output.strip())
    return ok, output


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ['git', *args],
        cwd=str(cwd),
        check=check,
        capture_output=True,
        text=True,
    )


def latest_tag() -> str:
    tags = git('tag', '--sort=-creatordate').stdout.splitlines()
    if not tags:
        raise SystemExit('오류: git tag가 없습니다.')
    return tags[0].strip()


def next_patch(version: str) -> str:
    major, minor, patch = version.removeprefix('v').split('.')
    return f'v{major}.{minor}.{int(patch) + 1}'


def required_check_fragments(version: str) -> list[str]:
    return [
        '# Release helper summary',
        f'- version: {version}',
        '- changelog:',
        '- release notes:',
        '검증 통과.',
    ]


def required_plan_fragments(version: str) -> list[str]:
    return [
        '# Release helper summary',
        f'- version: {version}',
        '# Planned commands',
        f'git tag -a {version} -m {version}',
        f'gh release create {version} --title {version} --notes-file docs/release-notes-{version}.md',
    ]


def validate_output(
    *,
    label: str,
    output: str,
    required: list[str],
    forbidden: list[str] | None = None,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for fragment in required:
        if fragment not in output:
            errors.append(f'필수 문자열 누락: {fragment}')
    for fragment in forbidden or []:
        if fragment in output:
            errors.append(f'금지 문자열 존재: {fragment}')

    if errors:
        print(f'❌ {label} 출력 계약 검증 실패')
        for error in errors:
            print(f'  - {error}')
        preview = '\n'.join(output.strip().splitlines()[:40])
        if preview:
            print('  - 출력 미리보기:')
            print(preview)
        return False, errors

    print(f'✅ {label} 출력 계약 검증 통과')
    return True, []


def scenario(
    *,
    label: str,
    cmd: list[str],
    cwd: Path,
    required: list[str],
    forbidden: list[str] | None = None,
) -> tuple[bool, str]:
    ok, output = execute(cmd, cwd=cwd)
    prefix = '✅' if ok else '❌'
    print(f'{prefix} {label}')
    if output.strip():
        print(output.strip())
    if not ok:
        return False, output
    validated, _ = validate_output(
        label=label,
        output=output,
        required=required,
        forbidden=forbidden,
    )
    return validated, output


def seed_next_release_docs(worktree: Path, version: str) -> None:
    changelog = worktree / 'CHANGELOG.md'
    notes = worktree / 'docs' / f'release-notes-{version}.md'

    if notes.exists():
        return

    changelog_text = changelog.read_text(encoding='utf-8')
    heading = f'## {version} — TBD\n\n### 핵심 변경\n\n- smoke check fixture generated for release helper validation.\n\n### 검증에 사용한 명령\n\n```bash\npython3 scripts/release_helper.py check --version {version} --skip-gh-auth\npython3 scripts/release_helper.py plan --version {version} --skip-gh-auth\n```\n\n'
    changelog.write_text(changelog_text.replace('# CHANGELOG\n\n', '# CHANGELOG\n\n' + heading, 1), encoding='utf-8')
    notes.write_text(
        f'''## {version}

이 문서는 release helper smoke check를 위한 synthetic release notes fixture입니다.

### Highlights

- smoke check worktree에서 `{version}` 문서 준비 경로를 검증합니다.

### Recommended validation

```bash
python3 scripts/release_helper.py check --version {version} --skip-gh-auth
python3 scripts/release_helper.py plan --version {version} --skip-gh-auth
```
''',
        encoding='utf-8',
    )


def write_github_step_summary(*, latest: str, future: str, results: list[tuple[str, bool]]) -> None:
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return

    passed = sum(1 for _, ok in results if ok)
    failed = len(results) - passed
    log_path = os.environ.get('RELEASE_SMOKE_LOG_PATH')

    lines = [
        '## release-smoke',
        '',
        f'- command: `python3 scripts/run_release_smoke_checks.py --skip-gh-auth`',
        f'- latest tag: `{latest}`',
        f'- synthetic next patch: `{future}`',
        f'- passed: `{passed}`',
        f'- failed: `{failed}`',
    ]
    if log_path:
        lines.append(f'- log path: `{log_path}`')
    lines.extend(
        [
            '',
            '| scenario | status |',
            '|---|---|',
        ]
    )
    for label, ok in results:
        lines.append(f'| {label} | {"✅ pass" if ok else "❌ fail"} |')

    Path(summary_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Run smoke checks for scripts/release_helper.py')
    parser.add_argument('--skip-gh-auth', action='store_true', help='release_helper.py 실행 시 --skip-gh-auth를 전달합니다.')
    args = parser.parse_args()

    overall_ok = True
    scenario_results: list[tuple[str, bool]] = []

    print('# Release Helper Smoke Checks')
    print(f'Root: {ROOT}')

    ok, _ = run(['python3', '-m', 'py_compile', 'scripts/release_helper.py'], 'Python compile')
    overall_ok &= ok

    latest = latest_tag()
    latest_check = ['python3', 'scripts/release_helper.py', 'check', '--version', latest, '--allow-existing-tag', '--allow-dirty']
    latest_plan = ['python3', 'scripts/release_helper.py', 'plan', '--version', latest, '--allow-existing-tag', '--allow-dirty']
    latest_plan_publish = ['python3', 'scripts/release_helper.py', 'plan', '--version', latest, '--allow-existing-tag', '--allow-dirty', '--publish-release']
    if args.skip_gh_auth:
        latest_check.append('--skip-gh-auth')
        latest_plan.append('--skip-gh-auth')
        latest_plan_publish.append('--skip-gh-auth')

    ok, _ = scenario(
        label=f'current release check ({latest})',
        cmd=latest_check,
        cwd=ROOT,
        required=required_check_fragments(latest),
    )
    scenario_results.append((f'current release check ({latest})', ok))
    overall_ok &= ok
    ok, _ = scenario(
        label=f'current release plan ({latest})',
        cmd=latest_plan,
        cwd=ROOT,
        required=required_plan_fragments(latest) + ['--draft'],
    )
    scenario_results.append((f'current release plan ({latest})', ok))
    overall_ok &= ok
    ok, _ = scenario(
        label=f'current release publish-plan ({latest})',
        cmd=latest_plan_publish,
        cwd=ROOT,
        required=required_plan_fragments(latest),
        forbidden=['--draft'],
    )
    scenario_results.append((f'current release publish-plan ({latest})', ok))
    overall_ok &= ok

    temp_root = Path(tempfile.mkdtemp(prefix='release-smoke-'))
    worktree = temp_root / 'worktree'
    future = next_patch(latest)
    try:
        git('worktree', 'add', '--detach', str(worktree), 'HEAD')
        seed_next_release_docs(worktree, future)

        future_check = ['python3', 'scripts/release_helper.py', 'check', '--version', future, '--allow-dirty']
        future_plan = ['python3', 'scripts/release_helper.py', 'plan', '--version', future, '--allow-dirty']
        future_plan_publish = ['python3', 'scripts/release_helper.py', 'plan', '--version', future, '--allow-dirty', '--publish-release']
        if args.skip_gh_auth:
            future_check.append('--skip-gh-auth')
            future_plan.append('--skip-gh-auth')
            future_plan_publish.append('--skip-gh-auth')

        ok, _ = scenario(
            label=f'future release check ({future})',
            cmd=future_check,
            cwd=worktree,
            required=required_check_fragments(future),
        )
        scenario_results.append((f'future release check ({future})', ok))
        overall_ok &= ok
        ok, _ = scenario(
            label=f'future release plan ({future})',
            cmd=future_plan,
            cwd=worktree,
            required=required_plan_fragments(future) + ['--draft'],
        )
        scenario_results.append((f'future release plan ({future})', ok))
        overall_ok &= ok
        ok, _ = scenario(
            label=f'future release publish-plan ({future})',
            cmd=future_plan_publish,
            cwd=worktree,
            required=required_plan_fragments(future),
            forbidden=['--draft'],
        )
        scenario_results.append((f'future release publish-plan ({future})', ok))
        overall_ok &= ok
    finally:
        subprocess.run(['git', 'worktree', 'remove', '--force', str(worktree)], cwd=str(ROOT), capture_output=True, text=True)
        shutil.rmtree(temp_root, ignore_errors=True)

    passed = sum(1 for _, ok in scenario_results if ok)
    failed = len(scenario_results) - passed
    print('\n## Scenario summary')
    print(f'- passed: {passed}')
    print(f'- failed: {failed}')

    write_github_step_summary(
        latest=latest,
        future=future,
        results=scenario_results,
    )

    print('\n## 결과')
    if overall_ok:
        print('✅ release helper smoke checks를 통과했습니다.')
        print('다음 단계: CI에서 같은 스크립트를 실행하거나 release_helper.py publish 전 사전 점검으로 사용하세요.')
        return 0

    print('❌ release helper smoke checks에 실패한 항목이 있습니다. 위 로그를 확인하세요.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
