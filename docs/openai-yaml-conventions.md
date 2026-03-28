# `agents/openai.yaml` Conventions

이 문서는 이 저장소의 `agents/openai.yaml` 작성 규칙을 정리합니다. 기본 형식은 OpenAI Codex Skills 문서의 optional metadata를 따르되, 이 저장소는 **trigger 범위**, **Review Harness 정합성**, **과장 방지**를 더 엄격하게 봅니다.

## 기준 출처

- OpenAI Codex Skills: skills는 `SKILL.md`와 optional scripts / references / `agents/openai.yaml`로 구성될 수 있습니다.
- OpenAI Codex Skills: implicit invocation은 `description` 기반이므로 설명의 범위와 경계가 중요합니다.
- 이 저장소의 review harness 규약: `docs/review-harness.md`

## 최소 구조

```yaml
interface:
  display_name: "My Skill"
  short_description: "One-line summary"
  default_prompt: "Use this skill to ..."
policy:
  allow_implicit_invocation: true
```

## 필드별 규칙

### `interface.display_name`

- UI에 보일 이름입니다.
- `SKILL.md`의 `name`과 완전히 같을 필요는 없지만 **같은 스킬임이 분명해야** 합니다.
- 브랜드 표현보다 **용도 표현**을 우선합니다.

좋음:
- `Agent Context Verify`
- `Apple Harness`

피해야 함:
- `Ultimate Skill Auditor`
- `Magic Swift Helper`

### `interface.short_description`

- 1문장 요약입니다.
- implicit invocation을 유도하는 핵심 텍스트라서 **너무 넓으면 안 됩니다**.
- “언제 쓰는가”를 드러내되, 없는 능력을 암시하지 않습니다.

좋음:
- `Run a separate Codex CLI task only on explicit request`

나쁨:
- `Helps with anything in the repo`

### `interface.default_prompt`

- 시작 프롬프트 예시입니다.
- 이 저장소에서는 가능한 한 아래를 반영합니다.
  - 작업 범위
  - evidence 또는 verify/audit 의도
  - explicit-only 여부
- marketing 문구보다 **실제 실행 문장**이 좋습니다.

좋음:
- `Audit this Codex skill repository for official structure, frontmatter quality, openai.yaml alignment, review-harness consistency, and progressive-disclosure hygiene.`

나쁨:
- `Use this amazing skill to do the best possible work.`

### `policy.allow_implicit_invocation`

- `true`: 설명 기반으로 Codex가 암묵 호출 가능
- `false`: 사용자가 명시적으로 호출할 때만 사용

다음 경우 `false`를 강하게 권장합니다.

- 스킬 본문에 “명시적으로 요청했을 때만”이 들어가는 경우
- 별도 프로세스 실행, 배포, destructive write처럼 오용 비용이 큰 경우
- 일반 skill discovery에 섞이면 오탐이 쉬운 경우

예:
- `hey-codex` → `false`

## Review Harness와의 정합성

`SKILL.md`에 `Review Harness`가 있다면 메타데이터도 같은 의도를 보여야 합니다.

### mode별 권장

| mode | 메타데이터 권장 |
|---|---|
| `none` | evaluator-native 성격이 드러나게 `short_description` 작성 |
| `optional` | `default_prompt`에 검증/evidence를 과장 없이 암시 |
| `required` | `default_prompt`에 verify gate, planner/evaluator, audit-ready 같은 표현을 포함해도 좋음 |

### explicit-only와 policy 일치

아래 둘은 반드시 같이 움직여야 합니다.

- `SKILL.md` 본문: explicit-only 선언
- `openai.yaml`: `allow_implicit_invocation: false`

불일치 예:

- 본문: “이 스킬은 사용자가 명시적으로 요청했을 때만 사용한다.”
- YAML: `allow_implicit_invocation: true`

이 경우 audit에서 경고 대상입니다.

## 작성 원칙

1. **SKILL.md 우선**
   - `openai.yaml`는 보조 메타데이터입니다.
   - 의미의 source of truth는 여전히 `SKILL.md`입니다.
2. **범위 축소를 두려워하지 않기**
   - discovery가 조금 덜 되더라도 오탐이 줄어드는 편이 낫습니다.
3. **없는 능력 금지**
   - review, verification, packaging, release 같은 단어는 실제 절차가 있을 때만 씁니다.
4. **문구보다 증거**
   - 가능한 경우 `default_prompt`는 build, audit, screenshot, verify 같은 검증 어휘를 포함합니다.

## 저장소 기본 체크리스트

- `display_name`이 실제 스킬과 대응되는가
- `short_description`이 trigger 범위를 과장하지 않는가
- `default_prompt`가 SKILL.md와 모순되지 않는가
- `Review Harness mode`와 메타데이터 뉘앙스가 일치하는가
- explicit-only 스킬이면 `allow_implicit_invocation: false`인가

## 관련 문서

- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`
- `.agents/skills/codex-skill-bootstrap/references/openai-yaml-guide.md`
- `.agents/skills/codex-skill-audit/references/audit-checklist.md`
