# v0.4.0 후보 작업 목록

이 문서는 **확정 로드맵이 아니라 후보 작업 목록**입니다.  
`v0.3.0`에서 정리한 research / install validation / audit parity / release helper 기반을 바탕으로,  
다음 단계에서 무엇을 더 자동화하고 무엇을 더 안정화할지 정리합니다.

## 목표

`v0.3.0`이 운영 모델과 반복 가능한 도구를 추가했다면,  
`v0.4.0`에서는 이를 **더 자동화되고, 더 재현 가능하며, 더 기계적으로 검증 가능한 상태**로 밀어붙이는 것이 목표입니다.

핵심 방향은 다음 3가지입니다.

1. release / install / plugin parity 검증을 더 자동화하기
2. evaluator 출력과 review harness 계약을 더 구조화하기
3. 장기 루프와 로컬 테스트 흐름의 재현성을 높이기

## 후보 작업

### 1. release helper smoke check / CI 연동

`scripts/release_helper.py`는 현재 `check / plan / publish`를 제공하지만,  
아직 정적 smoke check 또는 CI 검증 단계에 연결되어 있지는 않습니다.

다음 단계 후보:

- `scripts/run_release_smoke_checks.py` 추가 또는 기존 smoke check에 release helper 검증 포함
- 샘플 버전/문서 fixture 기반으로 `check` / `plan` 회귀 검증
- `draft`와 `publish` 경로의 명령 생성 차이 자동 비교
- `docs/release-workflow.md`와 helper CLI help 출력의 정합성 검사

### 2. packaged plugin parity를 README / assets까지 확장

`v0.3.0`에서는 packaged `SKILL.md`, packaged `openai.yaml`, single-skill plugin manifest metadata drift를 잡게 했습니다.  
다음 단계에서는 아래도 후보입니다.

- packaged plugin `README.md`의 핵심 문구 drift 탐지
- screenshots / browser capture / live capture 존재 정책 정리
- generated assets 재생성 후 메타데이터 변화 힌트 추가
- multi-skill plugin(`agent-context`, `apple-craft`)의 prompt/description parity rules 확장

### 3. evaluator output template / schema 고정

문서 수준의 `Review Harness` 선언은 강화됐지만,  
각 evaluator-native skill의 출력 형식은 아직 완전히 고정돼 있지 않습니다.

후보:

- `codex-skill-audit` findings JSON schema 또는 markdown template 고정
- `agent-context-verify`의 링크/명령/주장 3단 리포트 형식 고정
- `apple-review`의 severity / 위치 / 영향 / 수정 방향 포맷 고정
- `plugin-doctor`의 packaged/source drift findings 형식 고정

### 4. global install validation을 CI/fixture 수준으로 승격

`v0.3.0`에서 `--dry-run`과 `--validate-installed`는 개선됐지만,  
지금은 주로 manual smoke check에 의존합니다.

후보:

- temp destination fixture 기반 install validation regression check
- populated `~/.codex/skills` 시뮬레이션을 위한 isolated test destination
- alias / dependency / frontmatter drift를 fixture 기반으로 다시 검증
- install helper 결과를 CI에서 summary 형태로 남기기

### 5. goal-research-loop runner 안정화

`goal-research-loop`는 usable state에 도달했지만,  
장기적으로는 host-managed artifact 흐름을 더 단단하게 만들 여지가 있습니다.

후보:

- structured result append와 ledger 관리 회귀 점검
- round artifact 생성/종료 시점 일관성 강화
- runner failure / timeout / interrupted turn 복구 흐름 정리
- lightweight / standard prompt profile 차이 검증

### 6. local plugin testing 문서 단순화

현재 문서와 스크립트는 충분히 강하지만,  
사용 순서를 더 짧고 분명하게 만들 여지가 있습니다.

후보:

- `docs/local-plugin-testing.md`를 install → sync → smoke → restart → verify 순서로 재정리
- live capture / browser capture 갱신 절차 압축
- “처음 해보는 사람용” 최소 절차와 “유지보수용” 전체 절차를 분리

## 우선순위 초안

### P1

- release helper smoke check / CI 연동
- packaged plugin parity 범위 확장
- evaluator output template / schema 고정

### P2

- global install validation regression automation
- goal-research-loop runner 안정화

### P3

- local plugin testing 문서 단순화

## 제외하거나 신중히 볼 항목

- release helper를 즉시 범용 배포 도구로 일반화하는 것
- multi-skill plugin parity를 과도하게 엄격하게 만들어 false positive를 늘리는 것
- evidence 없이 evaluator 출력 형식만 복잡하게 만드는 것

## 제안되는 다음 이슈 단위

1. release helper smoke check / regression automation
2. packaged plugin README / asset parity 확장
3. evaluator output template 고정
4. goal-research-loop runner artifact 안정화
