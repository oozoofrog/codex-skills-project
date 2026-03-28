# codex-skills-project

[![GitHub Repo](https://img.shields.io/badge/GitHub-oozoofrog/codex--skills--project-181717?logo=github)](https://github.com/oozoofrog/codex-skills-project)
[![Release](https://img.shields.io/github/v/release/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/issues)
[![Repo Size](https://img.shields.io/github/repo-size/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project)

이 저장소는 **전역 Codex 스킬 소스 저장소**입니다.

핵심 의도는 다음과 같습니다.

- 스킬의 **authoring source**는 repo 안의 `.agents/skills/`
- 실제 사용은 `~/.codex/skills/`로 **전역 설치**
- repo를 직접 여는 방식은 **개발/검증용 보조 흐름**
- **검토는 가능하면 generator/evaluator 분리와 evidence 기반 harness로 수행**

즉, 이 저장소는 “repo-local workspace 자체”보다 **전역 스킬 배포 원본**에 더 가깝게 운영합니다.

## 빠른 링크

- Latest release: https://github.com/oozoofrog/codex-skills-project/releases/latest
- CHANGELOG: `CHANGELOG.md`
- v0.2.0 release notes: `docs/release-notes-v0.2.0.md`
- v0.2.0 announcement draft: `docs/release-announcement-v0.2.0.md`
- v0.3.0 candidate roadmap: `docs/roadmap-v0.3.0.md`

## 가장 쉬운 설치

```bash
git clone https://github.com/oozoofrog/codex-skills-project.git
cd codex-skills-project
./install.sh
```

설치가 끝나면 **Codex를 재시작**하세요.

기본 설치 모드는 `copy`입니다.  
즉, `~/.codex/skills` 아래에 **직접 복사된 전역 스킬**이 생깁니다.

업데이트도 같은 방식입니다.

```bash
cd codex-skills-project
git pull
./install.sh
```

macOS에서 터미널 명령보다 더 직관적인 방식을 원하면:

- Finder에서 `install.command`를 더블클릭

원본 저장소와 연결된 개발용 설치가 정말 필요할 때만 다음처럼 `symlink`를 명시적으로 사용하세요.

```bash
python3 scripts/install_global_skills.py --mode symlink --overwrite
```

## 설치 방식

### 일반 사용자

이 저장소를 쓰는 대부분의 경우는 아래만 기억하면 됩니다.

```bash
./install.sh
```

이 명령은 내부적으로 다음을 수행합니다.

- 전역 스킬을 `copy` 방식으로 설치
- 기존 이 저장소 버전이 있으면 덮어쓰기
- 설치가 끝나면 Codex 재시작만 남김

### 고급 사용자 / 수동 제어

더 세밀한 제어가 필요할 때만 `scripts/install_global_skills.py`를 직접 사용하세요.

기본 대상 경로:

- `~/.codex/skills`

지원 기능:

- 전체 스킬 일괄 설치
- 특정 스킬만 선택 설치
- 의존 스킬 자동 포함
- 기본 `copy` 설치
- 필요 시 명시적 `symlink` 모드 지원
- 이름 충돌 회피용 install alias 지원
- `--dry-run` 계획 확인

### 자주 쓰는 예시

#### 1. 전체 스킬 설치

```bash
./install.sh
```

기본값이 `copy`이므로 전역 스킬 디렉토리에 실제 파일이 복사됩니다.

#### 2. 특정 스킬만 설치

```bash
python3 scripts/install_global_skills.py apple-craft apple-review
```

`apple-review`는 `apple-craft` reference를 사용하므로, 의존성이 자동으로 함께 설치됩니다.

#### 3. 설치 계획만 미리 보기

```bash
python3 scripts/install_global_skills.py --dry-run
```

#### 4. 다른 대상 디렉토리에 테스트 설치

```bash
python3 scripts/install_global_skills.py --dest /tmp/codex-skills-test --mode copy
```

#### 5. 개발용 symlink 설치

```bash
python3 scripts/install_global_skills.py --mode symlink --overwrite
```

#### 6. 설치 목록 보기

```bash
python3 scripts/install_global_skills.py --list
```

## 충돌 정책

현재 확인된 전역 이름 충돌은 1개입니다.

- source skill: `macos-release`
- install name: `ooz-macos-release`

이 별칭은 Codex에 이미 있는 기본 제공 `macos-release`와 충돌하지 않기 위해 사용합니다.

관련 규칙은 다음 파일에 있습니다.

- `scripts/global_skills_manifest.json`

새 스킬을 추가할 때:

- 다른 전역 스킬과 이름이 겹치지 않는지 확인
- 겹치면 manifest에 `install_name` alias를 추가
- sibling reference가 있으면 `dependencies`도 같이 선언

## 포함 스킬

### Context / Structure

- `agent-context-guide`
- `agent-context-init`
- `agent-context-verify`
- `agent-context-audit`

### Apple / Automation

- `app-automation`
- `apple-craft`
- `apple-harness`
- `apple-review`
- `ooz-macos-release` *(source name: `macos-release`)*

### Bootstrap / Audit / Delegation

- `codex-skill-audit`
- `codex-skill-bootstrap`
- `gpt-research` — 외부 GPT/deep research로 넘길 프롬프트와 컨텍스트 패키지 생성
- `goal-research-loop` — objective 기반 반복 실험 루프 운영, contract/ledger/state snapshot 유지
- `hey-codex`
- `plugin-doctor`

## 저장소 구조

```text
codex-skills-project/
├── AGENTS.md
├── README.md
├── .agents/
│   └── skills/
│       ├── agent-context-audit/
│       ├── agent-context-guide/
│       ├── agent-context-init/
│       ├── agent-context-verify/
│       ├── app-automation/
│       ├── apple-craft/
│       ├── apple-harness/
│       ├── apple-review/
│       ├── codex-skill-audit/
│       ├── codex-skill-bootstrap/
│       ├── gpt-research/
│       ├── goal-research-loop/
│       ├── hey-codex/
│       ├── macos-release/
│       └── plugin-doctor/
├── .codex/
│   └── agents/
├── plugins/
└── scripts/
    ├── global_skills_manifest.json
    ├── install_global_skills.py
    └── ...
```

## 이 저장소의 두 가지 사용 방식

### 1. 기본 사용 방식: 전역 스킬 소스로 설치

이 방식이 **1순위**입니다.

- `.agents/skills`를 소스 오브 트루스로 유지
- `scripts/install_global_skills.py`로 `~/.codex/skills`에 반영
- Codex를 어느 프로젝트에서 열든 전역 스킬처럼 사용

### 2. 보조 사용 방식: 저장소 자체를 열어 개발/검증

이 방식은 다음 작업에만 권장합니다.

- 스킬 자체 수정
- reference/scripts 업데이트
- `.codex/agents` 실험
- packaged plugin 테스트

즉, repo-local 실행은 **개발자 워크벤치**이고, 최종 사용 경험은 **복사 기반 전역 설치**가 목표입니다.

## 보조 레이어

이 저장소에는 전역 스킬 외에 다음 레이어도 들어 있습니다.

### `AGENTS.md`

이 repo를 수정할 때 쓰는 **저장소 전용 작업 지침**입니다.  
최종 사용자가 전역 설치 후 각 프로젝트에서 쓰는 지침이 아니라, **이 스킬 저장소를 유지보수하기 위한 문서**입니다.

### `.codex/agents/`

일부 워크플로(`apple-harness`)를 위한 **project-scoped custom agent 예시**입니다.  
이 디렉토리는 전역 설치 대상이 아니며, 필요하면 각 프로젝트로 가져가서 쓰는 보조 자산입니다.

### `plugins/`

Codex plugin 패키징과 로컬 marketplace 테스트를 위한 **2차 실험 레이어**입니다.  
전역 스킬 배포가 1차 목적이고, plugin 패키징은 보조 목적입니다.

### Review Harness 공통 규약

이 저장소는 **literal GAN training**이 아니라 **GAN-inspired generator/evaluator harness**를 repo-wide convention으로 사용합니다.

- 공통 원칙: `docs/review-harness.md`
- 스킬별 매핑: `docs/review-harness-skill-matrix.md`
- 평가 루프 표준안: `docs/evaluation-loop-standard.md`
- 평가축/증거/자동 다음 행동 매트릭스: `docs/evaluation-loop-skill-matrix.md`
- `agents/openai.yaml` 규약: `docs/openai-yaml-conventions.md`

핵심은 다음과 같습니다.

- `SKILL.md`는 짧게 유지
- 고위험 쓰기 작업은 planner / generator / evaluator를 분리
- 검토는 가능하면 build/test/screenshot/audit script 같은 **외부 evidence**에 앵커링
- 감사/검증 스킬은 `mode: none`의 evaluator-native skill로 취급

## 유지보수 체크리스트

스킬을 바꿨다면 최소한 아래는 확인하는 것을 권장합니다.

```bash
python3 scripts/install_global_skills.py --dry-run
python3 scripts/install_global_skills.py --dest /tmp/codex-skills-test --mode copy
python3 .agents/skills/codex-skill-audit/scripts/audit_codex_skill_repo.py .
```

plugin 패키징까지 함께 건드렸다면:

```bash
python3 scripts/sync_packaged_plugins.py
python3 scripts/run_local_plugin_smoke_checks.py
```

## 공식 문서
### 테스트 가이드
- `docs/local-plugin-testing.md`
- `python3 scripts/update_browser_capture_assets.py <plugin-name> /path/to/browser-capture.png`

### 로컬 설치 테스트 메모

OpenAI Codex plugin 문서 기준으로 repo marketplace는 `$REPO_ROOT/.agents/plugins/marketplace.json`에 두고, 각 entry의 `source.path`는 marketplace root 기준 상대 경로 `./plugins/<plugin-name>`를 사용합니다. marketplace 또는 plugin 패키지를 갱신한 뒤에는 Codex를 재시작해서 카탈로그를 다시 읽게 하면 됩니다.

## 사용 예시

- “이 저장소 instruction 구조를 다시 짜줘” → `agent-context-guide`
- “AGENTS.md 체계를 자동으로 깔아줘” → `agent-context-init`
- “SwiftUI 빌드 에러를 잡아줘” → `apple-craft`
- “처음부터 설정 화면을 만들어줘” → `apple-harness`
- “PR #42를 Apple 관점에서 리뷰해줘” → `apple-review`
- “이 프로젝트를 외부 GPT 리서치용 프롬프트로 정리해줘” → `gpt-research`
- “목표를 두고 가설을 반복 검증하면서 best state를 찾아줘” → `goal-research-loop`
- “Codex CLI를 한 번 더 돌려서 세컨드 오피니언 받아와” → `hey-codex`
- “이 repo를 Codex plugin 관점에서 검사해줘” → `plugin-doctor`
- “새 스킬을 만들고 audit까지 끝내줘” → `codex-skill-bootstrap` → `codex-skill-audit`
- “AGENTS.md 구조를 고치고 검증까지 해줘” → `agent-context-init` → `agent-context-verify` / `agent-context-audit`


### 라이브 캡처 갱신

- `python3 scripts/update_live_capture_assets.py /path/to/codex-live-capture.png`

## 공식 문서

- [Codex Skills](https://developers.openai.com/codex/skills)
- [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [Codex Plugins](https://developers.openai.com/codex/plugins)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-codex-in-chatgpt)

## License

MIT
