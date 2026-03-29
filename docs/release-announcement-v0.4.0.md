# v0.4.0 발표문

`codex-skills-project` **v0.4.0**은 저장소의 핵심 운영 흐름을
**더 자동화되고, 더 재현 가능하며, 더 기계적으로 검증 가능한 상태**로 끌어올리는 릴리스입니다.

## 무엇이 달라졌나

- release / install / goal-research-loop regression이 CI에서 자동 검증됩니다.
- packaged plugin parity가 multi-skill / README / optional asset 수준까지 확장되었습니다.
- evaluator-native skill 출력이 공통 contract와 machine summary schema 기반으로 정리되었습니다.
- `goal-research-loop`는 `reconcile`, `resume`, runtime status를 갖춘 더 안정적인 runner가 되었습니다.
- local plugin testing은 quick path / maintenance path / UI verification report 흐름으로 정리되었습니다.

## 왜 중요한가

이번 릴리스로 이 저장소는 단순히 skill을 모아 두는 공간이 아니라,

- release가 깨지지 않는지,
- install이 regress되지 않는지,
- packaged/source가 drift하지 않는지,
- evaluator 결과가 구조화되는지,
- 장기 research loop가 안전하게 이어지는지

를 모두 **반복 가능한 검사 레일 위**에서 운영할 수 있게 됩니다.

## 포함된 핵심 변화

- release helper smoke / install smoke / goal-research-loop smoke CI
- packaged plugin multi-skill parity
- evaluator output contract + formatter/schema
- goal-research-loop resume/reconcile/runtime status
- local plugin UI verification report

## 링크

- Release: https://github.com/oozoofrog/codex-skills-project/releases/tag/v0.4.0
- Release notes: `docs/release-notes-v0.4.0.md`
- CHANGELOG: `CHANGELOG.md`

## 검증

```bash
python3 scripts/run_release_smoke_checks.py --skip-gh-auth
python3 scripts/run_global_install_smoke_checks.py
python3 scripts/run_goal_research_loop_regression.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 scripts/run_local_plugin_ui_checks.py --strict
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```
