#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "오류: python3가 필요합니다." >&2
  exit 1
fi

echo "== Codex Skills 전역 설치 =="
echo "repo: $ROOT_DIR"
echo "mode: copy"
echo

python3 "$ROOT_DIR/scripts/install_global_skills.py" --overwrite "$@"

echo
echo "완료: Codex를 재시작하면 새 전역 스킬이 로드됩니다."
