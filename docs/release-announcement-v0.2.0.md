# v0.2.0 발표문 초안

`codex-skills-project` **v0.2.0**을 배포했습니다.

이번 릴리스의 핵심은 저장소를 단순한 Codex skill 모음에서, **평가와 자동 진행까지 명시된 운영 모델**로 확장한 것입니다.

## 무엇이 달라졌나

- 전역 Codex 스킬 설치 흐름을 더 명확히 정리했습니다.
- repo-wide `Review Harness` 규약을 도입했습니다.
- Anthropic의 *Harness design for long-running application development* 글을 바탕으로 평가 루프 표준안을 추가했습니다.
- 각 스킬에 대해 **평가축 / 증거 / 자동 다음 행동** 매트릭스를 문서화했습니다.
- `agents/openai.yaml` 작성 규칙과 audit 검사를 강화했습니다.
- packaged plugins와 marketplace metadata를 review/evidence 모델에 맞춰 동기화했습니다.

## 새로 추가된 핵심 문서

- `docs/review-harness.md`
- `docs/review-harness-skill-matrix.md`
- `docs/openai-yaml-conventions.md`
- `docs/evaluation-loop-standard.md`
- `docs/evaluation-loop-skill-matrix.md`
- `CHANGELOG.md`

## 왜 중요한가

이번 변화로 각 스킬은 단순히 “무엇을 하는가”를 넘어서,

- 무엇을 평가하는지
- 어떤 증거를 보는지
- 평가 후 다음 행동이 무엇인지

를 더 명확하게 드러내게 되었습니다.

즉, **GAN-inspired harness**라는 표현을 실무적으로 풀어서,
실제 저장소 운영에서 쓸 수 있는 **planner / generator / evaluator + evidence-first loop**로 구체화한 릴리스입니다.

## 검증

```bash
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py --skip-regenerate
python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .
```

## 링크

- Release: https://github.com/oozoofrog/codex-skills-project/releases/tag/v0.2.0
- CHANGELOG: `CHANGELOG.md`
