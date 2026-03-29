# Local Codex Plugin Testing Guide

이 문서는 현재 저장소의 **repo-local marketplace + packaged plugins**를 점검하는 절차를
두 가지 흐름으로 나눠 설명합니다.

- **빠른 확인**: 처음 해보는 사람, 또는 변경 직후 최소 확인만 하고 싶을 때
- **유지보수 전체 절차**: plugin metadata / packaged assets / smoke check까지 전부 다시 볼 때

---

## 1. 빠른 확인

가장 자주 쓰는 순서는 아래 4단계입니다.

```bash
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/run_local_plugin_ui_checks.py --write-report
python3 scripts/run_local_plugin_load_assistant.py --run-smoke --run-ui-checks
```

그 다음:

1. **Codex를 현재 저장소 루트에서 다시 시작**
2. 로컬 plugin catalog에서 plugin이 보이는지 확인
3. 원하는 plugin 하나에서 starter prompt 1개 실행

### 빠른 확인에서 꼭 보는 것

- `.agents/plugins/marketplace.json`이 현재 packaged plugins와 맞는지
- `plugins/*/.codex-plugin/plugin.json` 경로 참조가 깨지지 않았는지
- packaged assets가 모두 존재하는지
- `reports/local-plugin-ui-report-*.md`에 UI 기대 상태가 정리됐는지
- Codex UI에서 실제로 plugin이 로드되는지

### 빠른 확인용 starter prompts

- `agent-context`
  - “이 저장소의 AGENTS.md 구조를 제안해줘”
- `app-automation`
  - “부팅된 시뮬레이터 목록을 보여줘”
- `apple-craft`
  - “SwiftUI 뷰 빌드 에러 원인 분석해줘”
- `gpt-research`
  - “이 디렉토리를 외부 GPT 리서치용 프롬프트로 정리해줘”
- `hey-codex`
  - “별도 Codex CLI로 세컨드 오피니언 받아와”
- `macos-release`
  - “이 프로젝트 릴리스 준비 상태를 점검해줘”
- `plugin-doctor`
  - “이 저장소의 plugin/skill 구조를 감사해줘”

---

## 2. 유지보수 전체 절차

아래는 packaged plugin / marketplace / assets / 로컬 로딩까지 전부 다시 보는 흐름입니다.

### Step 1. packaged plugin 재생성

```bash
python3 scripts/sync_packaged_plugins.py
```

언제 실행하나:

- `.agents/skills/` 내용이 바뀌었을 때
- plugin manifest 메타데이터를 바꿨을 때
- assets를 다시 만들었을 때
- browser/live capture를 반영했을 때

### Step 2. 정적 검증

가장 쉬운 기본 명령:

```bash
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/run_local_plugin_ui_checks.py --write-report
```

필요하면 개별 검증도 돌립니다.

```bash
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

무엇을 확인하나:

- JSON 파싱
- manifest path validity
- packaged assets 존재 여부
- plugin-doctor / skill-audit findings

### Step 3. 로컬 로딩 체크리스트 생성

```bash
python3 scripts/run_local_plugin_load_assistant.py --run-smoke --run-ui-checks
```

이 스크립트는:

- 정적 smoke check를 한 번 더 돌리고
- UI verification report도 생성하고
- `reports/local-plugin-load-checklist-*.md`를 생성해
- 실제 UI 확인 순서를 정리해 줍니다.

### Step 3a. UI verification report만 따로 생성

```bash
python3 scripts/run_local_plugin_ui_checks.py --write-report
```

이 스크립트는 plugin별로 아래 기대 상태를 정리합니다.

- display name
- category
- icon / logo / screenshots 경로
- screenshot 개수
- starter prompt 개수와 예시 prompt
- 수동 UI 체크리스트

### Step 4. Codex UI 로딩 확인

1. Codex를 **현재 저장소 루트에서 다시 시작**
2. repo-level instruction과 skill discovery가 정상인지 확인
3. local plugin catalog를 다시 읽게 함
4. `Codex Skills Local` 또는 동등한 로컬 plugin 목록에서 plugin이 보이는지 확인

### Step 5. plugin별 최소 실행 확인

각 plugin에 대해 starter prompt 1개 이상 실행합니다.

중점:

- catalog에 실제로 노출되는지
- detail panel의 아이콘/로고/스크린샷이 보이는지
- 첫 prompt가 의도대로 시작되는지

---

## 3. assets / capture 갱신

### browser capture 반영

```bash
python3 scripts/update_browser_capture_assets.py <plugin-name> /path/to/browser-capture.png
python3 scripts/sync_packaged_plugins.py
```

### live capture 반영

```bash
python3 scripts/update_live_capture_assets.py /path/to/codex-live-capture.png
python3 scripts/sync_packaged_plugins.py
```

### assets에서 꼭 보는 것

- `assets/icon.svg`, `assets/icon.png`
- `assets/logo.svg`, `assets/logo.png`
- `assets/screenshot.svg`, `assets/screenshot.png`
- optional:
  - `assets/browser-capture.png`
  - `assets/live-capture.png`

또한 `.codex-plugin/plugin.json`의 아래 필드가 실제 파일과 맞는지 확인합니다.

- `interface.composerIcon`
- `interface.logo`
- `interface.screenshots[]`

---

## 4. 언제 다시 점검해야 하나

다음 변경 후에는 최소한 **빠른 확인**, 가능하면 **유지보수 전체 절차**를 다시 실행합니다.

- plugin 이름 변경
- packaged plugin 추가/삭제
- marketplace entry 순서 변경
- plugin manifest의 `skills`, `mcpServers`, `interface` 수정
- skill 경로 구조 변경
- browser/live capture 추가 또는 교체

---

## 5. 유지보수용 추천 명령 순서

```bash
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py
python3 scripts/run_local_plugin_ui_checks.py --write-report
python3 scripts/run_local_plugin_load_assistant.py --run-smoke --run-ui-checks
```

그 다음 Codex를 재시작하고, generated checklist를 따라 UI에서 수동 확인합니다.

---

## 6. 관련 파일

- `scripts/sync_packaged_plugins.py`
- `scripts/run_local_plugin_smoke_checks.py`
- `scripts/run_local_plugin_ui_checks.py`
- `scripts/run_local_plugin_load_assistant.py`
- `plugins/README.md`
- `.agents/plugins/marketplace.json`
