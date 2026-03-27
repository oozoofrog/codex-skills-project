#!/usr/bin/env python3
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'reports' / 'plugin-gallery'


BASE_CSS = '''
:root{--bg:#0f172a;--panel:#111827;--card:#ffffff;--muted:#64748b;--line:#e2e8f0;}
*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,sans-serif;background:#f8fafc;color:#0f172a}
a{text-decoration:none;color:inherit}.wrap{max-width:1320px;margin:0 auto;padding:48px 32px 80px}.hero{background:linear-gradient(135deg,#0f172a,#1e293b);color:#fff;border-radius:32px;padding:40px 44px;box-shadow:0 24px 70px rgba(15,23,42,.28)}.hero h1{margin:0;font-size:48px;line-height:1.05}.hero p{margin:16px 0 0;color:#cbd5e1;font-size:20px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:32px}.card{background:#fff;border:1px solid #e2e8f0;border-radius:28px;padding:28px;box-shadow:0 16px 48px rgba(15,23,42,.08)}.top{display:flex;gap:20px;align-items:center}.icon{width:88px;height:88px;border-radius:24px;object-fit:cover;box-shadow:0 12px 24px rgba(15,23,42,.16)}.name{font-size:28px;font-weight:800;line-height:1.1}.short{margin-top:8px;color:#475569;font-size:17px;line-height:1.5}.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.chip{padding:9px 14px;border-radius:999px;font-size:13px;font-weight:700}.prompts{margin-top:20px;padding-top:20px;border-top:1px solid #e2e8f0}.prompts div{font-size:14px;line-height:1.55;color:#334155;margin-top:8px}.detail-layout{display:grid;grid-template-columns:1.15fr .85fr;gap:28px;margin-top:28px}.panel{background:#fff;border:1px solid #e2e8f0;border-radius:28px;padding:28px;box-shadow:0 16px 48px rgba(15,23,42,.08)}.logo{width:100%;border-radius:22px;border:1px solid #e2e8f0}.section-title{font-size:14px;font-weight:800;letter-spacing:.08em;color:#64748b;text-transform:uppercase}.detail-title{font-size:44px;line-height:1.05;margin:14px 0 10px}.detail-sub{font-size:20px;color:#475569;line-height:1.55}.list{margin:18px 0 0;padding-left:18px;color:#334155;font-size:17px;line-height:1.7}.prompt-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:20px;padding:18px;margin-top:14px}.prompt-card strong{display:block;margin-bottom:8px}.live{width:100%;margin-top:18px;border-radius:22px;border:1px solid #cbd5e1;box-shadow:0 18px 40px rgba(15,23,42,.12)}.subnav{display:flex;gap:14px;flex-wrap:wrap;margin-top:20px}.subnav a{padding:10px 14px;border-radius:999px;background:#fff;color:#0f172a;border:1px solid rgba(255,255,255,.18)}
'''


def load_plugins():
    plugins = []
    for manifest_path in sorted((ROOT / 'plugins').glob('*/.codex-plugin/plugin.json')):
        data = json.loads(manifest_path.read_text())
        interface = data.get('interface', {})
        plugins.append({
            'name': data['name'],
            'display': interface.get('displayName', data['name']),
            'short': interface.get('shortDescription', ''),
            'long': interface.get('longDescription', ''),
            'capabilities': interface.get('capabilities', []),
            'prompts': interface.get('defaultPrompt', []),
            'keywords': data.get('keywords', []),
            'brand': interface.get('brandColor', '#334155'),
            'icon': Path('..') / '..' / 'plugins' / data['name'] / 'assets' / 'icon.png',
            'logo': Path('..') / '..' / 'plugins' / data['name'] / 'assets' / 'logo.png',
            'live': Path('..') / '..' / 'plugins' / data['name'] / 'assets' / 'live-capture.png',
        })
    return plugins


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    plugins = load_plugins()

    index_cards = []
    nav = []
    for p in plugins:
        color = escape(p['brand'])
        caps = ''.join(f"<span class='chip' style='background:{color}20;color:{color}'>{escape(c)}</span>" for c in p['capabilities'][:3])
        prompts = ''.join(f"<div>• {escape(pr)}</div>" for pr in p['prompts'][:2])
        href = f"{p['name']}.html"
        nav.append(f"<a href='{href}'>{escape(p['display'])}</a>")
        index_cards.append(f"""
    <a class='card' href='{href}'>
      <div class='top'>
        <img class='icon' src='{p['icon'].as_posix()}' alt='{escape(p['display'])} icon'/>
        <div>
          <div class='name'>{escape(p['display'])}</div>
          <div class='short'>{escape(p['short'])}</div>
        </div>
      </div>
      <div class='chips'>{caps}</div>
      <div class='prompts'>
        <div class='section-title'>Starter prompts</div>
        {prompts}
      </div>
    </a>
    """)

    index_html = f"""<!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><title>Codex Local Plugin Gallery</title><style>{BASE_CSS}</style></head><body><div class='wrap'><div class='hero'><div class='section-title' style='color:#93c5fd'>Local Codex Plugin Gallery</div><h1>Packaged plugin catalog preview</h1><p>이 페이지는 현재 저장소의 <code>.agents/plugins/marketplace.json</code> 및 packaged plugin manifest를 기반으로 생성된 실제 로컬 미리보기입니다.</p><div class='subnav'>{''.join(nav)}</div></div><div class='grid'>{''.join(index_cards)}</div></div></body></html>"""
    (OUT / 'index.html').write_text(index_html, encoding='utf-8')

    for p in plugins:
        color = escape(p['brand'])
        caps = ''.join(f"<span class='chip' style='background:{color}20;color:{color}'>{escape(c)}</span>" for c in p['capabilities'])
        prompt_cards = ''.join(f"<div class='prompt-card'><strong>Prompt {i+1}</strong>{escape(pr)}</div>" for i, pr in enumerate(p['prompts']))
        keywords = ''.join(f"<span class='chip' style='background:#eef2ff;color:#334155'>{escape(k)}</span>" for k in p['keywords'])
        highlights = ''.join(f"<li>{escape(h)}</li>" for h in [
            f"Packaged skills live under plugins/{p['name']}/skills",
            f"Brand assets and screenshots live under plugins/{p['name']}/assets",
            "This page is generated from plugin metadata and shown inside a real browser for capture workflows",
        ])
        html = f"""<!doctype html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><title>{escape(p['display'])}</title><style>{BASE_CSS}</style></head><body><div class='wrap'><div class='hero'><div class='section-title' style='color:#bfdbfe'>Plugin Detail Preview</div><h1>{escape(p['display'])}</h1><p>{escape(p['short'])}</p><div class='subnav'><a href='index.html'>← Catalog</a></div></div><div class='detail-layout'><div class='panel'><div class='section-title'>Overview</div><div class='detail-title'>{escape(p['display'])}</div><div class='detail-sub'>{escape(p['long'])}</div><div class='chips' style='margin-top:22px'>{caps}{keywords}</div><ul class='list'>{highlights}</ul><div class='section-title' style='margin-top:30px'>Starter prompts</div>{prompt_cards}</div><div class='panel'><img class='logo' src='{p['logo'].as_posix()}' alt='{escape(p['display'])} logo'/><div class='section-title' style='margin-top:22px'>Live Codex workspace capture</div><img class='live' src='{p['live'].as_posix()}' alt='live codex capture'/></div></div></div></body></html>"""
        (OUT / f"{p['name']}.html").write_text(html, encoding='utf-8')

    print(f'gallery generated at {OUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
