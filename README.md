# codex-skills-project

[![GitHub Repo](https://img.shields.io/badge/GitHub-oozoofrog/codex--skills--project-181717?logo=github)](https://github.com/oozoofrog/codex-skills-project)
[![Release](https://img.shields.io/github/v/release/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project/issues)
[![Repo Size](https://img.shields.io/github/repo-size/oozoofrog/codex-skills-project)](https://github.com/oozoofrog/codex-skills-project)

이 저장소는 **전역 Codex 스킬 소스 저장소**입니다.

핵심 의도는 다음과 같습니다.

- 스킬의 **authoring source**는 repo 안의 `.agents/skills/`
- 실제 사용은 `~/.codex/skills/`로 **전역 설치**
- repo를 직접 여는 방식은 **개발/검증용 보조 흐름**

즉, 이 저장소는 “repo-local workspace 자체”보다 **전역 스킬 배포 원본**에 더 가깝게 운영합니다.

## 빠른 시작

```bash
git clone https://github.com/oozoofrog/codex-skills-project.git
cd codex-skills-project
python3 scripts/install_global_skills.py --list
python3 scripts/install_global_skills.py
```

설치가 끝나면 **Codex를 재시작**하세요.

기본 설치 모드는 `copy`입니다.  
즉, `~/.codex/skills` 아래에 **직접 복사된 전역 스킬**이 생깁니다.

원본 저장소와 연결된 개발용 설치가 정말 필요할 때만 다음처럼 `symlink`를 명시적으로 사용하세요.

```bash
python3 scripts/install_global_skills.py --mode symlink --overwrite
```

## 설치 스크립트

전역 설치는 `scripts/install_global_skills.py`가 담당합니다.

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
python3 scripts/install_global_skills.py
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
- `gpt-research`
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

- [Codex Skills](https://developers.openai.com/codex/skills)
- [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [Codex Plugins](https://developers.openai.com/codex/plugins)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-codex-in-chatgpt)

## License

MIT
