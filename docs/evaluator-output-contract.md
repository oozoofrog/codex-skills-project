# Evaluator output contract

이 문서는 evaluator-native skill과 audit script가 따를 **공통 출력 계약**을 정리합니다.

목표는 두 가지입니다.

1. 사람이 읽는 Markdown 요약이 항상 비슷한 구조를 갖게 하기
2. 자동화가 읽을 수 있는 machine summary JSON을 안정적으로 남기기

## Markdown 기본 형식

최소한 아래 순서를 권장합니다.

```markdown
# <Report title>

## Summary
- 범위
- 핵심 판정
- finding 수

## Findings
- [critical] ...
- [warning] ...
- [info] ...

## Recommended fixes
1. ...
2. ...

## Machine summary
```json
{ ... }
```
```

원칙:

- 사람이 읽는 요약이 먼저 온다
- severity는 `critical / warning / info / strength` 같은 고정 vocabulary를 우선 사용한다
- `Machine summary`는 항상 마지막에 둔다

## Machine summary 공통 필드

script가 machine summary를 출력하거나 파일로 쓸 때는 가능한 한 아래 필드를 유지합니다.

```json
{
  "report_type": "codex-skill-audit",
  "schema_version": 1,
  "target": "/abs/path",
  "findings_count": 0,
  "strengths_count": 0,
  "findings": [],
  "strengths": []
}
```

### 필수 필드

- `report_type`
- `schema_version`
- `target`
- `findings_count`
- `strengths_count`
- `findings`
- `strengths`

### findings 항목 공통 형식

```json
{
  "severity": "warning",
  "where": "path/or/name",
  "message": "human-readable explanation"
}
```

## 스크립트 옵션 권장

deterministic audit script가 있다면 아래 옵션을 권장합니다.

- `--json-out <path>`
  - machine summary JSON을 파일로 저장

stdout에는 여전히 사람이 읽는 보고서를 출력하고,
`--json-out`은 추가 artifact로 취급하는 편을 기본값으로 둡니다.

## 현재 적용 대상

- `codex-skill-audit`
- `plugin-doctor`
- `agent-context-verify` 같은 evaluator-native verification skill의 문서 출력 가이드
