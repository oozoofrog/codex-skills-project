# plugins

이 디렉토리는 `.agents/skills/`에서 파생된 **로컬 배포/설치 테스트용 Codex plugin 패키지 레이어**입니다.

## 갱신 방법

```bash
python3 scripts/sync_packaged_plugins.py
```

## 로컬 마켓플레이스

- repo marketplace: `.agents/plugins/marketplace.json`
- plugin roots: `./plugins/<plugin-name>`
- smoke test guide: `docs/local-plugin-testing.md`
- static smoke script: `python3 scripts/run_local_plugin_smoke_checks.py`
- load assistant: `python3 scripts/run_local_plugin_load_assistant.py`

Codex plugin 문서 기준으로 `source.path`는 marketplace root 기준 상대 경로여야 하므로, 현재 저장소에서는 `./plugins/<plugin-name>` 형태를 사용합니다.
