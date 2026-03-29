#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], label: str, *, cwd: Path = ROOT) -> tuple[bool, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    output = (proc.stdout or '') + (proc.stderr or '')
    ok = proc.returncode == 0
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


def main() -> int:
    parser = argparse.ArgumentParser(description='Run smoke checks for scripts/release_helper.py')
    parser.add_argument('--skip-gh-auth', action='store_true', help='release_helper.py 실행 시 --skip-gh-auth를 전달합니다.')
    args = parser.parse_args()

    overall_ok = True

    print('# Release Helper Smoke Checks')
    print(f'Root: {ROOT}')

    ok, _ = run(['python3', '-m', 'py_compile', 'scripts/release_helper.py'], 'Python compile')
    overall_ok &= ok

    latest = latest_tag()
    latest_check = ['python3', 'scripts/release_helper.py', 'check', '--version', latest, '--allow-existing-tag', '--allow-dirty']
    latest_plan = ['python3', 'scripts/release_helper.py', 'plan', '--version', latest, '--allow-existing-tag', '--allow-dirty']
    if args.skip_gh_auth:
        latest_check.append('--skip-gh-auth')
        latest_plan.append('--skip-gh-auth')

    ok, _ = run(latest_check, f'current release check ({latest})')
    overall_ok &= ok
    ok, _ = run(latest_plan, f'current release plan ({latest})')
    overall_ok &= ok

    temp_root = Path(tempfile.mkdtemp(prefix='release-smoke-'))
    worktree = temp_root / 'worktree'
    try:
        git('worktree', 'add', '--detach', str(worktree), 'HEAD')
        future = next_patch(latest)
        seed_next_release_docs(worktree, future)

        future_check = ['python3', 'scripts/release_helper.py', 'check', '--version', future, '--allow-dirty']
        future_plan = ['python3', 'scripts/release_helper.py', 'plan', '--version', future, '--allow-dirty']
        if args.skip_gh_auth:
            future_check.append('--skip-gh-auth')
            future_plan.append('--skip-gh-auth')

        ok, _ = run(future_check, f'future release check ({future})', cwd=worktree)
        overall_ok &= ok
        ok, _ = run(future_plan, f'future release plan ({future})', cwd=worktree)
        overall_ok &= ok
    finally:
        subprocess.run(['git', 'worktree', 'remove', '--force', str(worktree)], cwd=str(ROOT), capture_output=True, text=True)
        shutil.rmtree(temp_root, ignore_errors=True)

    print('\n## 결과')
    if overall_ok:
        print('✅ release helper smoke checks를 통과했습니다.')
        print('다음 단계: CI에서 같은 스크립트를 실행하거나 release_helper.py publish 전 사전 점검으로 사용하세요.')
        return 0

    print('❌ release helper smoke checks에 실패한 항목이 있습니다. 위 로그를 확인하세요.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
