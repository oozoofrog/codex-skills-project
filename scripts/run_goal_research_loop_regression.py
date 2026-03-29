#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / '.agents' / 'skills' / 'goal-research-loop' / 'scripts' / 'codex_goal_research_loop.py'
WRAPPER = ROOT / '.agents' / 'skills' / 'goal-research-loop' / 'scripts' / 'goal-research-loop.sh'


def execute(cmd: list[str], *, cwd: Path = ROOT) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return proc.returncode, (proc.stdout or '') + (proc.stderr or '')


def print_result(label: str, output: str, ok: bool) -> None:
    prefix = '✅' if ok else '❌'
    print(f'{prefix} {label}')
    if output.strip():
        print(output.strip())


def write_summary(results: list[tuple[str, bool]]) -> None:
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return
    log_path = os.environ.get('GOAL_LOOP_SMOKE_LOG_PATH')
    passed = sum(1 for _, ok in results if ok)
    failed = len(results) - passed
    lines = [
        '## goal-research-loop-smoke',
        '',
        '- command: `python3 scripts/run_goal_research_loop_regression.py`',
        f'- passed: `{passed}`',
        f'- failed: `{failed}`',
    ]
    if log_path:
        lines.append(f'- log path: `{log_path}`')
    lines.extend(['', '| scenario | status |', '|---|---|'])
    for label, ok in results:
        lines.append(f'| {label} | {"✅ pass" if ok else "❌ fail"} |')
    Path(summary_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def fake_codex(path: Path, *, sleep_seconds: int = 0) -> Path:
    script = textwrap.dedent(
        f'''\
        #!/usr/bin/env python3
        import json
        import pathlib
        import re
        import sys
        import time

        args = sys.argv[1:]
        out_path = pathlib.Path(args[args.index('-o') + 1])
        prompt = sys.stdin.read()
        dump_path = out_path.with_suffix(out_path.suffix + '.prompt.txt')
        dump_path.write_text(prompt, encoding='utf-8')
        if {sleep_seconds}:
            time.sleep({sleep_seconds})
        m = re.search(r'Goal Research Loop Round (\\d+)', prompt)
        round_num = int(m.group(1)) if m else 0
        payload = {{
            "round": round_num,
            "objective": "fixture objective",
            "hypothesis": "fixture hypothesis",
            "change_summary": "fixture change",
            "hard_gates": {{"result": "pass", "details": "fixture pass"}},
            "metric": "fixture metric",
            "evidence_summary": "fixture evidence",
            "experiment_status": "keep",
            "control_action": "pass",
            "best_state_summary": "fixture best state",
            "next_step": "fixture done",
            "notes": "fixture notes",
            "updated_files": [],
            "evidence_files": []
        }}
        out_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        '''
    )
    path.write_text(script, encoding='utf-8')
    path.chmod(0o755)
    return path


def write_orphan_round(workspace: Path, *, round_num: int, pending: bool = False) -> Path:
    round_dir = workspace / '.goal-research-loop' / 'rounds' / f'round-{round_num:03d}'
    round_dir.mkdir(parents=True, exist_ok=True)
    if not pending:
        payload = {
            'round': round_num,
            'objective': 'resume test',
            'hypothesis': 'resume can reconcile',
            'change_summary': 'fixture',
            'hard_gates': {'result': 'pass', 'details': 'fixture'},
            'metric': 'stable',
            'evidence_summary': 'fixture evidence',
            'experiment_status': 'keep',
            'control_action': 'refine',
            'best_state_summary': 'state preserved',
            'next_step': 'continue',
            'notes': 'fixture row',
            'updated_files': [],
            'evidence_files': [],
        }
        (round_dir / 'last-message.json').write_text(json.dumps(payload), encoding='utf-8')
    return round_dir


def init_workspace(workspace: Path, objective: str) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    code, output = execute(['python3', str(RUNNER), 'init', '--workspace', str(workspace), '--objective', objective])
    if code != 0:
        raise RuntimeError(output)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def scenario_reconcile_and_status() -> tuple[bool, str]:
    tmp = Path(tempfile.mkdtemp(prefix='goal-loop-reconcile-'))
    try:
        init_workspace(tmp, 'runner reconcile test')
        write_orphan_round(tmp, round_num=0, pending=False)
        write_orphan_round(tmp, round_num=1, pending=True)
        code, output = execute(['python3', str(RUNNER), 'reconcile', '--workspace', str(tmp)])
        if code != 0:
            return False, output
        code, status_output = execute(['python3', str(RUNNER), 'status', '--workspace', str(tmp)])
        if code != 0:
            return False, output + '\n' + status_output
        ledger = (tmp / '.goal-research-loop' / 'ledger.tsv').read_text(encoding='utf-8')
        runtime = read_json(tmp / '.goal-research-loop' / 'runtime' / 'status.json')
        ok = (
            'reconciled rounds: [0]' in output
            and 'pending rounds: [1]' in output
            and 'pending rounds: [1]' in status_output
            and '(reconciled from round artifact)' in ledger
            and runtime['pending_rounds'] == [1]
            and runtime['next_round'] == 2
        )
        return ok, output + '\n' + status_output
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_resume_flow() -> tuple[bool, str]:
    tmp = Path(tempfile.mkdtemp(prefix='goal-loop-resume-'))
    try:
        init_workspace(tmp, 'resume flow test')
        write_orphan_round(tmp, round_num=0, pending=False)
        fake = fake_codex(tmp / 'fake-codex')
        code, output = execute([
            'bash',
            str(WRAPPER),
            'resume',
            str(tmp),
            '--codex-bin',
            str(fake),
            '--max-rounds',
            '1',
            '--allow-dirty',
        ])
        if code != 0:
            return False, output
        ledger_rows = (tmp / '.goal-research-loop' / 'ledger.tsv').read_text(encoding='utf-8').splitlines()
        round1_response = tmp / '.goal-research-loop' / 'rounds' / 'round-001' / 'response.json'
        ok = ('reconciled rounds before resume: [0]' in output and len(ledger_rows) == 3 and round1_response.exists())
        return ok, output
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_prompt_profiles() -> tuple[bool, str]:
    tmp = Path(tempfile.mkdtemp(prefix='goal-loop-profiles-'))
    try:
        fake = fake_codex(tmp / 'fake-codex')
        standard_ws = tmp / 'standard'
        lightweight_ws = tmp / 'lightweight'
        init_workspace(standard_ws, 'standard profile test')
        init_workspace(lightweight_ws, 'lightweight profile test')
        code1, out1 = execute([
            'python3', str(RUNNER), 'run', '--workspace', str(standard_ws), '--codex-bin', str(fake), '--max-rounds', '1', '--allow-dirty', '--prompt-profile', 'standard'
        ])
        code2, out2 = execute([
            'python3', str(RUNNER), 'run', '--workspace', str(lightweight_ws), '--codex-bin', str(fake), '--max-rounds', '1', '--allow-dirty', '--prompt-profile', 'lightweight'
        ])
        if code1 != 0 or code2 != 0:
            return False, out1 + '\n' + out2
        standard_prompt = (standard_ws / '.goal-research-loop' / 'rounds' / 'round-000' / 'prompt.md').read_text(encoding='utf-8')
        lightweight_prompt = (lightweight_ws / '.goal-research-loop' / 'rounds' / 'round-000' / 'prompt.md').read_text(encoding='utf-8')
        ok = (
            '이번 라운드는 standard prompt profile입니다.' in standard_prompt
            and 'references/fit-and-mode-routing.md' in standard_prompt
            and '이번 라운드는 lightweight prompt profile입니다.' in lightweight_prompt
            and 'references/fit-and-mode-routing.md' not in lightweight_prompt
            and 'references/decision-layers-and-status-mapping.md' in lightweight_prompt
        )
        return ok, out1 + '\n' + out2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def scenario_timeout_fallback() -> tuple[bool, str]:
    tmp = Path(tempfile.mkdtemp(prefix='goal-loop-timeout-'))
    try:
        init_workspace(tmp, 'timeout test')
        fake = fake_codex(tmp / 'slow-codex', sleep_seconds=2)
        code, output = execute([
            'python3', str(RUNNER), 'run', '--workspace', str(tmp), '--codex-bin', str(fake), '--max-rounds', '1', '--allow-dirty', '--timeout-seconds', '1'
        ])
        if code != 0:
            return False, output
        response = read_json(tmp / '.goal-research-loop' / 'rounds' / 'round-000' / 'response.json')
        ledger = (tmp / '.goal-research-loop' / 'ledger.tsv').read_text(encoding='utf-8')
        ok = (
            response['experiment_status'] == 'crash'
            and response['control_action'] == 'escalate'
            and 'timed out' in response['notes']
            and '\tcrash\tescalate\t' in ledger
        )
        return ok, output
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


SCENARIOS = [
    ('reconcile-and-status', scenario_reconcile_and_status),
    ('resume-flow', scenario_resume_flow),
    ('prompt-profiles', scenario_prompt_profiles),
    ('timeout-fallback', scenario_timeout_fallback),
]


def write_summary(results: list[tuple[str, bool]]) -> None:
    summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
    if not summary_path:
        return
    log_path = os.environ.get('GOAL_LOOP_REGRESSION_LOG_PATH')
    passed = sum(1 for _, ok in results if ok)
    failed = len(results) - passed
    lines = [
        '## goal-research-loop-regression',
        '',
        '- command: `python3 scripts/run_goal_research_loop_regression.py`',
        f'- passed: `{passed}`',
        f'- failed: `{failed}`',
    ]
    if log_path:
        lines.append(f'- log path: `{log_path}`')
    lines.extend(['', '| scenario | status |', '|---|---|'])
    for label, ok in results:
        lines.append(f'| {label} | {"✅ pass" if ok else "❌ fail"} |')
    Path(summary_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    print('# Goal Research Loop Regression')
    results = []
    overall_ok = True
    for label, fn in SCENARIOS:
        ok, output = fn()
        prefix = '✅' if ok else '❌'
        print(f'{prefix} {label}')
        if output.strip():
            print(output.strip())
        results.append((label, ok))
        overall_ok &= ok
    passed = sum(1 for _, ok in results if ok)
    failed = len(results) - passed
    print('\n## Scenario summary')
    print(f'- passed: {passed}')
    print(f'- failed: {failed}')
    write_summary(results)
    if overall_ok:
        print('\n✅ goal-research-loop regression checks를 통과했습니다.')
        raise SystemExit(0)
    print('\n❌ goal-research-loop regression checks에 실패한 항목이 있습니다.')
    raise SystemExit(1)
