#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / '.agents' / 'skills'
PLUGINS_ROOT = ROOT / 'plugins'
MARKETPLACE_PATH = ROOT / '.agents' / 'plugins' / 'marketplace.json'
LIVE_CAPTURE_SOURCE = ROOT / 'assets' / 'live-captures' / 'codex-live-capture.png'
BROWSER_CAPTURE_DIR = ROOT / 'assets' / 'browser-captures'

PLUGIN_SPECS = [
    {
        'name': 'agent-context',
        'version': '1.4.0',
        'description': 'Layered AGENTS.md instruction architecture for Codex repositories.',
        'skills': ['agent-context-guide', 'agent-context-init', 'agent-context-verify', 'agent-context-audit'],
        'keywords': ['agents-md', 'context', 'documentation', 'architecture'],
        'color': '#2563EB',
        'accent': '#60A5FA',
        'glyph': 'AC',
        'highlights': ['Root + nested AGENTS.md', 'Instruction drift verification', 'Coverage and duplication audit'],
        'interface': {
            'displayName': 'Agent Context',
            'shortDescription': 'Layered AGENTS.md design and verification',
            'longDescription': 'Scaffold, validate, and audit layered Codex instruction architectures with root and nested AGENTS.md files plus lightweight supporting docs.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Scaffold', 'Read', 'Write', 'Validate'],
            'defaultPrompt': [
                'Analyze this repository and propose a layered AGENTS.md structure.',
                'Scaffold AGENTS.md and nested instruction files for this repo.',
                'Verify whether the current AGENTS.md files still match the codebase.',
            ],
        },
        'readme': 'Codex instruction architecture tools packaged for local marketplace testing.',
    },
    {
        'name': 'app-automation',
        'version': '1.0.0',
        'description': 'Automate iOS Simulator and macOS apps with baepsae MCP tooling.',
        'skills': ['app-automation'],
        'keywords': ['automation', 'simulator', 'macos', 'baepsae'],
        'color': '#0EA5E9',
        'accent': '#67E8F9',
        'glyph': 'AA',
        'highlights': ['UI tree inspection', 'Repeatable run_steps flows', 'Screenshots and video capture'],
        'mcp_servers': {
            'mcpServers': {
                'baepsae': {
                    'command': '/bin/bash',
                    'args': ['-l', '-c', 'exec npx -y mcp-baepsae@latest'],
                }
            }
        },
        'interface': {
            'displayName': 'App Automation',
            'shortDescription': 'Automate iOS Simulator and macOS apps',
            'longDescription': 'Inspect UI trees, interact with simulator or macOS apps, capture screenshots, and run repeatable automation flows with baepsae.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Automation', 'UI', 'Screenshots', 'MCP'],
            'defaultPrompt': [
                'Analyze the current simulator UI tree and tell me what is visible.',
                'Launch the app in the booted simulator and capture a screenshot.',
                'Automate a login flow and report where it fails.',
            ],
        },
        'readme': 'Local plugin package for simulator and macOS automation with baepsae.',
    },
    {
        'name': 'apple-craft',
        'version': '1.9.2',
        'description': 'Apple platform development with Xcode tools, bundled references, and review workflows.',
        'skills': ['apple-craft', 'apple-harness', 'apple-review'],
        'keywords': ['swift', 'swiftui', 'uikit', 'xcode', 'apple'],
        'color': '#7C3AED',
        'accent': '#C4B5FD',
        'glyph': 'AP',
        'highlights': ['Xcode diagnostics + previews', 'Bundled Apple reference docs', 'Review and harness workflows'],
        'interface': {
            'displayName': 'Apple Craft',
            'shortDescription': 'Swift, SwiftUI, UIKit, and Xcode support',
            'longDescription': 'Build, troubleshoot, review, and orchestrate Apple platform work using Xcode tools plus bundled reference docs for current Apple APIs.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Swift', 'Xcode', 'Review', 'Planning'],
            'defaultPrompt': [
                'Diagnose this SwiftUI build error and suggest the minimal fix.',
                'Review this branch for Apple-platform-specific correctness risks.',
                'Plan and implement a new Apple feature with a spec and evaluation loop.',
            ],
        },
        'readme': 'Local plugin package for Apple platform development and review workflows.',
    },
    {
        'name': 'gpt-research',
        'version': '1.0.1',
        'description': 'Extract structured prompts for external GPT and deep research workflows.',
        'skills': ['gpt-research'],
        'keywords': ['research', 'prompt', 'context', 'analysis'],
        'color': '#14B8A6',
        'accent': '#5EEAD4',
        'glyph': 'GR',
        'highlights': ['Module / arch / issue modes', 'Prompt-ready context extraction', 'Chunking-aware handoff templates'],
        'interface': {
            'displayName': 'GPT Research',
            'shortDescription': 'Prepare structured prompts for external research',
            'longDescription': 'Collect the right repository context and format it into reusable prompts for external GPT or deep research workflows.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Research', 'Prompting', 'Context'],
            'defaultPrompt': [
                'Generate a module-focused research prompt for this directory.',
                'Prepare an architecture research prompt for the whole repository.',
                'Turn this error and its related files into a deep-research handoff.',
            ],
        },
        'readme': 'Local plugin package for external GPT or deep research prompt generation.',
    },
    {
        'name': 'hey-codex',
        'version': '1.1.0',
        'description': 'Delegate selected tasks to a separate Codex CLI invocation when explicitly requested.',
        'skills': ['hey-codex'],
        'keywords': ['codex', 'delegation', 'cli', 'review'],
        'color': '#F97316',
        'accent': '#FDBA74',
        'glyph': 'HC',
        'highlights': ['Separate Codex CLI runs', 'Read / review / suggest / write routing', 'Diff-aware result handoff'],
        'interface': {
            'displayName': 'Hey Codex',
            'shortDescription': 'Run a separate Codex CLI task on demand',
            'longDescription': 'Invoke a second Codex CLI process for isolated read-only analysis, review, suggestions, or carefully scoped full-auto runs when the user explicitly asks.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Delegation', 'CLI', 'Review'],
            'defaultPrompt': [
                'Ask a separate Codex CLI run for a second opinion on this refactor.',
                'Run a read-only Codex review on the current branch.',
                'Delegate this task to another Codex process and summarize the result.',
            ],
        },
        'readme': 'Local plugin package for explicit second-opinion Codex CLI delegation.',
    },
    {
        'name': 'macos-release',
        'version': '1.0.0',
        'description': 'Automate macOS app and CLI release preparation, packaging, and publishing.',
        'skills': ['macos-release'],
        'keywords': ['release', 'macos', 'packaging', 'homebrew'],
        'color': '#EF4444',
        'accent': '#FCA5A5',
        'glyph': 'MR',
        'highlights': ['Version bump to publish flow', 'Packaging + local install validation', 'GitHub Release and Homebrew support'],
        'interface': {
            'displayName': 'macOS Release',
            'shortDescription': 'Prepare and publish macOS releases',
            'longDescription': 'Guide or automate version bumps, builds, packaging, local install verification, GitHub Releases, and Homebrew publishing for macOS software.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Release', 'Build', 'Packaging'],
            'defaultPrompt': [
                'Prepare a dry-run release plan for this macOS app.',
                'Review this repository for missing release automation steps.',
                'Set up a release script for build, DMG, GitHub Release, and Homebrew.',
            ],
        },
        'readme': 'Local plugin package for macOS release automation workflows.',
    },
    {
        'name': 'plugin-doctor',
        'version': '1.0.1',
        'description': 'Audit Codex plugin, custom-agent, and skill repositories for structural issues.',
        'skills': ['plugin-doctor'],
        'keywords': ['plugins', 'audit', 'metadata', 'validation'],
        'color': '#6366F1',
        'accent': '#A5B4FC',
        'glyph': 'PD',
        'highlights': ['Marketplace ↔ package cross-checks', 'Manifest, asset, and path validation', 'Claude artifact drift detection'],
        'interface': {
            'displayName': 'Plugin Doctor',
            'shortDescription': 'Audit Codex plugin and skill repositories',
            'longDescription': 'Validate repo-local skills, optional packaged plugins, marketplace metadata, and custom agents while flagging stale Claude-specific leftovers.',
            'developerName': 'codex-skills-project',
            'category': 'Productivity',
            'capabilities': ['Audit', 'Validation', 'Metadata'],
            'defaultPrompt': [
                'Audit this repository for Codex plugin and skill structure issues.',
                'Check whether packaged plugins and marketplace metadata are consistent.',
                'Find stale Claude-specific artifacts that should be removed or documented.',
            ],
        },
        'readme': 'Local plugin package for Codex plugin and skill repository audits.',
    },
]


