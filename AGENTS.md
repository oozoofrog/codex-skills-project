# AGENTS.md

## Repository purpose

이 디렉토리는 **Codex 네이티브 스킬 작업 공간**입니다. Claude용 플러그인 구조를 그대로 복제하지 말고, Codex 공식 문서 기준으로 `.agents/skills` 중심 구조를 유지하세요.

## Working rules

- 새 스킬은 반드시 `.agents/skills/<skill-name>/SKILL.md` 아래에 둡니다.
- 스킬 이름은 kebab-case를 사용합니다.
- `SKILL.md` frontmatter에는 최소 `name`, `description`을 넣습니다.
- 긴 설명은 `references/`로 분리하고, `SKILL.md` 본문은 핵심 절차만 유지합니다.
- `agents/openai.yaml`를 쓰는 경우 SKILL.md와 의미가 어긋나지 않도록 같이 갱신합니다.
- 스킬 디렉토리 안에는 README.md 같은 보조 문서를 추가하지 않습니다.
- 스킬 구조나 메타데이터를 바꿨다면 마지막에 `codex-skill-audit` 기준으로 자체 점검합니다.

## Preferred workflow

1. 공식 Codex 문서를 먼저 확인한다.
2. 기존 스킬과 중복되지 않는지 확인한다.
3. 가장 작은 단위의 스킬부터 만든다.
4. 필요할 때만 `references/`, `scripts/`, `assets/`를 추가한다.
5. 변경 후 감사 스크립트로 구조 점검을 실행한다.

## Output style

- 저장소 문서는 한국어 우선
- 파일 경로, 명령어, 식별자, API 이름은 원문 유지
- README에는 사용 예시를 남기되, 스킬 디렉토리 내부 문서는 최소화
