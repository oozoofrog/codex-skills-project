# 평가축 · 증거 · 자동 다음 행동 매트릭스

이 문서는 Anthropic의 harness 글을 바탕으로, 이 저장소의 각 스킬에 대해 **무엇을 평가하고**, **무슨 증거를 보고**, **그 뒤 무엇을 자동으로 할지**를 정리한 운영 매트릭스입니다.

관련 문서:

- `docs/evaluation-loop-standard.md`
- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`

## 읽는 법

- **평가축**: evaluator가 실제로 판정해야 하는 항목
- **증거**: 판정을 지탱하는 로그/스크립트/산출물
- **자동 다음 행동**: 평가 결과에 따라 시스템이 기본으로 취할 다음 단계

| Skill | 평가축 | 증거 | 자동 다음 행동 |
|---|---|---|---|
| `agent-context-audit` | instruction 밀도, 책임 분리, 중복 규칙, 커버리지 공백 | instruction tree, `AGENTS.md` 계층, 중복 규칙 사례 | `pass`면 개선안 보고 후 종료, `warning`이면 분리 제안, `critical`이면 `agent-context-init` 또는 `agent-context-guide`로 구조 재설계 |
| `agent-context-guide` | 계층 설계 적절성, 루트/하위 책임, 외부 docs 분리 적절성 | 제안된 파일 배치안, 책임 표, 링크 구조 | `pass`면 설계안 확정, `refine`이면 책임 경계 재설정, `rescope`면 planner 단계로 돌아가 범위 축소, 필요 시 `agent-context-verify`/`audit` 호출 |
| `agent-context-init` | 생성된 instruction 구조 정확성, 링크 무결성, 중복 감소, 책임 명확성 | 생성 파일 목록, 링크 검사, 명령 검증, verify/audit 결과 | `pass`면 종료, `refine`이면 파일/링크 수정, `rescope`면 구조 재배치, `critical`이면 `agent-context-verify` → `agent-context-audit` 순으로 교차 검증 후 재생성 |
| `agent-context-verify` | 링크 무결성, 명령/경로 정확성, 문서 주장과 코드 일치성 | 파일 존재 여부, 실행 명령 결과, 관련 코드/설정 | `pass`면 종료, `warning`이면 수정 후보 제안, `critical`이면 해당 문서를 block 처리하고 상위 스킬에 재작성 요청 |
| `app-automation` | selector 안정성, 플로우 재현성, 증거 충분성, 실패 위치 명확성 | `analyze_ui`, `query_ui`, `run_steps`, screenshot/video, step log | `pass`면 시나리오 완료 보고, `refine`이면 selector/step 조정 후 재실행, `pivot`이면 좌표 기반에서 selector 기반 또는 반대로 전략 전환, `escalate`면 사람에게 막힌 단계 보고 |
| `apple-craft` | buildability, API 사용 정확성, lifecycle/concurrency 안정성, UI 검증 가능성 | `BuildProject`, diagnostics, `RenderPreview`, 관련 파일 diff | `pass`면 종료, `refine`이면 최소 수정 후 재빌드, `pivot`이면 구현 전략 변경, `escalate`면 `apple-review` 또는 장기 작업이면 `apple-harness`로 넘김 |
| `apple-harness` | feature completeness, functionality, visual design, code quality, acceptance criteria 충족 | `.codex/harness/*`, build log, preview, QA round 문서, runtime interaction | `pass`면 다음 기능 또는 종료, `refine`이면 builder 재수행, `pivot`이면 디자인/구조 전환, `rescope`면 planner/spec 갱신, 3라운드 초과 시 `escalate` |
| `apple-review` | correctness, lifecycle, concurrency, state management, test/accessibility 누락 | Swift 파일, PR diff, diagnostics, build 결과 | `pass`면 findings 없음으로 종료, `warning`이면 수정 제안, `critical`이면 block finding으로 반환하고 구현 스킬에 수정 요청 |
| `codex-skill-audit` | 구조 적합성, discovery readiness, frontmatter 품질, `openai.yaml` 정합성, review harness 선언 적절성 | `audit_codex_skill_repo.py`, `SKILL.md`, `openai.yaml`, references/scripts 구조 | `pass`면 종료, `warning`이면 문서/metadata 정리, `critical`이면 `codex-skill-bootstrap`으로 구조 재정비 후 재감사 |
| `codex-skill-bootstrap` | skill 구조 적합성, frontmatter 정확성, progressive disclosure, review harness 선언 적절성 | 생성 파일 목록, `SKILL.md`, `openai.yaml`, audit 결과 | `pass`면 완료, `refine`이면 구조/메타데이터 수정, `rescope`면 skill 범위 축소, `critical`이면 `codex-skill-audit` findings 기준으로 재생성 |
| `goal-research-loop` | 목표 명확성, 평가 가능성, evidence 품질, keep/revert 정당성, 반복 discipline, 세션 간 상태 연속성 | loop contract, baseline, experiment ledger, state snapshot, 실행 로그 또는 조사 근거 | `pass`면 best state 요약 후 종료, `refine`이면 같은 계약으로 다음 가설 실행, `pivot`이면 접근 전략 변경, `rescope`면 계약 재작성, `escalate`면 사람 판단/별도 스킬 요청, `stop`이면 남은 리스크와 다음 후보만 남기고 종료 |
| `gpt-research` | 소스 커버리지, chunking 적절성, 민감정보 누락, prompt 사용 가능성 | 포함 파일 목록, chunking 결과, 최종 prompt 본문 | `pass`면 prompt 반환, `refine`이면 맥락 추가/제거, `pivot`이면 module/arch/issue 모드 변경, `escalate`면 사람이 범위 재지정 |
| `hey-codex` | explicit-only 준수, subprocess 결과 품질, diff 안전성, 결과 요약 충실성 | mode detection 결과, subprocess output, snapshot diff, 변경 파일 목록 | `pass`면 결과 요약 전달, `refine`이면 prompt/모드 수정 후 재실행, `critical`이면 write 결과 수용 중단, `escalate`면 부모 세션 직접 검토 |
| `macos-release` | release completeness, 로컬 검증 통과, 산출물 무결성, 공개 순서 준수 | build logs, package path, checksum, local install 확인, release notes | `pass`면 공개 단계 진행, `refine`이면 빌드/패키징 수정, `stop`이면 외부 공개 중단, `critical`이면 checksum 또는 install 문제 해결 전 병합/배포 금지 |
| `plugin-doctor` | marketplace ↔ package 정합성, manifest 품질, legacy residue, custom agent/skill 연결성 | plugin audit script, manifest JSON, asset 존재, marketplace metadata | `pass`면 종료, `warning`이면 metadata 정리, `critical`이면 packaging 또는 manifest 재생성, 필요 시 `sync_packaged_plugins.py` 재실행 |

## 공통 자동화 규칙

### 1. `pass`
- 문서화 후 종료
- 다음 기능 또는 다음 스킬로 이동 가능

### 2. `refine`
- 같은 계약 안에서 한 번 더 수정
- 반드시 **구체적 수정 지시**와 **재검증 방식**을 같이 남김

### 3. `pivot`
- 접근 방식 자체를 바꿈
- 예: 레이아웃만 손보던 흐름에서 구조 재설계로 전환

### 4. `rescope`
- 계획/계약이 너무 넓거나 애매할 때
- planner 또는 spec 재작성으로 복귀

### 5. `escalate`
- 모델/스크립트만으로는 판단이 불충분
- 사람 검토, 상위 스킬, 별도 reviewer 호출

## 기본 threshold

- 결정적 검사 실패 → 즉시 `warning` 이상
- 실행 실패/경로 불일치/metadata 모순 → 보통 `critical`
- evidence 부족 → 기본적으로 `pass` 금지
- 같은 실패 패턴 2회 반복 → `refine`에서 `pivot/rescope`로 승격

## 운영 메모

- 이 표는 **정적 문서**가 아니라 모델/도구 변화에 따라 줄이거나 바꿔야 하는 운영 기준입니다.
- 특히 evaluator가 너무 많은 오버헤드를 만든다면, Anthropic 글의 원칙처럼 **load-bearing component인지 다시 검토**합니다.
