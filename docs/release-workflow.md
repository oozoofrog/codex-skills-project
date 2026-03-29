# Release workflow

이 저장소의 릴리스는 **docs-first** 흐름을 기본값으로 사용합니다.

즉, 먼저 아래 산출물을 준비합니다.

- `CHANGELOG.md`에 `## vX.Y.Z` 항목
- `docs/release-notes-vX.Y.Z.md`
- 필요 시 `docs/release-announcement-vX.Y.Z.md`

그 다음에 tag / GitHub Release를 만듭니다.

## 최소 지원 흐름

### 1. 사전 점검

```bash
python3 scripts/release_helper.py check --version v0.2.2
```

이 단계는 최소한 아래를 확인합니다.

- 버전 형식이 `vX.Y.Z`인지
- `CHANGELOG.md`에 해당 버전 헤더가 있는지
- `docs/release-notes-vX.Y.Z.md`가 있는지
- git working tree가 깨끗한지
- tag가 이미 존재하는지
- `gh auth status`가 통과하는지

### 2. dry-run 계획 확인

```bash
python3 scripts/release_helper.py plan --version v0.2.2
```

이 명령은 실제 변경 없이 아래 흐름을 출력합니다.

- `git switch main`
- `git pull --ff-only origin main`
- `git push origin main`
- `git tag -a vX.Y.Z -m vX.Y.Z`
- `git push origin vX.Y.Z`
- `gh release create vX.Y.Z --title vX.Y.Z --notes-file docs/release-notes-vX.Y.Z.md --draft`

기본값은 **draft GitHub Release** 기준입니다.

공개 릴리스 기준 명령을 보고 싶으면:

```bash
python3 scripts/release_helper.py plan --version v0.2.2 --publish-release
```

### 3. 실제 실행

draft Release 생성:

```bash
python3 scripts/release_helper.py publish --version v0.2.2
```

공개 Release 생성:

```bash
python3 scripts/release_helper.py publish --version v0.2.2 --publish-release
```

## 안전장치

- `publish`는 항상 검증을 먼저 통과해야 합니다.
- `publish`는 dirty working tree에서 실행되지 않습니다.
- 기존 local/remote tag가 이미 있으면 중단합니다.
- 기본 출력은 draft Release 기준이라 실수로 바로 공개되지 않게 설계했습니다.

## 선택 플래그

기존 릴리스 문서를 점검만 하고 싶을 때:

```bash
python3 scripts/release_helper.py plan \
  --version v0.2.1 \
  --allow-existing-tag \
  --allow-dirty
```

`check` / `plan`에서는 아래 우회 플래그를 사용할 수 있습니다.

- `--allow-dirty`
- `--allow-existing-tag`
- `--skip-gh-auth`

이 플래그들은 **점검/계획용**이고, 실제 `publish`에는 적용되지 않습니다.

## 현재 저장소에서 권장하는 사용 순서

1. `CHANGELOG.md`와 `docs/release-notes-vX.Y.Z.md` 준비
2. `python3 scripts/release_helper.py check --version vX.Y.Z`
3. `python3 scripts/release_helper.py plan --version vX.Y.Z`
4. draft가 필요하면 `publish`
5. 공개 시점에 `--publish-release`
