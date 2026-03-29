#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def execute(cmd: list[str], *, cwd: Path = ROOT) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    output = (proc.stdout or '') + (proc.stderr or '')
    return proc.returncode, output


def print_result(label: str, output: str, ok: bool) -> None:
    prefix = '✅' if ok else '❌'
    print(f'{prefix} {label}')
    if output.strip():
        print(output.strip())


def validate_output(
    *,
    label: str,
    output: str,
    required: list[str],
    forbidden: list[str] | None = None,
) -> bool:
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
        return False

    print(f'✅ {label} 출력 계약 검증 통과')
    return True


def scenario(
    *,
    label: str,
    cmd: list[str],
    required: list[str],
    expect_code: int = 0,
    forbidden: list[str] | None = None,
) -> tuple[bool, str]:
    code, output = execute(cmd)
    ok = code == expect_code
    print_result(label, output, ok)
    if not ok:
        print(f'  - expected exit code: {expect_code}, actual: {code}')
        return False, output
    return validate_output(label=label, output=output, required=required, forbidden=forbidden), output


def write_summary(*, passed: int, failed: int, selected_install_root: Path) -> None:
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return
    log_path = os.environ.get('INSTALL_SMOKE_LOG_PATH')
    lines = [
        '## install-smoke',
        '',
        '- command: `python3 scripts/run_global_install_smoke_checks.py`',
        f'- install fixture root: `{selected_install_root}`',
        f'- passed: `{passed}`',
        f'- failed: `{failed}`',
    ]
    if log_path:
        lines.append(f'- log path: `{log_path}`')
    Path(summary_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    print('# Global Install Smoke Checks')
    print(f'Root: {ROOT}')

    overall_ok = True
    results: list[tuple[str, bool]] = []

    compile_code, compile_output = execute(['python3', '-m', 'py_compile', 'scripts/install_global_skills.py'])
    compile_ok = compile_code == 0
    print_result('Python compile', compile_output, compile_ok)
    overall_ok &= compile_ok

    temp_root = Path(tempfile.mkdtemp(prefix='install-smoke-'))
    dry_dest = temp_root / 'dry-run-install'
    install_dest = temp_root / 'installed-skills'
    broken_dest = temp_root / 'broken-install'

    try:
        ok, _ = scenario(
            label='fresh dry-run',
            cmd=['python3', 'scripts/install_global_skills.py', '--dest', str(dry_dest), '--dry-run'],
            required=[
                '# Global skill install plan',
                '- dry-run: True',
                '[new]',
                '드라이런 완료: 실제 파일 변경은 없었습니다.',
            ],
        )
        results.append(('fresh dry-run', ok))
        overall_ok &= ok
        if dry_dest.exists():
            print('❌ fresh dry-run 부작용: dry-run destination이 생성되었습니다.')
            overall_ok = False
        else:
            print('✅ fresh dry-run side-effect 검증 통과')

        ok, _ = scenario(
            label='targeted install with alias and dependency',
            cmd=[
                'python3',
                'scripts/install_global_skills.py',
                'plugin-doctor',
                'macos-release',
                '--dest',
                str(install_dest),
                '--mode',
                'copy',
                '--overwrite',
            ],
            required=[
                '- selected: codex-skill-audit, ooz-macos-release, plugin-doctor',
                '[alias: macos-release]',
                '[deps: codex-skill-audit]',
                '설치 완료. Codex를 재시작해서 새 전역 스킬을 다시 로드하세요.',
            ],
        )
        results.append(('targeted install with alias and dependency', ok))
        overall_ok &= ok

        ok, _ = scenario(
            label='validate installed tree',
            cmd=[
                'python3',
                'scripts/install_global_skills.py',
                'plugin-doctor',
                'macos-release',
                '--dest',
                str(install_dest),
                '--validate-installed',
            ],
            required=[
                '# Installed skill validation',
                'alias: macos-release -> ooz-macos-release',
                'deps: codex-skill-audit',
                '설치 검증 완료.',
            ],
        )
        results.append(('validate installed tree', ok))
        overall_ok &= ok

        ok, _ = scenario(
            label='dry-run on populated install tree',
            cmd=[
                'python3',
                'scripts/install_global_skills.py',
                'plugin-doctor',
                'macos-release',
                '--dest',
                str(install_dest),
                '--dry-run',
            ],
            required=[
                'exists; dry-run only, real install needs --overwrite',
                '드라이런 완료: 실제 파일 변경은 없었습니다.',
            ],
        )
        results.append(('dry-run on populated install tree', ok))
        overall_ok &= ok

        ok, _ = scenario(
            label='dry-run with overwrite on populated install tree',
            cmd=[
                'python3',
                'scripts/install_global_skills.py',
                'plugin-doctor',
                'macos-release',
                '--dest',
                str(install_dest),
                '--dry-run',
                '--overwrite',
            ],
            required=[
                'exists; dry-run would replace',
                '드라이런 완료: 실제 파일 변경은 없었습니다.',
            ],
        )
        results.append(('dry-run with overwrite on populated install tree', ok))
        overall_ok &= ok

        shutil.copytree(install_dest, broken_dest)
        shutil.rmtree(broken_dest / 'codex-skill-audit')

        ok, _ = scenario(
            label='broken install validation failure',
            cmd=[
                'python3',
                'scripts/install_global_skills.py',
                'plugin-doctor',
                '--dest',
                str(broken_dest),
                '--validate-installed',
            ],
            expect_code=1,
            required=[
                'dependency 누락: plugin-doctor requires codex-skill-audit',
                '설치 검증 실패:',
            ],
        )
        results.append(('broken install validation failure', ok))
        overall_ok &= ok
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    passed = sum(1 for _, ok in results if ok)
    failed = len(results) - passed
    print('\n## Scenario summary')
    print(f'- passed: {passed}')
    print(f'- failed: {failed}')

    write_summary(
        passed=passed,
        failed=failed,
        selected_install_root=install_dest,
    )

    print('\n## 결과')
    if overall_ok:
        print('✅ global install smoke checks를 통과했습니다.')
        print('다음 단계: CI에서 같은 스크립트를 실행하거나 install_global_skills.py 변경 전후 회귀 검증으로 사용하세요.')
        return 0

    print('❌ global install smoke checks에 실패한 항목이 있습니다. 위 로그를 확인하세요.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
