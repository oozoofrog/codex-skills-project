# Anthropic 기반 평가 루프 표준안

이 문서는 Anthropic의 *Harness design for long-running application development* (Published Mar 24, 2026)를 읽고, 이 저장소에서 **평가와 이후 동작 자동 진행**을 어떻게 설계할지 정리한 표준안입니다.

핵심 전제:

- **GAN은 영감의 출발점일 뿐**입니다.
- 실제 본체는 **planner / generator / evaluator 분리**
- 그리고 **평가 결과가 다음 동작을 결정하는 자동 제어 루프**입니다.

참고 원문:
- https://www.anthropic.com/engineering/harness-design-long-running-apps

## 0. 먼저 바로잡을 오해

이 문서에서 중요한 것은 “GAN처럼 둘이 싸운다”가 아닙니다.

더 정확히는:

1. **자기 평가 편향(self-evaluation bias)** 을 줄이기 위해 생성과 평가를 분리하고
2. **채점 가능한 기준(gradable criteria)** 을 만들고
3. **도구 기반 증거**로 평가한 뒤
4. 그 결과로 **다음 행동**을 자동 결정하는 것입니다.

이 저장소는 이 구조를 **GAN-inspired review harness**로 부릅니다.

## 1. 평가 루프의 목적

좋은 evaluator의 목적은 단순히 “좋다/나쁘다”를 말하는 것이 아닙니다.

반드시 아래를 만족해야 합니다.

- 결과물이 **실제로 동작하는지** 확인한다
- 어디가 실패했는지 **재현 가능한 형태**로 남긴다
- generator가 다음 라운드에서 바로 고칠 수 있을 만큼 **구체적**이어야 한다
- 평가 결과가 **다음 상태 전이**를 결정해야 한다

즉, 평가는 보고서가 아니라 **제어 신호(control signal)** 입니다.

## 2. 기본 루프

이 저장소의 기본 자동 진행 루프는 아래 순서를 따릅니다.

### Phase A. Scope

작업을 먼저 분류합니다.

- `solo`: 모델 단독으로 충분한가
- `optional-eval`: evaluator를 붙일지 말지 선택 가능한가
- `required-eval`: evaluator 없이는 리스크가 큰가

판단 기준:

- 쓰기 범위가 큰가
- 실행/배포 리스크가 큰가
- 사람이 직접 쓰지 않은 내용이 구조나 정책을 바꾸는가
- 시각/경험 품질처럼 주관 평가가 필요한가
- 모델의 현재 capability boundary 바깥인가

### Phase B. Plan

generator가 바로 작업을 시작하지 않게 합니다.

최소한 아래를 먼저 적습니다.

- 목표 산출물
- 제외 범위
- 평가축
- 증거 종류
- pass / fail 기준
- 최대 반복 횟수

Anthropic 글의 planner 역할을 이 단계로 흡수합니다.

### Phase C. Contract

평가 가능한 계약을 명시합니다.

예:

- “구조가 맞다”가 아니라 → “중복 skill name이 없어야 한다”
- “릴리스가 준비됐다”가 아니라 → “local install, checksum, draft notes가 모두 존재해야 한다”
- “UI가 괜찮다”가 아니라 → “핵심 플로우가 selector 기반으로 재현 가능해야 한다”

**계약은 testable해야 합니다.**

### Phase D. Generate

generator가 구현/수정/생성을 수행합니다.

원칙:

- 가능한 한 작은 write scope
- 중간 아티팩트 남기기
- 다음 evaluator가 바로 읽을 수 있게 하기

### Phase E. Evaluate

evaluator는 가능하면 **read-only + tool-using** 역할을 유지합니다.

우선순위:

1. 결정적 검사
2. 실행 로그
3. UI/미리보기/스크린샷
4. 구조와 metadata
5. 마지막으로 모델 해석

### Phase F. Decide

평가 결과는 아래 상태 중 하나를 반환해야 합니다.

- `pass`
- `refine`
- `pivot`
- `rescope`
- `escalate`
- `stop`

즉 자동 진행의 핵심은 “평가 이후 무엇을 할지”가 미리 정의되어 있는 것입니다.

## 3. 자동 다음 동작 상태기계

이 저장소에서 권장하는 상태 전이는 다음과 같습니다.

| 평가 결과 | 의미 | 자동 다음 동작 |
|---|---|---|
| `pass` | 기준 충족 | 종료 또는 다음 기능으로 이동 |
| `refine` | 방향은 맞지만 결함 존재 | generator에 구체적 수정 지시 후 같은 계약으로 재시도 |
| `pivot` | 현재 접근 방향 자체가 약함 | 다른 설계/전략으로 generator 재시작 |
| `rescope` | spec 또는 contract가 과하거나 모호함 | planner/contract 단계로 되돌림 |
| `escalate` | 모델/도구만으로 판단 불가 | 사람 검토 또는 별도 스킬로 위임 |
| `stop` | 반복 한도 초과 또는 비용 대비 효용 낮음 | 남은 리스크 명시 후 종료 |

### 기본 규칙

- 같은 문제를 같은 방식으로 **3회 이상 반복하지 않는다**
- `refine` 2회 이상인데 점수/증거 개선이 없으면 `pivot` 또는 `rescope`
- 결정적 검사 실패는 감상평보다 우선
- evaluator가 “불확실”하면 승인하지 말고 `escalate` 또는 `rescope`

## 4. 평가축 설계 규칙

Anthropic 글의 핵심은 평가축을 **채점 가능한 형태로 번역**한 점입니다.

