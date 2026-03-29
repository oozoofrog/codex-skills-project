#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = ROOT / '.agents' / 'skills'
MANIFEST_PATH = ROOT / 'scripts' / 'global_skills_manifest.json'
DEFAULT_DEST = Path.home() / '.codex' / 'skills'


@dataclass(frozen=True)
class SkillSpec:
    source: str
    install_name: str
    description: str
    dependencies: tuple[str, ...] = ()
    alias_reason: str | None = None


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = read_text(path).splitlines()
    data: dict[str, str] = {}
    if not lines or lines[0].strip() != '---':
        return data
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        data[key.strip()] = value.strip()
    return data


def replace_frontmatter_name(text: str, new_name: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        raise ValueError('SKILL.md frontmatter가 없습니다.')

    updated = False
    for idx in range(1, len(lines)):
        if lines[idx].strip() == '---':
            break
        if lines[idx].startswith('name:'):
            lines[idx] = f'name: {new_name}'
            updated = True
            break
    if not updated:
        raise ValueError('SKILL.md frontmatter에 name 필드가 없습니다.')
    return '\n'.join(lines) + ('\n' if text.endswith('\n') else '')


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def load_manifest() -> list[SkillSpec]:
    raw = json.loads(read_text(MANIFEST_PATH))
    specs: list[SkillSpec] = []
    seen_sources: set[str] = set()
    seen_install_names: set[str] = set()

    for item in raw.get('skills', []):
        source = item['source']
        if source in seen_sources:
            raise ValueError(f'manifest source 중복: {source}')
        seen_sources.add(source)

        skill_dir = SOURCE_ROOT / source
        skill_md = skill_dir / 'SKILL.md'
        if not skill_dir.is_dir() or not skill_md.is_file():
            raise ValueError(f'소스 스킬이 없습니다: {source}')

        install_name = item.get('install_name', source)
        if install_name in seen_install_names:
            raise ValueError(f'install_name 중복: {install_name}')
        seen_install_names.add(install_name)

        fm = parse_frontmatter(skill_md)
        description = item.get('description') or fm.get('description', '')
        specs.append(
            SkillSpec(
                source=source,
                install_name=install_name,
                description=description,
                dependencies=tuple(item.get('dependencies', [])),
                alias_reason=item.get('alias_reason'),
            )
        )

    return specs


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if path.exists():
        shutil.rmtree(path)


def ensure_supported_mode(mode: str) -> None:
    if mode not in {'copy', 'symlink'}:
        raise ValueError(f'지원하지 않는 mode: {mode}')


def install_copy(spec: SkillSpec, dest_root: Path) -> Path:
    src_dir = SOURCE_ROOT / spec.source
    dest_dir = dest_root / spec.install_name
    shutil.copytree(src_dir, dest_dir)
    if spec.install_name != spec.source:
        skill_md = dest_dir / 'SKILL.md'
        skill_md.write_text(
            replace_frontmatter_name(read_text(skill_md), spec.install_name),
            encoding='utf-8',
        )
    return dest_dir


def install_symlink(spec: SkillSpec, dest_root: Path) -> Path:
    src_dir = SOURCE_ROOT / spec.source
    dest_dir = dest_root / spec.install_name

    if spec.install_name == spec.source:
        dest_dir.symlink_to(src_dir, target_is_directory=True)
        return dest_dir

    dest_dir.mkdir(parents=True, exist_ok=False)
    for child in src_dir.iterdir():
        target = dest_dir / child.name
        if child.name == 'SKILL.md':
            target.write_text(
                replace_frontmatter_name(read_text(child), spec.install_name),
                encoding='utf-8',
            )
            continue
        target.symlink_to(child, target_is_directory=child.is_dir())
    return dest_dir


def validate_install(spec: SkillSpec, dest_dir: Path) -> None:
    skill_md = dest_dir / 'SKILL.md'
    if not skill_md.is_file():
        raise ValueError(f'SKILL.md 누락: {dest_dir}')
    fm = parse_frontmatter(skill_md)
    if fm.get('name') != spec.install_name:
        raise ValueError(
            f'frontmatter name 불일치: expected={spec.install_name} actual={fm.get("name")}'
        )
    if not fm.get('description'):
        raise ValueError(f'frontmatter description 누락: {skill_md}')


def format_plan_status(dest_dir: Path, *, overwrite: bool, dry_run: bool) -> str:
    if not path_exists(dest_dir):
        return ' [new]'
    if dry_run:
        if overwrite:
            return ' [exists; dry-run would replace]'
        return ' [exists; dry-run only, real install needs --overwrite]'
    if overwrite:
        return ' [exists; will replace]'
    return ' [exists; install will fail without --overwrite]'


def validate_installed_tree(
    selected_specs: list[SkillSpec],
    *,
    all_specs: list[SkillSpec],
    dest_root: Path,
) -> None:
    if not dest_root.exists():
        raise ValueError(f'설치 대상 디렉토리가 없습니다: {dest_root}')

    by_source = {spec.source: spec for spec in all_specs}
    problems: list[str] = []

    print('# Installed skill validation')
    print(f'- destination: {dest_root}')
    print(f'- selected: {", ".join(spec.install_name for spec in selected_specs)}')

    for spec in selected_specs:
        dest_dir = dest_root / spec.install_name
        notes = ['frontmatter: ok']
        if spec.install_name != spec.source:
            notes.append(f'alias: {spec.source} -> {spec.install_name}')

        try:
            if not path_exists(dest_dir):
                raise ValueError(f'설치 경로 누락: {dest_dir}')
            validate_install(spec, dest_dir)

            if spec.dependencies:
                dep_labels: list[str] = []
                for dep_source in spec.dependencies:
                    dep_spec = by_source[dep_source]
                    dep_dir = dest_root / dep_spec.install_name
                    if not path_exists(dep_dir):
                        raise ValueError(
                            f'dependency 누락: {spec.install_name} requires {dep_spec.install_name}'
                        )
                    dep_labels.append(dep_spec.install_name)
                notes.append(f'deps: {", ".join(dep_labels)}')
            else:
                notes.append('deps: -')

            print(f'  - OK {dest_dir} [{"; ".join(notes)}]')
        except Exception as exc:
            problems.append(str(exc))
            print(f'  - FAIL {dest_dir} [{exc}]')

    if problems:
        raise ValueError('설치 검증 실패:\n- ' + '\n- '.join(problems))


def build_lookup(specs: list[SkillSpec]) -> tuple[dict[str, SkillSpec], dict[str, SkillSpec]]:
    by_source = {spec.source: spec for spec in specs}
    by_install_name = {spec.install_name: spec for spec in specs}
    return by_source, by_install_name


def resolve_requested_sources(
    requested_tokens: list[str],
    specs: list[SkillSpec],
) -> list[str]:
    by_source, by_install_name = build_lookup(specs)
    if not requested_tokens:
        return [spec.source for spec in specs]

    resolved: list[str] = []
    for token in requested_tokens:
        if token in by_source:
            resolved.append(token)
            continue
        if token in by_install_name:
            resolved.append(by_install_name[token].source)
            continue
        raise ValueError(f'알 수 없는 skill 이름: {token}')
    return resolved


def expand_dependencies(requested_sources: list[str], specs: list[SkillSpec]) -> list[SkillSpec]:
    by_source = {spec.source: spec for spec in specs}
    expanded: set[str] = set()
    visiting: set[str] = set()

    def visit(source: str) -> None:
        if source in expanded:
            return
        if source in visiting:
            chain = ' -> '.join([*sorted(visiting), source])
            raise ValueError(f'dependency cycle 감지: {chain}')
        if source not in by_source:
            raise ValueError(f'manifest에 없는 dependency: {source}')

        visiting.add(source)
        for dep in by_source[source].dependencies:
            visit(dep)
        visiting.remove(source)
        expanded.add(source)

    for source in requested_sources:
        visit(source)

    return [spec for spec in specs if spec.source in expanded]


def format_specs(specs: list[SkillSpec]) -> str:
    rows = []
    for spec in specs:
        deps = ', '.join(spec.dependencies) if spec.dependencies else '-'
        install = spec.install_name
        if spec.install_name != spec.source:
            install = f'{install} (alias)'
        rows.append((spec.source, install, deps, spec.description))

    widths = [
        max(len('source'), *(len(row[0]) for row in rows)),
        max(len('install'), *(len(row[1]) for row in rows)),
        max(len('deps'), *(len(row[2]) for row in rows)),
    ]

    lines = [
        f'{"source".ljust(widths[0])}  {"install".ljust(widths[1])}  {"deps".ljust(widths[2])}  description',
        f'{"-" * widths[0]}  {"-" * widths[1]}  {"-" * widths[2]}  -----------',
    ]
    for source, install, deps, description in rows:
        lines.append(
            f'{source.ljust(widths[0])}  {install.ljust(widths[1])}  {deps.ljust(widths[2])}  {description}'
        )
    return '\n'.join(lines)


def install_selected(
    selected_specs: list[SkillSpec],
    *,
    dest_root: Path,
    mode: str,
    overwrite: bool,
    dry_run: bool,
) -> None:
    ensure_supported_mode(mode)
    if not dry_run:
        dest_root.mkdir(parents=True, exist_ok=True)

    for spec in selected_specs:
        dest_dir = dest_root / spec.install_name
        if path_exists(dest_dir):
            if dry_run:
                continue
            if not overwrite:
                raise FileExistsError(
                    f'이미 존재하는 설치 경로: {dest_dir} (덮어쓰려면 --overwrite 사용)'
                )
            remove_existing(dest_dir)

        if dry_run:
            continue

        if mode == 'copy':
            installed_dir = install_copy(spec, dest_root)
        else:
            installed_dir = install_symlink(spec, dest_root)
        validate_install(spec, installed_dir)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Install repo-local source skills into ~/.codex/skills for global Codex usage.'
    )
    parser.add_argument(
        'skills',
        nargs='*',
        help='설치할 source 이름 또는 install 이름. 비우면 manifest의 전체 스킬을 설치합니다.',
    )
    parser.add_argument(
        '--dest',
        default=str(DEFAULT_DEST),
        help='설치 대상 디렉토리 (기본값: ~/.codex/skills)',
    )
    parser.add_argument(
        '--mode',
        choices=['copy', 'symlink'],
        default='copy',
        help='설치 방식 (기본값: copy)',
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='기존 설치 경로가 있으면 덮어씁니다.',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 설치 없이 계획만 출력합니다.',
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='manifest 기준 설치 가능한 스킬 목록을 출력합니다.',
    )
    parser.add_argument(
        '--validate-installed',
        action='store_true',
        help='설치 대상 디렉토리의 alias/dependency/frontmatter 상태를 검증합니다.',
    )
    args = parser.parse_args()

    specs = load_manifest()

    if args.list:
        print(format_specs(specs))
        print('\n주의: `macos-release`는 기본 제공 스킬과 충돌을 피하기 위해 `ooz-macos-release`로 설치됩니다.')
        return 0

    requested_sources = resolve_requested_sources(args.skills, specs)
    selected_specs = expand_dependencies(requested_sources, specs)
    dest_root = Path(args.dest).expanduser().resolve()

    if args.validate_installed and args.dry_run:
        raise ValueError('--validate-installed와 --dry-run은 함께 사용할 수 없습니다.')

    if args.validate_installed:
        validate_installed_tree(
            selected_specs,
            all_specs=specs,
            dest_root=dest_root,
        )
        print('\n설치 검증 완료.')
        return 0

    print(f'# Global skill install plan')
    print(f'- repo root: {ROOT}')
    print(f'- source root: {SOURCE_ROOT}')
    print(f'- destination: {dest_root}')
    print(f'- mode: {args.mode}')
    print(f'- overwrite: {args.overwrite}')
    print(f'- dry-run: {args.dry_run}')
    print(f'- selected: {", ".join(spec.install_name for spec in selected_specs)}')

    for spec in selected_specs:
        dest_dir = dest_root / spec.install_name
        alias_note = f' [alias: {spec.source}]' if spec.install_name != spec.source else ''
        dep_note = (
            f' [deps: {", ".join(spec.dependencies)}]'
            if spec.dependencies
            else ''
        )
        status_note = format_plan_status(
            dest_dir,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
        print(f'  - {dest_dir}{alias_note}{dep_note}{status_note}')
        if spec.alias_reason:
            print(f'    ↳ {spec.alias_reason}')

    install_selected(
        selected_specs,
        dest_root=dest_root,
        mode=args.mode,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print('\n드라이런 완료: 실제 파일 변경은 없었습니다.')
        return 0

    print('\n설치 완료. Codex를 재시작해서 새 전역 스킬을 다시 로드하세요.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f'오류: {exc}', file=sys.stderr)
        raise SystemExit(1)
