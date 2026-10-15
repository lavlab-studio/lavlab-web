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
    content=fallback[idx%6]
    if image:
        cover_class+=' has-image'
        content=f'<img class="cover-img" src="{esc(image)}" alt="" loading="lazy" decoding="async">'
    cards.append(f'<button type="button" class="work" data-title="{title}" data-text="{desc}" data-url="{url}" data-image="{esc(image)}"><div class="{cover_class}">{content}</div><div class="work-meta"><span>{idx+1:02d} / {title}</span><span>{cat}</span></div></button>')
html_out=template.replace('&lt;!-- LAVLAB_PROJECTS --&gt;','\n'.join(cards) if cards else '<p class="empty-projects">Próximamente: nuevos proyectos de LavLab.</p>')
html_out=html_out.replace('Archivo / 001—006',f'Archivo / {len(visible):03d} proyectos')
html_out=html_out.replace('Una selección de exploraciones visuales y sonoras.<br/>Proyectos de ejemplo para esta demo.','Una selección de exploraciones visuales y sonoras.')

# Editables desde Pages CMS: salas, gear y textos generales.
def read_yaml(path):
    if not path.exists(): return {}
    data=yaml.safe_load(path.read_text(encoding='utf-8-sig')) or {}
    return data if isinstance(data,dict) else {}

site=read_yaml(BASE/'content/site.yml')
for placeholder,key in [('LAVLAB_HERO_TAGLINE','hero_tagline'),('LAVLAB_MANIFESTO_TEXT','manifesto_text')]:
    pass
room_names=[('control-room','Control Room'),('live-room','Live Room'),('vocal-booth','Vocal Booth'),('the-pub','The Pub')]
room_cards=[]
room_data={}
for i,(slug,default_title) in enumerate(room_names,1):
    info=read_yaml(BASE/'content/rooms'/f'{slug}.yml')
    title=str(info.get('title') or default_title)
    desc=str(info.get('description') or '')
    images=[safe_image(img) for img in (info.get('images') or []) if isinstance(img,str)]
    images=[img for img in images if img]
    room_data[slug]={'title':title,'description':desc,'images':images}
    cover=f'<img src="{esc(images[0])}" alt="{esc(title)}" loading="lazy">' if images else '<span class="lab-room-fallback">PHOTOS COMING SOON</span>'
    room_cards.append(f'<button type="button" class="lab-room" data-lab="{slug}"><div class="lab-room-image">{cover}</div><div class="lab-room-meta"><span>{i:02d} / {esc(title)}</span><span class="arrow">↗</span></div></button>')
gear=read_yaml(BASE/'content/gear.yml')
sections=[]
for section in gear.get('sections',[]) or []:
    if isinstance(section,dict):sections.append({'title':str(section.get('title') or ''),'items':str(section.get('items') or '')})
lab_json=json.dumps({'rooms':room_data,'gear':{'title':'Gear','description':str(gear.get('description') or ''),'sections':sections}},ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
html_out=html_out.replace('LAVLAB_ROOMS_PLACEHOLDER','\n'.join(room_cards))
html_out=html_out.replace('LAVLAB_LAB_JSON_PLACEHOLDER',lab_json)
if site.get('hero_tagline'):
    html_out=html_out.replace('Un espacio para hacer música. Y para hacer cosas que todavía no sabemos cómo llamar.',esc(site['hero_tagline']))
if site.get('manifesto_text'):
    html_out=html_out.replace('LavLab es un lugar donde las ideas se prueban, se desmontan y se convierten en música.',esc(site['manifesto_text']))

out=BASE/'dist';out.mkdir(exist_ok=True)
(out/'index.html').write_text(html_out,encoding='utf-8')
if (BASE/'media').exists():
    shutil.copytree(BASE/'media',out/'media',dirs_exist_ok=True)
print(f'Web generada: {out}/index.html ({len(visible)} proyectos)')
