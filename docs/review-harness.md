# Review Harness Convention

이 저장소는 **literal GAN training**을 도입하지 않습니다. 대신 **GAN-inspired generator–evaluator harness**를 스킬 설계 패턴으로 사용합니다. 즉, 같은 모델에게 자기 결과를 막연히 다시 물어보는 대신, **생성 역할**과 **검토 역할**을 분리하고 가능하면 외부 증거에 앵커링합니다.

## 왜 이 규칙을 두는가

- OpenAI Codex Skills 문서는 skill을 *instructions, resources, optional scripts*의 묶음으로 설명하며, progressive disclosure를 통해 필요한 순간에만 전체 지침을 로드한다고 설명합니다.
- OpenAI AGENTS.md 문서는 규칙을 작업과 가까운 곳에 두고, 긴 배경 설명은 `docs/` 같은 외부 문서로 분리하라고 안내합니다.
- Anthropic의 *Effective harnesses for long-running agents* (2025-11-26)는 **generator와 evaluator를 분리하는 편이 self-evaluation bias를 줄이는 데 더 실용적**이라는 운영 방향을 보여줍니다.

따라서 이 저장소에서는:

1. `SKILL.md`는 짧게 유지하고
2. review policy는 공통 문서로 분리하며
3. 필요한 스킬만 `Review Harness` 섹션으로 선언합니다.

자동 진행 제어 로직의 상세 표준안은 `docs/evaluation-loop-standard.md`,
스킬별 평가축/증거/다음 행동 표는 `docs/evaluation-loop-skill-matrix.md`를 따릅니다.

## 용어

- **Planner**: 범위, 완료 조건, 아티팩트 형식을 먼저 정리하는 역할
- **Generator**: 실제 문서, 코드, 설정, 릴리스 산출물을 만드는 역할
- **Evaluator**: read-only 우선으로 결과를 검토하고 evidence를 수집하는 역할
- **Evaluator-native skill**: 스킬 자체가 본질적으로 감사/검증/리뷰 역할인 경우
- **Artifact**: 역할 간 핸드오프를 위한 파일 또는 구조화된 결과물
- **Evidence**: 평가 판단을 지탱하는 로그, 스크린샷, diff, 링크 검사, 빌드 결과 등

## Harness mode

각 스킬은 아래 3가지 모드 중 하나를 선언할 수 있습니다.

| mode | 의미 | 적용 기준 |
|---|---|---|
| `none` | 별도 evaluator를 추가하지 않음 | 짧은 읽기 작업, 결정적 스크립트 중심 작업, evaluator-native skill |
| `optional` | 위험도나 범위가 커질 때 evaluator를 붙임 | 중간 규모 구현/자동화/문서화 작업 |
| `required` | planner/generator/evaluator 분리를 기본값으로 둠 | 장기 구현, 쓰기 위험이 큰 변경, 배포/릴리스, repo 구조 변경 |

## 기본 루프

1. **Scope**
   - 작업이 `none / optional / required` 중 어디에 속하는지 결정합니다.
   - 고위험 쓰기 작업이면 `required`를 우선 검토합니다.
2. **Plan**
   - 완료 조건, 금지사항, evidence 종류를 먼저 적습니다.
3. **Generate**
   - 변경은 가능한 한 작은 write scope로 수행합니다.
4. **Evaluate**
   - 결과를 독립적으로 읽고, 가능하면 스크립트/빌드/스크린샷/링크 체크로 검증합니다.
5. **Iterate**
   - evaluator가 문제를 남기면 generator가 수정합니다.
   - 기본 최대 라운드는 **2~3회**입니다.
6. **Stop**
   - 통과 조건 충족
   - 또는 남은 리스크를 명시하고 종료

## Evidence 우선순위

가능하면 아래 순서로 평가 근거를 쌓습니다.

1. **결정적 검사**
   - audit script, lint, schema check, path existence
2. **실행 증거**
   - build/test log, CLI output, exit code
3. **상호작용 증거**
   - screenshot, preview, UI tree, video
4. **구조 증거**
   - diff, file tree, frontmatter, metadata consistency
5. **모델 판단**
   - 위 증거를 해석하는 마지막 단계로만 사용

모델의 인상평만으로 승인하지 않습니다.

## `SKILL.md`에 넣는 최소 계약

review loop가 의미 있는 스킬은 아래 형식의 짧은 섹션을 둡니다.

```md
## Review Harness
- mode: optional
- 공통 기준: `../../../docs/review-harness.md`
- generator: ...
- evaluator: ...
- 평가축: ...
- artifacts/evidence: ...
- pass condition: ...
- 자동 다음 행동: ...
```

원칙:

- `SKILL.md`에는 **핵심 절차와 계약만** 둡니다.
- 긴 평가 루브릭은 `docs/` 또는 `references/`로 분리합니다.
- evaluator가 sibling skill이면 이름을 명시합니다.
- evaluator-native skill이면 `mode: none`으로 두고 **이 스킬 자체가 evaluator**임을 적습니다.
- `평가축`과 `자동 다음 행동`은 가능하면 한 줄로 명확히 씁니다.

## `agents/openai.yaml` 정합성

review harness를 선언했다면 선택적 메타데이터도 가능한 한 같은 의도를 반영합니다.

- **explicit-only skill**이면 `policy.allow_implicit_invocation: false`
- `required` 또는 `optional` 스킬이면 `default_prompt`가 검증/증거 수집 의도를 과장 없이 드러내는 편이 좋습니다
- `short_description`은 실제 범위보다 넓게 써서 무분별한 implicit invocation을 유도하지 않습니다

## 언제 생략해도 되는가

아래 경우에는 `mode: none`이 적절할 수 있습니다.

- 짧은 읽기/요약/탐색
- 결과가 거의 전적으로 결정적 스크립트에 의해 검증되는 작업
- 스킬 자체가 감사/검증/리뷰 스킬인 경우

## 저장소 기본 페어링

| Generator 측 | Evaluator 측 |
|---|---|
| `codex-skill-bootstrap` | `codex-skill-audit` |
| `agent-context-init` | `agent-context-verify`, `agent-context-audit` |
| `agent-context-guide` | `agent-context-verify`, `agent-context-audit` |
| `apple-craft` | `apple-review` + Xcode diagnostics |
| `apple-harness` | built-in PLAN / BUILD / EVALUATE roles |
| `macos-release` | dry-run / local install / checksum verification |

## 비목표

- 모든 작업을 무조건 multi-agent로 만드는 것
- 단순 자기반성 프롬프트를 “GAN”이라고 부르는 것
- evidence 없이 reviewer의 감상만 늘리는 것

## 참고

- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Anthropic, *Effective harnesses for long-running agents* (2025-11-26): https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
