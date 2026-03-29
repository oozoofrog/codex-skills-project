# v0.4.0 준비 상태

이 문서는 **후보 작업 목록**이 아니라, 현재 `main` 기준으로  
`v0.4.0` 준비 상태를 **완료 / 진행 기반 / 남은 후보**로 다시 정리한 상태판입니다.

기준:

- `v0.3.0` 공개 이후 main에 병합된 작업
- 현재 smoke / audit / packaged plugin 상태
- 다음에 실제로 착수 가치가 있는 남은 항목

## 현재 요약

`v0.4.0` 후보로 잡았던 큰 축은 상당 부분 main에 반영되었습니다.

완료된 축:

- release helper 도입 및 smoke / CI 연동
- global install validation regression automation
- packaged plugin parity 확장
  - `SKILL.md`
  - `openai.yaml`
  - single-skill manifest
  - multi-skill manifest
  - README / optional assets
- evaluator output contract / schema 기반 정리
- `agent-context-verify` deterministic script 추가
- `goal-research-loop` `reconcile` / `resume` / runtime status 보강
- local plugin testing 문서 단순화

즉, 남은 일은 **새 기반 작업**보다는 **세부 템플릿화 / 회귀 테스트 강화 / 반자동 UI 검증** 쪽에 가깝습니다.

---

## 완료된 항목

### 1. release / install / plugin parity 검증 자동화

- `scripts/release_helper.py`
- `scripts/run_release_smoke_checks.py`
- `scripts/run_global_install_smoke_checks.py`
- `scripts/run_local_plugin_smoke_checks.py`
- `.github/workflows/release-smoke.yml`
- `.github/workflows/install-smoke.yml`

효과:

- release / install / packaged plugin 레이어에 대해 CI 기준선을 확보
- draft/publish 분기, populated install, broken install 같은 회귀 포인트를 자동 점검

### 2. packaged plugin parity 확장

- `plugin-doctor` drift 검사 강화
- `scripts/packaged_plugin_parity.py`
- multi-skill plugin parity 규칙 반영
  - `agent-context`
  - `apple-craft`
- README / optional assets / screenshots parity 반영

효과:

- packaged/source drift의 사각지대가 크게 줄어듦
- generator가 만든 packaged outputs와 source skill metadata의 정합성이 높아짐

### 3. evaluator output 구조화

- `docs/evaluator-output-contract.md`
- `codex-skill-audit` schema + `--json-out`
- `plugin-doctor` schema + `--json-out`
- `agent-context-verify` schema + deterministic script

효과:

- 사람 읽기용 Markdown + machine summary JSON artifact 패턴이 정착
- evaluator-native skill 결과를 후속 자동화나 보고 흐름에 연결하기 쉬워짐

### 4. goal-research-loop runner 안정화

- `reconcile`
- `resume`
- `runtime/status.json`
- orphan round artifact 복구
- pending round 보호

효과:

- interrupted run 이후 이어받기 품질 개선
- round artifact를 덮어쓰는 위험 감소

### 5. local plugin testing 문서 단순화

- `docs/local-plugin-testing.md`
- `scripts/run_local_plugin_load_assistant.py` 문구 정렬

효과:

- 처음 해보는 사람용 quick path와 유지보수용 full path가 분리됨
- generated checklist와 문서 순서가 일치함

---

## 남은 후보

### 1. 도메인별 evaluator 템플릿 세분화

아직 남은 후보:

- `apple-review`
  - severity / file / impact / fix direction 형식 고정
- `agent-context-audit`
  - density / duplication / coverage 중심 템플릿 고정
- `plugin-doctor`
  - drift finding grouping / summary 포맷 고정
- `codex-skill-audit`
  - recommended fixes 생성 포맷 세분화

이유:

- 공통 contract는 생겼지만, 스킬별 특화 템플릿은 더 다듬을 수 있음

### 2. goal-research-loop 회귀 테스트 자동화

아직 남은 후보:

- timeout / interrupted turn fixture
- `prompt_profile=standard|lightweight` 차이 회귀 검증
- runtime status / ledger consistency regression test

이유:

- 기능은 들어갔지만, runner의 세부 회귀 테스트는 더 보강할 여지가 있음

### 3. local plugin UI 반자동 검증

아직 남은 후보:

- catalog 노출 여부 반자동 확인
- detail panel icon / logo / screenshots 확인 자동화
- starter prompt smoke 결과 구조화

이유:

- 정적 레이어는 강하지만 실제 UI 확인은 아직 사람이 많이 담당

---

## 현재 추천 우선순위

### P1

- 도메인별 evaluator 템플릿 세분화

### P2

- goal-research-loop 회귀 테스트 자동화

### P3

- local plugin UI 반자동 검증

---

## 운영 메모

- 현재 문서는 “남은 후보”만 보려는 사람에게 더 적합한 형태로 갱신된 상태판입니다.
- `v0.4.0`를 실제로 자를지 판단할 때는 이 문서와 현재 smoke/audit 결과를 함께 보는 편이 좋습니다.