def copy_skill(src_name: str, dst_root: Path) -> None:
    src = SKILLS_ROOT / src_name
    dst = dst_root / 'skills' / src_name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def patch_packaged_files(plugin_root: Path, plugin_name: str) -> None:
    if plugin_name == 'plugin-doctor':
        skill_path = plugin_root / 'skills' / 'plugin-doctor' / 'SKILL.md'
        text = skill_path.read_text(encoding='utf-8')
        text = text.replace(
            '- 필요 시 `../codex-skill-audit/scripts/audit_codex_skill_repo.py`\n',
            '- 필요 시 현재 저장소에 별도로 있는 `codex-skill-audit` 또는 동등한 skill audit 도구를 함께 사용\n',
        )
        skill_path.write_text(text, encoding='utf-8')

    if plugin_name == 'apple-craft':
        skill_path = plugin_root / 'skills' / 'apple-harness' / 'SKILL.md'
        text = skill_path.read_text(encoding='utf-8')
        text = text.replace(
            '- Codex app/CLI에서는 `.codex/agents/harness-*.toml` custom agents를 우선 사용한다.\n',
            '- 프로젝트에 custom agent 템플릿이 있으면 우선 사용하고, 없으면 built-in subagent 또는 로컬 작업 분리로 대체한다.\n',
        )
        skill_path.write_text(text, encoding='utf-8')


