## v0.3.0

이번 릴리스는 `v0.2.1` 이후 추가된 **goal-directed research**, **전역 설치 검증 강화**, **review harness / packaged plugin parity audit 강화**, 그리고 **docs-first release helper**를 한 버전으로 묶습니다.

### Highlights

- Added `goal-research-loop`
  - objective / contract / ledger / snapshot 기반의 bounded research loop
  - bundled Codex CLI runner:
    - `scripts/goal-research-loop.sh`
    - `scripts/codex_goal_research_loop.py`
- Strengthened global install validation
  - `install_global_skills.py --dry-run` is now safe on populated `~/.codex/skills`
  - new `--validate-installed` verifies frontmatter, alias, and dependency presence
- Deepened review-harness and evaluation-loop audit checks
  - stronger semantic checks in `codex-skill-audit`
  - stronger packaged/source drift checks in `plugin-doctor`
- Added docs-first release automation
  - `scripts/release_helper.py`
  - `docs/release-workflow.md`

### User-visible improvements

- 전역 스킬 설치 후 실제 설치 상태를 직접 점검할 수 있습니다.
- packaged plugin 레이어가 source skill metadata와 더 일관되게 유지됩니다.
- 장기 실험/가설 검증 워크플로를 저장소 안에서 반복 가능하게 운영할 수 있습니다.
- changelog / release notes / tag / GitHub Release를 dry-run부터 반복 가능한 명령으로 준비할 수 있습니다.

### Recommended validation

```bash
python3 scripts/install_global_skills.py --dry-run
python3 scripts/install_global_skills.py --validate-installed
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/release_helper.py check --version v0.3.0
python3 scripts/release_helper.py plan --version v0.3.0
```
