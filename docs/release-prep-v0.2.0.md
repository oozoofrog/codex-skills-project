# Release Prep Draft — v0.2.0

기준일: 2026-03-28  
현재 최신 공개 릴리스: `v0.1.0`  
권장 다음 버전: **`v0.2.0`**

## 왜 `v0.2.0`인가

`v0.1.0` 이후 변화는 단순 문구 수정 수준을 넘어섭니다.

- 전역 스킬 설치 흐름 단순화
- review harness 공통 규약 추가
- Anthropic harness 글 기반 평가 루프 표준안 추가
- 스킬별 평가축 / 증거 / 자동 다음 행동 매트릭스 추가
- `agents/openai.yaml` 규칙 강화
- packaged plugins / marketplace metadata 동기화

즉, 사용자에게 보이는 운영 모델과 저장소 유지보수 규약이 확장되었으므로 patch보다 **minor bump**가 더 자연스럽습니다.

## 변경 요약

### 1. 전역 설치 흐름 정리
- 저장소를 repo-local workspace 중심 설명에서 **전역 Codex 스킬 소스 저장소** 관점으로 더 명확히 정리
- 기본 설치 경로와 `copy` 중심 설치 흐름 명확화

### 2. Review Harness 규약 도입
- repo-wide `Review Harness` convention 추가
- 각 스킬에 `Review Harness` 선언 추가
- `mode: none / optional / required` 운용 정리

### 3. Anthropic 기반 평가 루프 표준화
- 평가 루프 표준안 문서 추가
- 상태 전이:
  - `pass`
  - `refine`
  - `pivot`
  - `rescope`
  - `escalate`
  - `stop`
- evidence-first 평가 원칙 정리

### 4. 스킬별 운영 매트릭스 추가
- 각 스킬에 대해
  - 평가축
  - 증거
  - 자동 다음 행동
  을 문서화

### 5. `agents/openai.yaml` 규칙 강화
- explicit-only 스킬의 `allow_implicit_invocation: false` 원칙 명확화
- `default_prompt`, `short_description` 작성 기준 강화
- audit 스크립트와 체크리스트에 반영

### 6. packaged plugins 동기화
- local marketplace metadata 갱신
- packaged skill 복제본까지 Review Harness 설명 동기화
- generated preview assets 재생성

## Release notes draft

```md
## v0.2.0

This release expands the repository from a basic Codex skill workspace into a more explicit, evidence-driven operating model for skill evaluation and long-running automation.

### Highlights
- Simplified the global Codex skill installation workflow
- Added repo-wide Review Harness conventions
- Added evaluation loop standards derived from Anthropic's harness design article
- Added per-skill matrices for evaluation criteria, evidence, and automatic next actions
- Tightened `agents/openai.yaml` conventions and audit coverage
- Synced packaged plugins and marketplace metadata with the new review/evidence model

### Recommended validation
```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```
```

## 검증 상태

확인한 항목:

```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```

요약:
- skill audit findings 0
- plugin-doctor findings 0
- packaged plugins 7개 재생성 완료
- JSON / asset / manifest path 검증 통과

## 태그/릴리스 실행 순서 제안

아직 실제 태그/릴리스는 만들지 않았습니다. 아래 순서를 권장합니다.

### 1. 태그 생성

```bash
git checkout main
git pull --ff-only origin main
git tag -a v0.2.0 -m "v0.2.0"
git push origin v0.2.0
```

### 2. GitHub Release 초안 생성

`gh` 사용 예시:

```bash
gh release create v0.2.0 \
  --title "v0.2.0" \
  --notes-file docs/release-prep-v0.2.0.md
```

실제 게시 시에는 위 `Release notes draft` 블록만 따로 정리해 넣는 편을 권장합니다.

## 관련 커밋

`v0.1.0` 이후 주요 커밋:

- `5f84661` Add review harness conventions and evaluation loop standards
- `4d6e27b` Simplify global Codex skill installation
- `d7ee161` docs: clarify usage surfaces and privacy hygiene

## 참고 문서

- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`
- `docs/evaluation-loop-standard.md`
- `docs/evaluation-loop-skill-matrix.md`
- `docs/openai-yaml-conventions.md`
