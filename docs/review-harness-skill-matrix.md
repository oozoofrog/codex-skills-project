# Review Harness Skill Matrix

이 문서는 현재 저장소의 각 스킬이 `docs/review-harness.md`를 어떻게 적용하는지 한눈에 보여줍니다.

| Skill | mode | Generator / Planner | Evaluator | Artifacts / Evidence | Notes |
|---|---|---|---|---|---|
| `agent-context-audit` | `none` | 상위 스킬이나 사용자가 제공한 instruction 구조 | 이 스킬 자체가 evaluator-native | instruction tree, 중복 규칙, 책임 분리 근거 | 필요 시 후속 수정안은 `agent-context-verify`로 교차 검증 |
| `agent-context-guide` | `optional` | AGENTS 계층 구조 설계안 | `agent-context-verify`, `agent-context-audit` | 파일 배치안, 책임 분리, docs 분리 계획 | 설계 제안 단계에서는 가볍게, 실제 반영 전에는 검증 권장 |
| `agent-context-init` | `required` | 루트/하위 `AGENTS.md`, `CONTEXT.md` 생성·정리 | `agent-context-verify` → `agent-context-audit` | 생성 파일 목록, 링크, 명령 검증, 책임 분리 | repo 지침을 직접 쓰므로 기본적으로 검증까지 한 세트 |
| `agent-context-verify` | `none` | 상위 스킬이 만든 instruction 파일 | 이 스킬 자체가 evaluator-native | 링크 무결성, 명령/파일 경로, 주장 정확성 | 결과는 `critical / warning / info / strength` |
| `app-automation` | `optional` | actor 단계가 UI를 조작 | observer 단계가 UI tree/screenshot/video 검토 | `analyze_ui`, `query_ui`, `screenshot`, `record_video` | 긴 플로우나 flaky UI에서는 review 단계 강화 |
| `apple-craft` | `optional` | 구현/수정/설명 | `apple-review`, `BuildProject`, `RenderPreview`, diagnostics | build log, preview, issue navigator | 단일 수정은 가볍게, UI/동시성 변화는 리뷰 권장 |
| `apple-harness` | `required` | planner / designer / builder | evaluator / reviewer | `.codex/harness/*`, preview, build logs, evaluation rounds | 이 저장소의 기준 harness 구현 |
| `apple-review` | `none` | 상위 구현 또는 PR diff | 이 스킬 자체가 evaluator-native | Swift 파일, diagnostics, build 결과, severity report | Apple lifecycle / concurrency / accessibility 중심 |
| `codex-skill-audit` | `none` | 상위 스킬이 만든 skill repo 변경 | 이 스킬 자체가 evaluator-native + audit script | 구조 감사 보고서, script output | bootstrap 이후 기본 후속 스킬 |
| `codex-skill-bootstrap` | `required` | skill 구조 설계 및 생성 | `codex-skill-audit` | 생성 파일 목록, frontmatter, references 분리, metadata | 새 스킬/구조 변경 시 audit까지 포함 |
| `gpt-research` | `optional` | research prompt 초안 생성 | coverage/chunking checklist 기반 read-only 검토 | 포함 파일 목록, chunking 결과, prompt 본문 | 민감정보·누락·과잉맥락을 점검 |
| `hey-codex` | `optional` | 별도 Codex 인스턴스 실행 | 부모 세션의 diff / output review | subprocess output, snapshot diff, mode detection | `write` 모드에서는 사실상 required에 가깝게 운용 |
| `macos-release` | `required` | 버전 범프, 빌드, 패키징, 배포 준비 | dry-run, local install, checksum, release checklist | build logs, package hashes, 설치 확인, release notes | 로컬 검증 전 외부 공개 금지 |
| `plugin-doctor` | `none` | 상위 변경사항 또는 대상 repo 구조 | 이 스킬 자체가 evaluator-native | plugin audit script, manifest consistency, legacy residue | plugin/skill/custom agent 정합성 감사 |

## 적용 규칙

1. 새로운 스킬을 추가할 때는 먼저 이 표에 들어갈 `mode`를 정합니다.
2. `required` 스킬은 `SKILL.md`에 `Review Harness` 섹션을 둡니다.
3. `optional` 스킬도 review loop가 의미 있으면 같은 섹션을 둡니다.
4. `none` 스킬은 보통 evaluator-native이므로 별도 evaluator를 강제하지 않습니다.
