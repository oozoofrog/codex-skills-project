#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG_PATH = ROOT / 'CHANGELOG.md'
VERSION_RE = re.compile(r'^v\d+\.\d+\.\d+$')


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def run(
    args: list[str],
    *,
    cwd: Path = ROOT,
    capture_output: bool = True,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        check=check,
        capture_output=capture_output,
        text=True,
    )


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(['git', *args], check=check)


def gh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(['gh', *args], check=check)


def ensure_version(version: str) -> None:
    if not VERSION_RE.match(version):
        raise SystemExit(f'오류: version 형식은 vX.Y.Z 여야 합니다: {version}')


def default_notes_path(version: str) -> Path:
    return ROOT / 'docs' / f'release-notes-{version}.md'


def default_announcement_path(version: str) -> Path:
    return ROOT / 'docs' / f'release-announcement-{version}.md'


def changelog_has_version(path: Path, version: str) -> bool:
    heading = f'## {version}'
    return heading in read_text(path)


def is_git_clean() -> bool:
    result = git('status', '--short')
    return not result.stdout.strip()


def current_branch() -> str:
    return git('branch', '--show-current').stdout.strip()


def local_tag_exists(version: str) -> bool:
    result = git('tag', '-l', version)
    return bool(result.stdout.strip())


def remote_tag_exists(version: str) -> bool:
    result = git('ls-remote', '--tags', 'origin', version, check=False)
    return result.returncode == 0 and bool(result.stdout.strip())


def ensure_gh_auth() -> None:
    result = gh('auth', 'status', check=False)
    if result.returncode != 0:
        raise SystemExit('오류: gh auth status 실패. GitHub CLI 인증이 필요합니다.')


def validate_release_inputs(
    *,
    version: str,
    notes_file: Path,
    changelog_file: Path,
    allow_dirty: bool,
    allow_existing_tag: bool,
    skip_gh_auth: bool,
) -> dict[str, object]:
    ensure_version(version)

    if not changelog_file.exists():
        raise SystemExit(f'오류: CHANGELOG 파일이 없습니다: {changelog_file}')
    if not changelog_has_version(changelog_file, version):
        raise SystemExit(f'오류: CHANGELOG에 `{version}` 헤더가 없습니다: {changelog_file}')

    if not notes_file.exists():
        raise SystemExit(f'오류: release notes 파일이 없습니다: {notes_file}')

    announcement_file = default_announcement_path(version)
    announcement_exists = announcement_file.exists()

    branch = current_branch()
    clean = is_git_clean()
    if not allow_dirty and not clean:
        raise SystemExit('오류: git 작업 트리가 깨끗하지 않습니다. 먼저 정리하거나 --allow-dirty를 사용하세요.')

    local_tag = local_tag_exists(version)
    remote_tag = remote_tag_exists(version)
    if not allow_existing_tag and (local_tag or remote_tag):
        where = []
        if local_tag:
            where.append('local')
        if remote_tag:
            where.append('remote')
        raise SystemExit(f'오류: 태그 `{version}` 가 이미 존재합니다 ({", ".join(where)}).')

    if not skip_gh_auth:
        ensure_gh_auth()

    return {
        'version': version,
        'notes_file': notes_file,
        'changelog_file': changelog_file,
        'announcement_file': announcement_file,
        'announcement_exists': announcement_exists,
        'branch': branch,
        'clean': clean,
        'local_tag_exists': local_tag,
        'remote_tag_exists': remote_tag,
    }


def print_summary(summary: dict[str, object]) -> None:
    print('# Release helper summary')
    print(f'- repo root: {ROOT}')
    print(f'- version: {summary["version"]}')
    print(f'- branch: {summary["branch"]}')
    print(f'- clean tree: {summary["clean"]}')
    print(f'- changelog: {summary["changelog_file"]}')
    print(f'- release notes: {summary["notes_file"]}')
    print(f'- announcement draft: {summary["announcement_file"]} (exists={summary["announcement_exists"]})')
    print(f'- local tag exists: {summary["local_tag_exists"]}')
    print(f'- remote tag exists: {summary["remote_tag_exists"]}')


def release_commands(version: str, notes_file: Path, *, draft: bool) -> list[list[str]]:
    commands = [
        ['git', 'switch', 'main'],
        ['git', 'pull', '--ff-only', 'origin', 'main'],
        ['git', 'push', 'origin', 'main'],
        ['git', 'tag', '-a', version, '-m', version],
        ['git', 'push', 'origin', version],
        ['gh', 'release', 'create', version, '--title', version, '--notes-file', str(notes_file.relative_to(ROOT))],
    ]
    if draft:
        commands[-1].append('--draft')
    return commands


