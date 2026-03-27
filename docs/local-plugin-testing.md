# Local Codex Plugin Testing Guide

이 문서는 현재 저장소의 **repo-local marketplace + local packaged plugins**를 점검하는 절차입니다.

## 1. 패키지 재생성

```bash
python3 scripts/sync_packaged_plugins.py
```

언제 실행하나:
- `.agents/skills/`의 내용이 바뀌었을 때
- plugin manifest 메타데이터를 바꿨을 때
- assets를 다시 만들었을 때

## 2. 정적 검증

### 원클릭 스모크 체크
```bash
python3 scripts/run_local_plugin_smoke_checks.py
```


### plugin 구조 감사
```bash
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```

### skill 구조 감사
```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

### JSON 파싱 스모크 체크
```bash
python3 - <<'PY'
import json
from pathlib import Path
paths=[Path('.agents/plugins/marketplace.json')] + sorted(Path('plugins').glob('*/.codex-plugin/plugin.json')) + sorted(Path('plugins').glob('*/.mcp.json'))
for p in paths:
    json.loads(p.read_text())
    print('OK', p)
PY
```

## 3. Codex 로컬 로딩 확인

### 로딩 확인 보조 체크리스트 생성
```bash
python3 scripts/run_local_plugin_load_assistant.py --run-smoke
```

1. Codex를 현재 저장소 루트에서 다시 시작한다.
2. repo-level instruction과 skill discovery가 정상인지 확인한다.
3. local plugin catalog를 다시 읽게 한다.
4. `Codex Skills Local` 카탈로그 또는 동등한 로컬 plugin 목록에서 plugin이 보이는지 확인한다.

## 4. 설치/활성화 스모크 테스트

각 plugin에 대해 최소 1개 프롬프트를 실행한다.

### agent-context
- “이 저장소의 AGENTS.md 구조를 제안해줘”

### app-automation
- “부팅된 시뮬레이터 목록을 보여줘”
- 필요 시 baepsae 연결 확인

### apple-craft
- “SwiftUI 뷰 빌드 에러 원인 분석해줘”

### gpt-research
- “이 디렉토리를 외부 GPT 리서치용 프롬프트로 정리해줘”

### hey-codex
- “별도 Codex CLI로 세컨드 오피니언 받아와”

### macos-release
- “이 프로젝트 릴리스 준비 상태를 점검해줘”

### plugin-doctor
- “이 저장소의 plugin/skill 구조를 감사해줘”

## 5. Assets 점검

각 packaged plugin에 대해 다음 파일이 존재하는지 확인한다.

- `assets/icon.svg`
- `assets/logo.svg`
- `assets/screenshot.svg`

또한 `.codex-plugin/plugin.json`의 `interface.composerIcon`, `logo`, `screenshots[]`가 실제 파일과 일치하는지 확인한다.

### 외부 브라우저 캡처 반영

외부 브라우저에서 plugin detail/gallery를 캡처했다면 다음 명령으로 shared browser capture로 반영한다.

```bash
python3 scripts/update_browser_capture_assets.py <plugin-name> /path/to/browser-capture.png
python3 scripts/sync_packaged_plugins.py
```

## 6. 회귀 체크 포인트

다음 변경 후에는 반드시 다시 점검한다.

- plugin 이름 변경
- packaged plugin 추가/삭제
- marketplace entry 순서 변경
- plugin manifest의 `skills`, `mcpServers`, `interface` 수정
- skill 경로 구조 변경

## 7. 권장 순서

```bash
python3 scripts/sync_packaged_plugins.py
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

그다음 Codex를 재시작하고 로컬 로딩을 수동 확인한다.


## 8. Live capture 교체

```bash
python3 scripts/update_live_capture_assets.py /path/to/codex-live-capture.png
python3 scripts/sync_packaged_plugins.py
```
