#!/usr/bin/env python3
"""Genera la web estática desde la plantilla y los proyectos del panel CMS."""
from pathlib import Path
import json, html, re, shutil
import yaml
from urllib.parse import urlparse

BASE=Path(__file__).resolve().parent
projects=[]
for file in sorted((BASE/'content/projects').glob('*.md')):
    raw=file.read_text(encoding='utf-8-sig')
    match=re.match(r'\A---\s*\n(.*?)\n---\s*(?:\n|$)',raw,re.S)
    if match:
        item=yaml.safe_load(match.group(1)) or {}
        if not isinstance(item,dict): continue
        body=raw[match.end():].strip()
        if not item.get('description') and body: item['description']=body
        item.setdefault('title',file.stem.replace('-',' ').title())
        projects.append(item)
# También permite proyectos JSON si Pages CMS crea archivos JSON individuales.
for file in sorted((BASE/'content/projects').glob('*.json')):
    item=json.loads(file.read_text(encoding='utf-8'))
    if isinstance(item,dict):
        item.setdefault('title',file.stem.replace('-',' ').title())
        projects.append(item)
template=(BASE/'template.html').read_text(encoding='utf-8')


def esc(value):
    return html.escape(str(value or ''),quote=True)


def safe_image(path):
    path=str(path or '').strip()
    if not path: return ''
    if (path.startswith('/media/') or path.startswith('media/')) and '..' not in path: return '/' + path.lstrip('/')
    return ''


def safe_link(url):
    url=str(url or '').strip()
    if not url: return ''
    parsed=urlparse(url)
    return url if parsed.scheme in ('https','http') and parsed.netloc else ''

cards=[]
visible=[p for p in projects if p.get('published',True)]
for idx,p in enumerate(visible):
    title=esc(p.get('title','Sin título'))
    cat=esc(p.get('category','Proyecto'))
    desc=esc(p.get('description',''))
    image=safe_image(p.get('image'))
    url=esc(safe_link(p.get('url')))
    # Conservamos los seis diseños gráficos originales mientras no se suban portadas.
    fallback=['<div class="cover-type">FRE<br>CUEN<br>CIA</div>','','<div class="cover-type">ERROR<br>03</div>','<div class="cover-type">Aa</div>','','<div class="cover-type">AFTER<br>HOURS</div>']
    cover_class=f'cover cover{(idx%6)+1}'
    style=''
    content=fallback[idx%6]
    if image:
        cover_class+=' has-image'
        style=f' style="background-image:url(\'{esc(image)}\')"'
        content=''
    cards.append(f'<button type="button" class="work" data-title="{title}" data-text="{desc}" data-url="{url}"><div class="{cover_class}"{style}>{content}</div><div class="work-meta"><span>{idx+1:02d} / {title}</span><span>{cat}</span></div></button>')
html_out=template.replace('&lt;!-- LAVLAB_PROJECTS --&gt;','\n'.join(cards) if cards else '<p class="empty-projects">Próximamente: nuevos proyectos de LavLab.</p>')
html_out=html_out.replace('Archivo / 001—006',f'Archivo / {len(visible):03d} proyectos')
html_out=html_out.replace('Una selección de exploraciones visuales y sonoras.<br/>Proyectos de ejemplo para esta demo.','Una selección de exploraciones visuales y sonoras.')
out=BASE/'dist';out.mkdir(exist_ok=True)
(out/'index.html').write_text(html_out,encoding='utf-8')
if (BASE/'media').exists():
    shutil.copytree(BASE/'media',out/'media',dirs_exist_ok=True)
print(f'Web generada: {out}/index.html ({len(visible)} proyectos)')