def format_command(args: list[str]) -> str:
    return ' '.join(args)


def cmd_check(args: argparse.Namespace) -> int:
    summary = validate_release_inputs(
        version=args.version,
        notes_file=args.notes_file,
        changelog_file=args.changelog_file,
        allow_dirty=args.allow_dirty,
        allow_existing_tag=args.allow_existing_tag,
        skip_gh_auth=args.skip_gh_auth,
    )
    print_summary(summary)
    print('\n검증 통과.')
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    summary = validate_release_inputs(
        version=args.version,
        notes_file=args.notes_file,
        changelog_file=args.changelog_file,
        allow_dirty=args.allow_dirty,
        allow_existing_tag=args.allow_existing_tag,
        skip_gh_auth=args.skip_gh_auth,
    )
    print_summary(summary)
    print()
    print('# Planned commands')
    for command in release_commands(args.version, args.notes_file, draft=not args.publish_release):
        print(f'- {format_command(command)}')
    print()
    print('드라이런 완료: 실제 tag/release 생성은 하지 않았습니다.')
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    summary = validate_release_inputs(
        version=args.version,
        notes_file=args.notes_file,
        changelog_file=args.changelog_file,
        allow_dirty=False,
        allow_existing_tag=False,
        skip_gh_auth=False,
    )
    print_summary(summary)
    print()
    print('# Executing release commands')
    for command in release_commands(args.version, args.notes_file, draft=not args.publish_release):
        print(f'- {format_command(command)}')
        run(command, capture_output=False)
    print()
    if args.publish_release:
        print('릴리스 생성 완료.')
    else:
        print('draft GitHub Release 생성 완료.')
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='docs-first 저장소용 반복 가능한 릴리스 헬퍼',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    def add_common_flags(subparser: argparse.ArgumentParser, *, allow_publish_flags: bool) -> None:
        subparser.add_argument('--version', required=True, help='릴리스 버전 태그 (예: v0.2.2)')
        subparser.add_argument(
            '--notes-file',
            type=Path,
            help='릴리스 노트 파일 경로 (기본: docs/release-notes-<version>.md)',
        )
        subparser.add_argument(
            '--changelog-file',
            type=Path,
            default=CHANGELOG_PATH,
            help='CHANGELOG 파일 경로 (기본: CHANGELOG.md)',
        )
        if allow_publish_flags:
            subparser.add_argument(
                '--publish-release',
                action='store_true',
                help='기본 draft 대신 publish 상태로 GitHub Release를 생성합니다.',
            )
        else:
            subparser.add_argument('--allow-dirty', action='store_true', help='dirty working tree에서도 점검/계획을 허용합니다.')
            subparser.add_argument('--allow-existing-tag', action='store_true', help='기존 태그가 있어도 점검/계획을 허용합니다.')
            subparser.add_argument('--skip-gh-auth', action='store_true', help='gh auth status 점검을 건너뜁니다.')
            subparser.add_argument(
                '--publish-release',
                action='store_true',
                help='plan 출력 시 draft 대신 publish release 명령을 보여줍니다.',
            )

    check_parser = subparsers.add_parser('check', help='릴리스 입력과 guardrail을 점검합니다.')
    add_common_flags(check_parser, allow_publish_flags=False)
    check_parser.set_defaults(func=cmd_check)

    plan_parser = subparsers.add_parser('plan', help='릴리스 명령을 dry-run으로 출력합니다.')
    add_common_flags(plan_parser, allow_publish_flags=False)
    plan_parser.set_defaults(func=cmd_plan)

    publish_parser = subparsers.add_parser('publish', help='검증 후 tag push와 GitHub Release 생성을 실제 실행합니다.')
    add_common_flags(publish_parser, allow_publish_flags=True)
    publish_parser.set_defaults(func=cmd_publish)

    return parser


def normalize_paths(args: argparse.Namespace) -> None:
    if args.notes_file is None:
        args.notes_file = default_notes_path(args.version)
    if not args.notes_file.is_absolute():
        args.notes_file = (ROOT / args.notes_file).resolve()
    if not args.changelog_file.is_absolute():
        args.changelog_file = (ROOT / args.changelog_file).resolve()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    normalize_paths(args)
    return args.func(args)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f'오류: 명령 실패: {format_command(exc.cmd)}', file=sys.stderr)
        raise SystemExit(exc.returncode)
