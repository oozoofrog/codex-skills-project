# CHANGELOG

이 문서는 이 저장소의 사용자 관점 변화와 릴리스 포인트를 기록합니다.

## v0.3.0 — 2026-03-29

관련 문서:

- release notes: `docs/release-notes-v0.3.0.md`
- roadmap: `docs/roadmap-v0.3.0.md`
- release workflow: `docs/release-workflow.md`

### 핵심 변경

- `goal-research-loop` 스킬과 Codex CLI runner를 추가해 objective 기반 반복 연구 루프를 지원합니다.
- 전역 설치 핵심 경로에서 `install_global_skills.py --dry-run`이 populated `~/.codex/skills`에서도 계획 전용으로 동작하도록 개선했습니다.
- `--validate-installed`를 추가해 전역 설치 결과의 frontmatter / alias / dependency 상태를 직접 검증할 수 있게 했습니다.
- `codex-skill-audit`가 review harness / evaluation loop 계약을 더 깊게 감사하도록 확장되었습니다.
- `plugin-doctor`가 packaged skill / plugin manifest drift를 source skill metadata와 비교해 탐지하도록 강화되었습니다.
- docs-first `scripts/release_helper.py`와 `docs/release-workflow.md`를 추가해 changelog / release notes / tag / GitHub Release 흐름을 반복 가능한 명령으로 정리했습니다.

### 새 스킬 및 운영 모델

- `goal-research-loop`
  - contract / snapshot / ledger / rounds 구조를 유지하는 script-first research loop 지원
  - `scripts/goal-research-loop.sh`
  - `scripts/codex_goal_research_loop.py`
- operator-facing skill guidance와 routing 문서를 보강해 explicit-only / script-first / review-harness 경계를 더 명확히 했습니다.

### 설치 및 검증 개선

- `scripts/install_global_skills.py`
  - non-mutating `--dry-run`
  - `--validate-installed`
  - install plan 상태 메모 출력
- README와 유지보수 smoke check 예시를 실제 전역 설치 검증 흐름과 맞췄습니다.

### audit / packaged plugin 개선

- `codex-skill-audit`
  - `평가축`, `자동 다음 행동`, `mode`와 설명/metadata 정합성 검사 강화
- `plugin-doctor`
  - packaged `SKILL.md` Review Harness drift 탐지
  - packaged `agents/openai.yaml` drift 탐지
  - single-skill plugin manifest metadata drift 탐지
- `scripts/sync_packaged_plugins.py`
  - single-skill plugin manifest metadata를 source `openai.yaml` 기준으로 재동기화

### 릴리스 준비 및 문서

- `docs/release-workflow.md`
- `scripts/release_helper.py`
- `docs/release-notes-v0.3.0.md`

### 검증에 사용한 명령

```bash
python3 scripts/install_global_skills.py --dry-run
python3 scripts/install_global_skills.py --validate-installed
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/release_helper.py check --version v0.3.0
python3 scripts/release_helper.py plan --version v0.3.0
```

## v0.2.1 — 2026-03-28

### 핵심 변경

- `v0.2.0` 이후 추가된 발표/로드맵 문서를 정리했습니다.
- README의 릴리스 링크를 최신 릴리스 기준으로 보강했습니다.
- `v0.3.0` 후보 작업을 별도 문서로 정리했습니다.
- `v0.2.0` 발표문 초안을 저장소 안에 남겼습니다.

### 추가된 문서

- `docs/release-announcement-v0.2.0.md`
- `docs/roadmap-v0.3.0.md`

### 링크 보강

- `README.md`에 latest release, changelog, release notes, roadmap 링크를 추가했습니다.

### 검증에 사용한 명령

```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

## v0.2.0 — 2026-03-28

관련 문서:

- release notes: `docs/release-notes-v0.2.0.md`
- announcement draft: `docs/release-announcement-v0.2.0.md`
- release prep: `docs/release-prep-v0.2.0.md`

### 핵심 변경

- 전역 Codex 스킬 설치 흐름을 더 명확히 정리했습니다.
- repo-wide `Review Harness` 규약을 도입했습니다.
- Anthropic의 *Harness design for long-running application development* 글을 바탕으로 평가 루프 표준안을 추가했습니다.
- 각 스킬에 대해 **평가축 / 증거 / 자동 다음 행동** 기준을 문서화했습니다.
- `agents/openai.yaml` 작성 규칙과 audit 검사를 강화했습니다.
- packaged plugins와 marketplace metadata를 새로운 review/evidence 모델에 맞춰 동기화했습니다.

### 추가된 문서

- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`
- `docs/openai-yaml-conventions.md`
- `docs/evaluation-loop-standard.md`
- `docs/evaluation-loop-skill-matrix.md`
- `docs/release-prep-v0.2.0.md`

### 운영 측면 개선

- 각 `SKILL.md`의 `Review Harness` 섹션을 더 구체화했습니다.
- `hey-codex`의 explicit-only 성격을 metadata와 packaged plugin 레이어까지 일치시켰습니다.
- skill audit / plugin-doctor 기준으로 review harness 정합성까지 검사하게 했습니다.

### 검증에 사용한 명령

```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```

## v0.1.0 — 2026-03-27

초기 공개 릴리스.

포함 내용:

- `.agents/skills/` 기반 repo-local Codex skills
- `.codex/agents/` 기반 custom agents
- `plugins/` 기반 local packaged plugins
- `.agents/plugins/marketplace.json`
- smoke test / packaging scripts
- generated preview/browser/live capture assets
- issue / PR templates와 MIT license
