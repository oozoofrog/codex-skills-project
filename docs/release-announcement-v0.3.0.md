# v0.3.0 발표문 초안

`codex-skills-project` **v0.3.0**을 배포했습니다.

이번 릴리스의 핵심은 저장소를 단순한 skill 모음에서 한 단계 더 밀어,  
**반복 연구 루프**, **전역 설치 검증 강화**, **review harness / packaged plugin parity 검사 강화**,  
그리고 **docs-first release helper**까지 포함한 운영 체계로 확장한 점입니다.

## 무엇이 달라졌나

- `goal-research-loop` 스킬과 Codex CLI runner를 추가했습니다.
- `install_global_skills.py --dry-run`이 populated `~/.codex/skills`에서도 안전하게 계획 전용으로 동작합니다.
- `--validate-installed`로 전역 설치 결과의 frontmatter / alias / dependency를 직접 검증할 수 있습니다.
- `codex-skill-audit`가 review harness / evaluation loop 계약을 더 깊게 검사합니다.
- `plugin-doctor`가 packaged skill / plugin manifest drift를 source skill metadata와 비교해 탐지합니다.
- `scripts/release_helper.py`와 `docs/release-workflow.md`를 추가해 changelog / release notes / tag / GitHub Release 흐름을 반복 가능한 명령으로 정리했습니다.

## 왜 중요한가

이번 변화로 이 저장소는:

- 스킬을 **추가하는 저장소**를 넘어서
- 스킬을 **검증하고**, **packaged layer까지 일치시키고**,
- 장기 실험을 **반복 가능한 구조**로 운영하며,
- 릴리스까지 **dry-run부터 통제 가능하게 준비하는 저장소**

로 더 선명해졌습니다.

즉, 문서/메타데이터/packaging/release가 각각 따로 노는 것이 아니라  
**같은 evidence-first 운영 모델** 안에서 연결되도록 정리한 릴리스입니다.

## 포함된 핵심 변화

- `goal-research-loop`
- global install validation 강화 (`--dry-run`, `--validate-installed`)
- review harness / evaluation loop audit 강화
- packaged plugin parity 검사 강화
- docs-first release helper 추가

## 검증

```bash
python3 scripts/install_global_skills.py --dry-run
python3 scripts/install_global_skills.py --validate-installed
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/release_helper.py check --version v0.3.0
python3 scripts/release_helper.py plan --version v0.3.0
```

## 링크

- Release: https://github.com/oozoofrog/codex-skills-project/releases/tag/v0.3.0
- Release notes: `docs/release-notes-v0.3.0.md`
- CHANGELOG: `CHANGELOG.md`
