# codex-skills-project

[![GitHub Repo](https://img.shields.io/badge/GitHub-oozoofrog/codex--skills--project-181717?logo=github)](https://github.com/oozoofrog/codex-skills-project)
[![Release](https://img.shields.io/github/v/release/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/issues)
[![Repo Size](https://img.shields.io/github/repo-size/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project)

`/Volumes/eyedisk/develop/oozoofrog/oozoofrog-plugins`를 **Codex 네이티브 작업공간**으로 이식한 저장소입니다.

핵심 원칙은 다음과 같습니다.

- **실행 포맷은 `.agents/skills`**
- **프로젝트 지침은 `AGENTS.md`**
- **Claude 전용 산출물(`CLAUDE.md`, `.claude-plugin`, plugin hooks)은 그대로 복제하지 않음**
- **원본 플러그인 에이전트는 필요 시 Codex 대응 구조(`.codex/agents`) 또는 skill references로 재구성**

## 공식 문서 기준

- Skills: https://developers.openai.com/codex/skills
- AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Plugins: https://developers.openai.com/codex/plugins
- Subagents: https://developers.openai.com/codex/subagents

## 현재 구조

```text
codex-skills-project/
├── AGENTS.md
├── README.md
├── .agents/
│   └── skills/
│       ├── codex-skill-bootstrap/
│       ├── codex-skill-audit/
│       ├── agent-context-guide/
│       ├── agent-context-init/
│       ├── agent-context-verify/
│       ├── agent-context-audit/
│       ├── app-automation/
│       ├── apple-craft/
│       ├── apple-harness/
│       ├── apple-review/
│       ├── gpt-research/
│       ├── hey-codex/
│       ├── macos-release/
│       └── plugin-doctor/
└── .codex/
    └── agents/
        ├── context-validator.toml
        ├── harness-planner.toml
        ├── harness-designer.toml
        ├── harness-builder.toml
        ├── harness-evaluator.toml
        └── harness-reviewer.toml
```

## 원본 플러그인 → Codex 이식 매핑

| 원본 | Codex 이식 결과 |
|---|---|
| `agent-context` | `agent-context-guide`, `agent-context-init`, `agent-context-verify`, `agent-context-audit` |
| `app-automation` | `app-automation` |
| `apple-craft` | `apple-craft`, `apple-harness`, `apple-review` + `.codex/agents/harness-*` |
| `gpt-research` | `gpt-research` |
| `hey-codex` | `hey-codex` |
| `macos-release` | `macos-release` |
| `plugin-doctor` | `plugin-doctor` |

## 설계 메모

### 1. `agent-context`의 Codex화

원본은 `CLAUDE.md`와 `.claude/rules/` 중심이었지만, Codex에서는 `AGENTS.md` / `AGENTS.override.md` 계층 구조가 공식 경로이므로 다음처럼 재해석했습니다.

- 루트 공통 규칙 → `AGENTS.md`
- 하위 도메인 전용 규칙 → 가까운 디렉토리의 `AGENTS.md`
- 임시/우선 규칙 → `AGENTS.override.md`
- 장문 도메인 설명 → `CONTEXT.md` 또는 `docs/`

### 2. `apple-craft`의 에이전트 이식

원본의 `agents/*.md`는 Codex의 **project-scoped custom agents**에 맞춰 `.codex/agents/*.toml`로 옮겼습니다. 현재 저장소에서는 skill 중심 구조를 유지하면서, 필요한 경우 Codex app/CLI에서 해당 custom agent를 사용할 수 있게 했습니다.

### 3. 플러그인 패키징은 의도적으로 보류

이 저장소는 **repo-local skill workspace**가 1차 목적입니다. `.codex-plugin/plugin.json` 기반의 배포 패키징은 다음 단계로 남겨두었습니다. 대신 `plugin-doctor`가 나중에 그 전환을 점검할 수 있게 Codex 기준 감사 규칙을 포함했습니다.

## 포함 스킬

### Bootstrap / Audit
- `codex-skill-bootstrap` — 새 Codex 스킬 생성/정리
- `codex-skill-audit` — repo-local skill workspace 감사

### Context Architecture
- `agent-context-guide` — Codex용 계층형 instruction 설계 가이드
- `agent-context-init` — AGENTS.md 기반 컨텍스트 구조 초기화
- `agent-context-verify` — instruction 정합성 3단계 검증
- `agent-context-audit` — instruction 밀도/깊이/중복 감사

### Apple / Automation
- `app-automation` — iOS Simulator / macOS 앱 자동화
- `apple-craft` — Swift/SwiftUI/UIKit/Xcode 개발
- `apple-harness` — PLAN→DESIGN→BUILD→EVALUATE 장기 루프
- `apple-review` — Apple 플랫폼 관점 코드/PR 리뷰

### Research / Delegation / Release
- `gpt-research` — 외부 GPT/리서치용 구조화 프롬프트 생성
- `hey-codex` — 별도 Codex CLI 인스턴스 위임
- `macos-release` — macOS 릴리스 자동화
- `plugin-doctor` — Codex plugin/skill repo 감사

## 로컬 plugin 패키징 레이어

배포/설치 테스트를 위해 다음도 함께 생성했습니다.

- repo marketplace: `.agents/plugins/marketplace.json`
- local plugin packages: `plugins/<plugin-name>/.codex-plugin/plugin.json`
- 동기화 스크립트: `scripts/sync_packaged_plugins.py`

### 생성된 로컬 plugin 패키지
- `plugins/agent-context`
- `plugins/app-automation`
- `plugins/apple-craft`
- `plugins/gpt-research`
- `plugins/hey-codex`
- `plugins/macos-release`
- `plugins/plugin-doctor`

### 갱신 방법

```bash
python3 scripts/sync_packaged_plugins.py
```

### 테스트 가이드
- `docs/local-plugin-testing.md`
- `python3 scripts/update_browser_capture_assets.py <plugin-name> /path/to/browser-capture.png`

### 로컬 설치 테스트 메모

OpenAI Codex plugin 문서 기준으로 repo marketplace는 `$REPO_ROOT/.agents/plugins/marketplace.json`에 두고, 각 entry의 `source.path`는 marketplace root 기준 상대 경로 `./plugins/<plugin-name>`를 사용합니다. marketplace 또는 plugin 패키지를 갱신한 뒤에는 Codex를 재시작해서 카탈로그를 다시 읽게 하면 됩니다.

## 사용 예시

- “이 저장소 instruction 구조를 다시 짜줘” → `agent-context-guide`
- “AGENTS.md 체계를 자동으로 깔아줘” → `agent-context-init`
- “SwiftUI 빌드 에러를 잡아줘” → `apple-craft`
- “처음부터 설정 화면을 만들어줘” → `apple-harness`
- “PR #42를 Apple 관점에서 리뷰해줘” → `apple-review`
- “이 프로젝트를 외부 GPT 리서치용 프롬프트로 정리해줘” → `gpt-research`
- “Codex CLI를 한 번 더 돌려서 세컨드 오피니언 받아와” → `hey-codex`
- “이 repo를 Codex plugin 관점에서 검사해줘” → `plugin-doctor`


- live capture 갱신: `python3 scripts/update_live_capture_assets.py /path/to/codex-live-capture.png`


## License

MIT
