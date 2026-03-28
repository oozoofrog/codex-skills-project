# v0.3.0 후보 작업 목록

이 문서는 **확정 로드맵이 아니라 후보 작업 목록**입니다.  
우선순위와 범위는 이후 이슈/사용자 피드백에 따라 바뀔 수 있습니다.

## 목표

`v0.2.0`에서 문서화한 review harness와 evaluation loop를,  
`v0.3.0`에서는 **더 자동화되고 더 강하게 검증되는 운영 체계**로 밀어붙이는 것이 목표입니다.

## 후보 작업

### 1. audit 스크립트의 평가 루프 검사 강화

현재는 `Review Harness` 존재와 필수 필드를 주로 확인합니다.  
다음 단계에서는 아래까지 보고 싶습니다.

- `평가축`과 `자동 다음 행동`의 형식 일관성
- `mode`와 실제 설명/metadata 간 불일치 탐지
- evaluator-native skill인데 과한 generator 문구가 있는지 탐지
- explicit-only + plugin metadata + packaged skill 복제본의 3중 정합성 검사

### 2. packaged plugin doctor 검사 강화

- packaged skill 복제본의 `Review Harness`가 원본과 동일한지 비교
- plugin manifest의 `defaultPrompt`와 source skill `openai.yaml` 의미 정합성 검사
- generated assets 변경 시 source metadata 변경 여부를 추적하는 힌트 추가

### 3. release 자동화 보강

- `v0.x.y` 릴리스용 스크립트/명령 래퍼 제공
- CHANGELOG / release notes / tag / GitHub Release를 한 흐름으로 정리
- dry-run release helper 추가 검토

### 4. global install 검증 강화

- `scripts/install_global_skills.py --dry-run` 결과를 CI/로컬 smoke check에 더 적극 반영
- 설치 후 `~/.codex/skills` 기준 검증 시나리오 정리
- alias / dependency 규칙 자동 검사 보강

### 5. skill-by-skill evaluator templates

문서 수준 선언을 넘어, 각 스킬별 evaluator 출력 형식을 더 고정하는 작업입니다.

예:
- `codex-skill-audit` → findings 템플릿 고정
- `agent-context-verify` → 링크/명령/주장 3단 리포트 고정
- `apple-review` → severity + file/line + impact + fix direction 고정

### 6. local plugin testing 문서 정리

- `docs/local-plugin-testing.md`를 최신 전역 설치/packaged plugin 흐름과 더 명확히 연결
- 실제 사용 순서 중심으로 재배치
- live capture / browser capture 절차를 더 짧게 정리

## 우선순위 초안

### P1
- audit 스크립트의 평가 루프 검사 강화
- packaged plugin doctor 검사 강화
- release 자동화 보강

### P2
- global install 검증 강화
- skill-by-skill evaluator templates

### P3
- local plugin testing 문서 정리

## 제외하거나 신중히 볼 항목

- 모든 스킬을 무조건 multi-agent로 만드는 것
- evaluator를 과도하게 붙여 오버헤드를 늘리는 것
- 문서 없이 스크립트만 늘리는 것

## 제안되는 다음 이슈 단위

1. `codex-skill-audit` / `plugin-doctor` audit 강화
2. release helper 또는 release script 초안
3. global install 검증 시나리오 정리