이 저장소에서는 각 스킬마다 평가축을 3~5개로 제한합니다.

### 공통 축 후보

- **정확성**: 규칙, 경로, 데이터, 명령이 실제 상태와 맞는가
- **완성도**: 핵심 기능/문서/구조가 빠지지 않았는가
- **증거성**: 주장마다 로그/스크린샷/스크립트 출력이 있는가
- **일관성**: `SKILL.md`, `openai.yaml`, README, marketplace가 서로 맞는가
- **사용성**: 사람이 바로 후속 작업을 할 수 있을 정도로 명확한가

### 축 설계 원칙

- 너무 많은 축 금지
- “좋아 보인다” 같은 인상형 표현 금지
- 사람이 재현할 수 있는 기준으로 번역
- 각 축은 최소 하나의 evidence source와 연결

## 5. Evidence 설계 규칙

평가자는 “생각”보다 “증거”를 먼저 수집해야 합니다.

### evidence 우선순위

1. **Deterministic**
   - lint
   - schema
   - audit script
   - path existence
   - duplicate check
2. **Runtime**
   - build/test logs
   - CLI output
   - exit code
3. **Interactive**
   - Playwright
   - UI tree
   - screenshot/video
4. **Structural**
   - diff
   - file tree
   - metadata alignment

### 강한 원칙

- evidence가 없으면 승인 강도를 낮춘다
- evaluator는 최소 한 개 이상의 **비주관적 근거**를 남겨야 한다
- “느낌상 괜찮다”는 pass 근거가 될 수 없다

## 6. Evaluator 튜닝 규칙

Anthropic 글은 evaluator도 처음부터 잘 작동하지 않는다고 분명히 말합니다.

그래서 이 저장소는 evaluator를 아래처럼 튜닝합니다.

### 1) skeptical default

- 문제를 찾지 못했다고 해서 곧바로 승인하지 않는다
- evidence 부족은 pass가 아니라 `needs more verification`로 본다

### 2) shallow test 금지

- happy path만 보고 승인하지 않는다
- edge case, missing file, mismatch, stale metadata를 적극 탐색한다

### 3) actionable critique

좋은 evaluator 출력은 다음을 포함합니다.

- 위치
- 문제
- 영향
- 최소 수정 방향
- 다음 재검증 방법

### 4) 로그 기반 재튜닝

evaluator가 너무 관대하거나 피상적이면:

1. evaluator 출력을 읽고
2. 놓친 사례를 모으고
3. criteria / threshold / prompt를 갱신합니다

## 7. Planner를 언제 써야 하는가

Anthropic 글에서 planner는 비용 대비 효과가 매우 큰 컴포넌트였습니다.

이 저장소에서는 아래 경우 planner를 강하게 권장합니다.

- 요구사항이 1~4문장 수준으로 짧을 때
- generator가 under-scope 되기 쉬운 작업
- 여러 파일/여러 단계가 엮이는 작업
- 기능보다 **완료 기준 정의**가 먼저 필요한 작업

반대로 아래는 생략 가능:

- 단일 파일의 국소 수정
- 이미 계약이 정해진 결정적 작업

## 8. Evaluator를 언제 생략할 수 있는가

Anthropic 글의 중요한 메시지 중 하나는
**evaluator는 고정 yes/no 컴포넌트가 아니라는 점**입니다.

이 저장소에서는 아래면 evaluator 생략을 검토합니다.

- 결정적 스크립트 하나로 거의 충분한 작업
- 모델이 현재 안정적으로 단독 처리 가능한 작업
- 수정 범위가 매우 작고 회귀 반경이 작음

하지만 아래는 evaluator를 붙이는 편이 낫습니다.

- 구조/정책/배포/설치 변경
- UI/UX 또는 자동화 플로우
- README + metadata + packaging처럼 여러 레이어 정합성이 필요한 작업

## 9. 모델이 바뀌면 하네스를 다시 줄여라

Anthropic 글의 아주 중요한 교훈:

- 하네스 컴포넌트는 영원하지 않습니다.
- 모델이 좋아지면 일부는 더 이상 load-bearing이 아닐 수 있습니다.

그래서 이 저장소는 아래를 기본 원칙으로 둡니다.

### Methodical ablation

- planner 제거 시 성능이 유지되는가
- evaluator를 final-pass로 줄여도 되는가
- per-step QA가 필요한가, final QA면 충분한가
- structured artifact가 과한가, 최소화할 수 있는가

즉:
**하네스는 복잡하게 쌓는 대상이 아니라, 주기적으로 덜어내는 대상**입니다.

## 10. 이 저장소의 기본 표준

### 기본 아티팩트

작업 유형에 따라 아래를 권장합니다.

- spec/plan 문서
- evaluation memo
- audit report
- smoke check output
- screenshot / preview / capture

### 기본 라운드 수

- `optional`: 0~2회
- `required`: 1~3회
- 3회 이후 개선 없으면 `pivot`, `rescope`, `escalate` 중 하나를 강제

### 기본 종료 조건

- 결정적 검사 통과
- 핵심 평가축이 threshold 이상
- 남은 위험이 문서화됨

## 11. 저장소 적용 포맷

각 스킬/워크플로는 아래 5가지를 문서에 남기는 것을 권장합니다.

1. 평가축
2. 증거
3. 자동 다음 행동
4. 최대 반복 수
5. 사람 개입 조건

구체적 스킬별 값은 `docs/evaluation-loop-skill-matrix.md`를 따릅니다.
