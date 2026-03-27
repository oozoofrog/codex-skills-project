# AGENTS.md

## Repository purpose

이 저장소는 **전역 설치 가능한 Codex 스킬 소스 저장소**입니다.

- 스킬 authoring source는 `.agents/skills/`
- 실제 사용 경로는 `~/.codex/skills/`
- 설치 정책은 `scripts/install_global_skills.py` + `scripts/global_skills_manifest.json`
- repo-local `AGENTS.md`, `.codex/agents`, `plugins/`는 개발/검증용 보조 레이어

즉, 이 repo를 수정할 때는 항상 **“이 변경이 전역 설치 후에도 자연스럽게 동작하는가?”**를 먼저 기준으로 삼으세요.

## Working rules

- 새 스킬은 반드시 `.agents/skills/<skill-name>/SKILL.md` 아래에 둡니다.
- 스킬 이름은 kebab-case를 사용합니다.
- `SKILL.md` frontmatter에는 최소 `name`, `description`을 넣습니다.
- 긴 설명은 `references/`로 분리하고, `SKILL.md` 본문은 핵심 절차만 유지합니다.
- 스킬이 sibling reference를 사용하면 `scripts/global_skills_manifest.json`에 `dependencies`를 선언합니다.
- 전역 이름 충돌 가능성이 있으면 manifest에 `install_name` alias를 추가하거나, 의도적으로 source 이름을 조정합니다.
- 스킬은 **기본적으로 copy 방식으로 `~/.codex/skills`에 설치되었을 때** 자연스럽게 동작해야 합니다.
- `symlink` 모드는 개발 편의용 보조 옵션으로만 취급합니다.
- `.codex/agents`는 전역 설치 대상이 아니므로, 특정 프로젝트 전용 자산처럼 다룹니다.
- plugin 패키징 구조를 바꿀 때도 `.agents/skills`가 여전히 source of truth인지 유지합니다.

## Preferred workflow

1. 먼저 `.agents/skills/<skill>/SKILL.md`와 관련 references/scripts를 수정한다.
2. 필요하면 `scripts/global_skills_manifest.json`의 dependency / alias를 같이 갱신한다.
3. `python3 scripts/install_global_skills.py --dry-run`으로 설치 계획을 확인한다.
4. 필요하면 `python3 scripts/install_global_skills.py --dest /tmp/codex-skills-test --mode copy --overwrite`로 테스트 설치한다.
5. 마지막에 `codex-skill-audit` 기준 구조 점검을 실행한다.
6. plugin 관련 변경이 있으면 별도로 `scripts/sync_packaged_plugins.py`와 smoke check를 실행한다.

## Output style

- 저장소 문서는 한국어 우선
- 파일 경로, 명령어, 식별자, API 이름은 원문 유지
- README는 전역 설치 사용자 흐름을 먼저 설명
- repo-local 실행법은 개발/검증용 보조 흐름으로 설명
