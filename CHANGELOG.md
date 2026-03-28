# CHANGELOG

이 문서는 이 저장소의 사용자 관점 변화와 릴리스 포인트를 기록합니다.

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