def render_png(svg_path: Path, png_path: Path) -> None:
    subprocess.run(
        ['sips', '-s', 'format', 'png', str(svg_path), '--out', str(png_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def chip_svg(x: int, y: int, text: str, fill: str) -> str:
    width = max(120, 26 + len(text) * 9)
    safe = escape(text)
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="36" rx="18" fill="{fill}" fill-opacity="0.16"/>'
        f'<text x="{x + 18}" y="{y + 24}" font-family="Inter, SF Pro Display, Arial, sans-serif" '
        f'font-size="15" font-weight="600" fill="white">{safe}</text>'
    )


def prompt_card_svg(x: int, y: int, width: int, prompt: str, accent: str) -> str:
    safe = escape(prompt)
    return f'''
  <rect x="{x}" y="{y}" width="{width}" height="126" rx="22" fill="white" fill-opacity="0.96"/>
  <rect x="{x + 18}" y="{y + 18}" width="92" height="28" rx="14" fill="{accent}" fill-opacity="0.18"/>
  <text x="{x + 36}" y="{y + 37}" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="14" font-weight="700" fill="#0F172A">Prompt</text>
  <text x="{x + 18}" y="{y + 74}" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="600" fill="#0F172A">{safe}</text>
  <text x="{x + 18}" y="{y + 106}" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="15" font-weight="500" fill="#475569">Representative workflow preview</text>
'''


def build_assets(plugin_root: Path, spec: dict) -> None:
    assets = plugin_root / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    color = spec['color']
    accent = spec['accent']
    glyph = escape(spec['glyph'])
    display = escape(spec['interface']['displayName'])
    short = escape(spec['interface']['shortDescription'])
    long_desc = escape(spec['interface']['longDescription'])
    highlights = [escape(item) for item in spec['highlights']]
    prompts = [escape(item) for item in spec['interface']['defaultPrompt']]

    icon_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" fill="none">
  <defs>
    <linearGradient id="g" x1="64" y1="48" x2="448" y2="464" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}"/>
      <stop offset="1" stop-color="{color}"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="#0F172A"/>
  <rect x="36" y="36" width="440" height="440" rx="88" fill="url(#g)"/>
  <rect x="72" y="72" width="368" height="368" rx="68" fill="white" fill-opacity="0.12"/>
  <text x="256" y="294" text-anchor="middle" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="168" font-weight="800" fill="white">{glyph}</text>
  <rect x="126" y="348" width="260" height="52" rx="26" fill="#0F172A" fill-opacity="0.22"/>
  <text x="256" y="381" text-anchor="middle" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="24" font-weight="700" fill="white">{display}</text>
</svg>
'''

    chip1 = chip_svg(396, 102, spec['interface']['capabilities'][0], accent)
    chip2 = chip_svg(396, 150, spec['interface']['capabilities'][1], accent)
    chip3 = chip_svg(396, 198, spec['interface']['capabilities'][2], accent)

    logo_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="820" viewBox="0 0 1400 820" fill="none">
  <defs>
    <linearGradient id="panel" x1="64" y1="64" x2="1320" y2="756" gradientUnits="userSpaceOnUse">
      <stop stop-color="{accent}" stop-opacity="0.26"/>
      <stop offset="1" stop-color="{color}" stop-opacity="0.12"/>
    </linearGradient>
  </defs>
  <rect width="1400" height="820" rx="40" fill="#020617"/>
  <rect x="40" y="40" width="1320" height="740" rx="32" fill="url(#panel)"/>
  <rect x="72" y="72" width="280" height="280" rx="52" fill="{color}"/>
  <text x="212" y="240" text-anchor="middle" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="110" font-weight="800" fill="white">{glyph}</text>
  <text x="396" y="162" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="74" font-weight="800" fill="white">{display}</text>
  <text x="396" y="216" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="30" font-weight="600" fill="#D6E4FF">{short}</text>
  <text x="396" y="276" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="500" fill="#CBD5E1">{long_desc}</text>
  {chip1}
  {chip2}
  {chip3}
  <rect x="72" y="414" width="1256" height="314" rx="28" fill="white" fill-opacity="0.08"/>
  <text x="112" y="474" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="28" font-weight="700" fill="white">Representative workflows</text>
  <text x="112" y="532" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="600" fill="#E2E8F0">• {highlights[0]}</text>
  <text x="112" y="580" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="600" fill="#E2E8F0">• {highlights[1]}</text>
  <text x="112" y="628" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="600" fill="#E2E8F0">• {highlights[2]}</text>
  <text x="112" y="694" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="500" fill="#94A3B8">Generated from repo-local Codex skills • local packaging preview</text>
</svg>
'''

    screenshot_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" fill="none">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1600" y2="1000" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F8FAFC"/>
      <stop offset="1" stop-color="#E2E8F0"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="1000" rx="36" fill="url(#bg)"/>
  <rect x="36" y="36" width="1528" height="928" rx="28" fill="white" stroke="#E2E8F0" stroke-width="2"/>
  <rect x="72" y="72" width="420" height="856" rx="26" fill="#0F172A"/>
  <rect x="108" y="108" width="120" height="120" rx="28" fill="{color}"/>
  <text x="168" y="183" text-anchor="middle" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="58" font-weight="800" fill="white">{glyph}</text>
  <text x="108" y="286" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="42" font-weight="800" fill="white">{display}</text>
  <text x="108" y="328" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="22" font-weight="600" fill="#CBD5E1">{short}</text>
  <rect x="108" y="372" width="348" height="2" fill="#334155"/>
  <text x="108" y="430" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="20" font-weight="700" fill="#E2E8F0">What this package includes</text>
  <text x="108" y="474" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• Packaged skills synced from .agents/skills</text>
  <text x="108" y="514" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• Marketplace metadata + local source path</text>
  <text x="108" y="554" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• PNG/SVG brand assets for local testing</text>
  <text x="108" y="624" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="20" font-weight="700" fill="#E2E8F0">Capability highlights</text>
  <text x="108" y="668" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• {highlights[0]}</text>
  <text x="108" y="708" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• {highlights[1]}</text>
  <text x="108" y="748" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#CBD5E1">• {highlights[2]}</text>
  <text x="108" y="862" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="16" font-weight="600" fill="#94A3B8">Representative preview • not a live Codex UI capture</text>
  <rect x="536" y="72" width="992" height="118" rx="24" fill="{color}"/>
  <text x="584" y="130" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="30" font-weight="800" fill="white">Prompt starter gallery</text>
  <text x="584" y="166" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="18" font-weight="600" fill="#E0E7FF">Use these after local plugin loading is confirmed.</text>
  {prompt_card_svg(536, 228, 460, prompts[0], accent)}
  {prompt_card_svg(1024, 228, 460, prompts[1], accent)}
  {prompt_card_svg(536, 382, 948, prompts[2], accent)}
  <rect x="536" y="548" width="948" height="316" rx="28" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="2"/>
  <text x="576" y="610" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="28" font-weight="800" fill="#0F172A">Launch checklist</text>
  <text x="576" y="660" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="19" font-weight="600" fill="#334155">1. Run static smoke checks</text>
  <text x="576" y="700" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="19" font-weight="600" fill="#334155">2. Restart Codex from this repository root</text>
  <text x="576" y="740" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="19" font-weight="600" fill="#334155">3. Confirm plugin appears in the local catalog</text>
  <text x="576" y="780" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="19" font-weight="600" fill="#334155">4. Run one starter prompt and record the result</text>
  <text x="576" y="832" font-family="Inter, SF Pro Display, Arial, sans-serif" font-size="17" font-weight="600" fill="#64748B">See docs/local-plugin-testing.md and scripts/run_local_plugin_smoke_checks.py</text>
</svg>
'''

    icon_svg_path = assets / 'icon.svg'
    logo_svg_path = assets / 'logo.svg'
    screenshot_svg_path = assets / 'screenshot.svg'
    icon_svg_path.write_text(icon_svg, encoding='utf-8')
    logo_svg_path.write_text(logo_svg, encoding='utf-8')
    screenshot_svg_path.write_text(screenshot_svg, encoding='utf-8')
    render_png(icon_svg_path, assets / 'icon.png')
    render_png(logo_svg_path, assets / 'logo.png')
    render_png(screenshot_svg_path, assets / 'screenshot.png')
    if LIVE_CAPTURE_SOURCE.exists():
        shutil.copy2(LIVE_CAPTURE_SOURCE, assets / 'live-capture.png')
    browser_capture = BROWSER_CAPTURE_DIR / f"{spec['name']}.png"
    if browser_capture.exists():
        shutil.copy2(browser_capture, assets / 'browser-capture.png')


def build_plugin_manifest(spec: dict) -> dict:
    interface = dict(spec['interface'])
    interface['brandColor'] = spec['color']
    interface['composerIcon'] = './assets/icon.png'
    interface['logo'] = './assets/logo.png'
    screenshots = ['./assets/screenshot.png']
    browser_capture = BROWSER_CAPTURE_DIR / f"{spec['name']}.png"
    if browser_capture.exists():
        screenshots.append('./assets/browser-capture.png')
    if LIVE_CAPTURE_SOURCE.exists():
        screenshots.append('./assets/live-capture.png')
    interface['screenshots'] = screenshots

    manifest = {
        'name': spec['name'],
        'version': spec['version'],
        'description': spec['description'],
        'author': {
            'name': 'codex-skills-project',
        },
        'keywords': spec['keywords'],
        'skills': './skills/',
        'interface': interface,
    }
    if spec.get('mcp_servers'):
        manifest['mcpServers'] = './.mcp.json'
    return manifest


def build_marketplace(specs: list[dict]) -> dict:
    return {
        'name': 'codex-skills-local',
        'interface': {
            'displayName': 'Codex Skills Local',
        },
        'plugins': [
            {
                'name': spec['name'],
                'description': spec['description'],
                'version': spec['version'],
                'author': {
                    'name': 'codex-skills-project',
                },
                'source': {
                    'source': 'local',
                    'path': f'./plugins/{spec["name"]}',
                },
                'policy': {
                    'installation': 'AVAILABLE',
                    'authentication': 'ON_INSTALL',
                },
                'category': spec['interface']['category'],
                'keywords': spec['keywords'],
            }
            for spec in specs
        ],
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def write_readme(plugin_root: Path, spec: dict) -> None:
    readme = f'''# {spec["name"]}

{spec["readme"]}

## Included skills

'''
    for skill in spec['skills']:
        readme += f'- `{skill}`\n'

    readme += '\n## Packaged assets\n\n- `assets/icon.svg` / `assets/icon.png`\n- `assets/logo.svg` / `assets/logo.png`\n- `assets/screenshot.svg` / `assets/screenshot.png`\n'
    browser_capture = BROWSER_CAPTURE_DIR / f"{spec['name']}.png"
    if browser_capture.exists():
        readme += '- `assets/browser-capture.png` (external browser render capture)\n'
    if LIVE_CAPTURE_SOURCE.exists():
        readme += '- `assets/live-capture.png` (actual Codex UI capture)\n'

    if spec.get('mcp_servers'):
        readme += '\n## Bundled MCP\n\n- `./.mcp.json`\n'

    readme += '\n## Notes\n\n- This directory is generated from repo-local skills in `.agents/skills/`.\n- Regenerate packaged plugins with `python3 scripts/sync_packaged_plugins.py`.\n- Validate with `python3 .agents/skills/plugin-doctor/scripts/audit_codex_plugin_repo.py .`.\n- Follow `docs/local-plugin-testing.md` for local loading checks.\n- Run `python3 scripts/run_local_plugin_smoke_checks.py` for static smoke checks.\n- `assets/screenshot.png`는 representative preview입니다.\n- `assets/browser-capture.png`가 있으면 외부 브라우저에서 렌더링한 실제 detail/gallery 캡처를 함께 제공합니다.\n- `assets/live-capture.png`가 있으면 현재 repo의 actual Codex UI capture를 함께 제공합니다.\n'
    (plugin_root / 'README.md').write_text(readme, encoding='utf-8')


def main() -> None:
    PLUGINS_ROOT.mkdir(parents=True, exist_ok=True)

    for spec in PLUGIN_SPECS:
        plugin_root = PLUGINS_ROOT / spec['name']
        if plugin_root.exists():
            shutil.rmtree(plugin_root)
        (plugin_root / '.codex-plugin').mkdir(parents=True, exist_ok=True)
        (plugin_root / 'skills').mkdir(parents=True, exist_ok=True)

        for skill in spec['skills']:
            copy_skill(skill, plugin_root)

        patch_packaged_files(plugin_root, spec['name'])
        build_assets(plugin_root, spec)
        write_json(plugin_root / '.codex-plugin' / 'plugin.json', build_plugin_manifest(spec))
        if spec.get('mcp_servers'):
            write_json(plugin_root / '.mcp.json', spec['mcp_servers'])
        write_readme(plugin_root, spec)

    write_json(MARKETPLACE_PATH, build_marketplace(PLUGIN_SPECS))

    plugins_readme = '''# plugins

이 디렉토리는 `.agents/skills/`에서 파생된 **로컬 배포/설치 테스트용 Codex plugin 패키지 레이어**입니다.

## 갱신 방법

```bash
python3 scripts/sync_packaged_plugins.py
```

## 로컬 마켓플레이스

- repo marketplace: `.agents/plugins/marketplace.json`
- plugin roots: `./plugins/<plugin-name>`
- smoke test guide: `docs/local-plugin-testing.md`
- static smoke script: `python3 scripts/run_local_plugin_smoke_checks.py`
- load assistant: `python3 scripts/run_local_plugin_load_assistant.py`

Codex plugin 문서 기준으로 `source.path`는 marketplace root 기준 상대 경로여야 하므로, 현재 저장소에서는 `./plugins/<plugin-name>` 형태를 사용합니다.
'''
    (PLUGINS_ROOT / 'README.md').write_text(plugins_readme, encoding='utf-8')

    print(f'Generated {len(PLUGIN_SPECS)} packaged plugins.')
    print(f'Marketplace: {MARKETPLACE_PATH}')


if __name__ == '__main__':
    main()
