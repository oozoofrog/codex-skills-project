## Summary
- 변경 내용을 짧게 설명해주세요.

## Checklist
- [ ] `python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate` 실행
- [ ] 필요한 경우 `python3 scripts/sync_packaged_plugins.py` 재실행
- [ ] skill / plugin metadata 변경 시 관련 문서도 함께 갱신
- [ ] 스크린샷/asset 변경 시 결과를 직접 확인

## Scope
- [ ] `.agents/skills`
- [ ] `.codex/agents`
- [ ] `plugins/*`
- [ ] `.agents/plugins/marketplace.json`
- [ ] `docs/`
- [ ] `scripts/`

## Validation
실행한 검증 절차와 결과를 적어주세요.

```bash
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
```

## Screenshots / Notes
UI, assets, live capture 관련 변경이면 첨부해주세요.
