## v0.2.0

이번 릴리스는 저장소를 단순한 Codex skill 모음에서, **평가와 자동 진행까지 명시된 운영 모델**로 확장합니다.

### 주요 변경

- 전역 Codex 스킬 설치 흐름을 더 명확히 정리했습니다.
- repo-wide `Review Harness` 규약을 도입했습니다.
- Anthropic의 *Harness design for long-running application development* 글을 바탕으로 평가 루프 표준안을 추가했습니다.
- 각 스킬에 대해 **평가축 / 증거 / 자동 다음 행동** 매트릭스를 문서화했습니다.
- `agents/openai.yaml` 작성 규칙과 audit 검사를 강화했습니다.
- packaged plugins와 marketplace metadata를 review/evidence 모델에 맞춰 동기화했습니다.

### 포함된 새 문서

- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`
- `docs/openai-yaml-conventions.md`
- `docs/evaluation-loop-standard.md`
- `docs/evaluation-loop-skill-matrix.md`
- `CHANGELOG.md`

### 검증

```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```

요약:
- skill audit findings 0
- plugin-doctor findings 0
- packaged plugins 7개 재생성 완료
- JSON / asset / manifest path 검증 통과
