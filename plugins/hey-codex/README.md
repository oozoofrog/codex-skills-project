# hey-codex

Local plugin package for explicit second-opinion Codex CLI delegation.

## Included skills

- `hey-codex`

## Packaged assets

- `assets/icon.svg` / `assets/icon.png`
- `assets/logo.svg` / `assets/logo.png`
- `assets/screenshot.svg` / `assets/screenshot.png`
- `assets/browser-capture.png` (external browser render capture)
- `assets/live-capture.png` (actual Codex UI capture)

## Notes

- This directory is generated from repo-local skills in `.agents/skills/`.
- Packaged skills may include `Review Harness` sections that describe generator/evaluator roles and evidence expectations.
- Regenerate packaged plugins with `python3 scripts/sync_packaged_plugins.py`.
- Validate with `python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .`.
- Follow `docs/local-plugin-testing.md` for local loading checks.
- Run `python3 scripts/run_local_plugin_smoke_checks.py` for static smoke checks.
- `assets/screenshot.png`는 representative preview입니다.
- `assets/browser-capture.png`가 있으면 외부 브라우저에서 렌더링한 실제 detail/gallery 캡처를 함께 제공합니다.
- `assets/live-capture.png`가 있으면 현재 repo의 actual Codex UI capture를 함께 제공합니다.
