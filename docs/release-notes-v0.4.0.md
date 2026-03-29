## v0.4.0

이번 릴리스는 `v0.3.0` 이후 진행된 **회귀 검증 자동화**, **packaged plugin parity 확장**, **evaluator 출력 표준화**, **goal-research-loop 안정화**, **local plugin UI verification 흐름 추가**를 한 번에 묶습니다.

### Highlights

- Added regression automation for release / install / goal-research-loop
  - `scripts/run_release_smoke_checks.py`
  - `scripts/run_global_install_smoke_checks.py`
  - `scripts/run_goal_research_loop_regression.py`
- Expanded packaged plugin parity
  - single-skill → multi-skill
  - README / optional assets / screenshots parity
- Standardized evaluator-native outputs
  - shared evaluator output contract
  - machine summary schemas / `--json-out`
  - deterministic formatter/scripts for key evaluator skills
- Hardened `goal-research-loop`
  - `reconcile`
  - `resume`
  - runtime status and regression checks
- Added semi-automated local plugin UI verification
  - `scripts/run_local_plugin_ui_checks.py`

### User-visible improvements

- plugin / install / release regressions가 CI에서 더 빨리 드러납니다.
- packaged plugin metadata와 source skill metadata가 더 일관되게 유지됩니다.
- evaluator-native skill 결과를 사람과 자동화가 함께 읽기 쉬워졌습니다.
- `goal-research-loop` interrupted run을 더 안전하게 이어받을 수 있습니다.
- local plugin catalog/detail panel 점검이 report 기반으로 더 구조화됩니다.

### Recommended validation

```bash
python3 scripts/run_release_smoke_checks.py --skip-gh-auth
python3 scripts/run_global_install_smoke_checks.py
python3 scripts/run_goal_research_loop_regression.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 scripts/run_local_plugin_ui_checks.py --strict
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```
