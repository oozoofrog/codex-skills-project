## Summary
- repo-wide `Review Harness` 규약을 유지한 상태로 packaged plugins를 다시 동기화했습니다.
- `agents/openai.yaml`의 stricter 작성 규칙을 `docs/openai-yaml-conventions.md`로 분리했습니다.
- local marketplace / packaged plugin metadata를 review/evidence 중심 설명으로 보강했습니다.
- `hey-codex`의 explicit-only 의도를 packaged metadata에도 반영했습니다.

## Checklist
- [x] `python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate` 실행
- [x] 필요한 경우 `python3 scripts/sync_packaged_plugins.py` 재실행
- [x] skill / plugin metadata 변경 시 관련 문서도 함께 갱신
- [x] 스크린샷/asset 변경 시 결과를 직접 확인

## Scope
- [x] `.agents/skills`
- [ ] `.codex/agents`
- [x] `plugins/*`
- [x] `.agents/plugins/marketplace.json`
- [x] `docs/`
- [x] `scripts/`

## Validation

```bash
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

결과 요약:
- packaged plugins 7개 재생성 완료
- plugin-doctor 감사 findings 0
- skill audit findings 0
- JSON / asset / manifest 경로 검증 통과

## Notes
- `docs/openai-yaml-conventions.md`를 새 source of truth로 추가했습니다.
- `scripts/sync_packaged_plugins.py`의 plugin metadata 문구와 버전을 함께 갱신했습니다.
- packaged plugin assets는 metadata 문구 변경에 따라 대표 SVG/PNG preview가 재생성되었습니다.
