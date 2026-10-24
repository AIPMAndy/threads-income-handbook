#!/usr/bin/env python3
"""Dependency-free quality checks for generated public files."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
import sys,re,importlib.util
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from content import CHAPTERS,ROUTES,FAQ,TEMPLATES,SOURCES
from advanced import DEEP_DIVES, DECISIONS, EXAMPLES

class Parser(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.h1=0;self.title=0;self.description=0;self.canonical=0;self.lang=False;self.secure=True;self.href_blank=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='html' and d.get('lang')=='zh-CN':self.lang=True
  if t=='h1':self.h1+=1
  if t=='title':self.title+=1
  if t=='meta' and d.get('name')=='description':self.description+=1
  if t=='link' and d.get('rel')=='canonical':self.canonical+=1
  if 'id' in d:self.ids.add(d['id'])
  if t in ('a','link','script'):
   k={'a':'href','link':'href','script':'src'}[t];v=d.get(k);self.links.append((t,v)) if v else None
  if t=='a' and d.get('target')=='_blank' and ('noopener' not in d.get('rel','') or 'noreferrer' not in d.get('rel','')):self.secure=False

checks=0

def ok(cond,msg):
 global checks
 checks+=1
 if not cond:raise AssertionError(msg)

def audit():
 htmlfiles=sorted(ROOT.glob('*.html'))+sorted((ROOT/'guide').glob('*.html'))
 ok(len(CHAPTERS)==24,'chapter count')
 ok(len(ROUTES)==6,'route count')
 ok(len(TEMPLATES)==24,'template count')
 ok(len(FAQ)>=35,'FAQ coverage')
 ok(len(SOURCES)>=14,'sources count')
 ok(len(DEEP_DIVES)>=10,'deep dives coverage')
 ok(len(DECISIONS)==6,'diagnosis stages')
 ok(len(EXAMPLES)==3,'worked examples')
 ok(len(htmlfiles)==31,'page count')
 ok(len(set(c['slug'] for c in CHAPTERS))==len(CHAPTERS),'unique slug')
 ok(len({c['title'] for c in CHAPTERS})==len(CHAPTERS),'unique chapter title')
 ok(all(len(c['steps'])>=5 for c in CHAPTERS),'adequate step count')
 ok(all(c['source'] in [s[0] for s in SOURCES] for c in CHAPTERS),'source mapping')
 ok(all(c['risk'] and c['metrics'] and c['output'] for c in CHAPTERS),'acceptance and risk sections')
 ok(all(s[3].startswith('https://') for s in SOURCES),'source HTTPS')
 ok((ROOT/'assets/social-preview.png').exists(),'share image')
 ok((ROOT/'assets/favicon.svg').exists(),'favicon')
 ok((ROOT/'assets/style.css').exists(),'CSS')
 ok((ROOT/'assets/app.js').exists(),'JS')
 allids={}
 for f in htmlfiles:
  raw=f.read_text(encoding='utf8');p=Parser();p.feed(raw);allids[f]=p.ids
  ok(p.lang and p.title==1 and p.h1==1,f'heading/lang: {f}')
  ok(p.description==1 and p.canonical==1,f'SEO: {f}')
  ok(p.secure,f'insecure target blank: {f}')
  ok('AIPMAndy' in raw and 'metaver.vip' in raw,f'conversion links: {f}')
  ok('index.html' in raw,f'return path: {f}')
  for tag,link in p.links:
   if link.startswith(('https:','http:','mailto:','tel:','data:')): continue
   target=unquote(link.split('#',1)[0]);anchor=link.split('#',1)[1] if '#' in link else None
   dest=(f.parent/target).resolve() if target else f
   if not str(dest).startswith(str(ROOT.resolve())):raise AssertionError(f'escaping root: {f} -> {link}')
   ok(dest.exists(),f'broken relative link {f} -> {link}')
   # Asset SVG and JS links cannot have anchors. ID anchors require target HTML.
   if anchor and dest.suffix=='.html':
    if dest not in allids:
     pp=Parser();pp.feed(dest.read_text(encoding='utf8'));allids[dest]=pp.ids
    ok(anchor in allids[dest],f'broken hash anchor: {f} -> {link}')
 sitemap=ROOT/'sitemap.xml';ok(sitemap.exists(),'sitemap')
 root=ET.fromstring(sitemap.read_text());locs=root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
 ok(len(locs)==30,'sitemap count')
 ok((ROOT/'robots.txt').exists(),'robots')
 ok('localStorage' in (ROOT/'assets/app.js').read_text(),'local-only progress')
 ok('prefers-reduced-motion' in (ROOT/'assets/style.css').read_text(),'motion accessibility')
 ok((ROOT/'lab.html').exists(),'workbench page')
 ok((ROOT/'plan.html').exists(),'30-day plan page')
 ok((ROOT/'plan.html').read_text().count('data-plan="plan-day-')==30,'30-day checklist generated')
 ok('id="lab-stage"' in (ROOT/'lab.html').read_text(),'workbench decision')
 ok('id="f-summary"' in (ROOT/'lab.html').read_text(),'actual funnel UI')
 ok('data-advice=' in (ROOT/'lab.html').read_text(),'diagnosis content')
 ok('renderFunnel' in (ROOT/'assets/app.js').read_text(),'actual funnel logic')
 ok('formatOffer' in (ROOT/'assets/app.js').read_text(),'offer creation logic')
 print(f'PASS: {checks} checks across {len(htmlfiles)} HTML pages · {len(CHAPTERS)} chapters · {len(SOURCES)} reviewed links')
if __name__=='__main__':
 try:audit()
 except AssertionError as exc:print('FAIL:',str(exc));sys.exit(1)
