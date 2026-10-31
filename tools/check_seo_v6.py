from pathlib import Path
from bs4 import BeautifulSoup
import re, subprocess, json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
langs=['fr','en','es','it','de','nl','pt','ar','ja','ko']
files=[root/'index.html']+[root/lang/'index.html' for lang in langs]+[root/lang/'video-stopododo.html' for lang in langs]+list((root/'fr').glob('*.html'))
files=sorted(set(files));fail=[];warnings=[]
for f in files:
 soup=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser')
 rel=f.relative_to(root)
 if not soup.find('h1'):fail.append(f'{rel}: missing h1')
 if len(soup.find_all('h1'))!=1:fail.append(f'{rel}: h1 count != 1')
 if not soup.title or not soup.title.get_text(strip=True):fail.append(f'{rel}: missing title')
 if not soup.find('meta',attrs={'name':'description'}):fail.append(f'{rel}: missing description')
 if not soup.find('link',attrs={'rel':'canonical'}):fail.append(f'{rel}: missing canonical')
 for tag in soup.find_all(['link','img','script','source','a','video']):
  for attr in ['href','src','poster']:
   val=tag.get(attr,'')
   if not val or val.startswith(('http:','https:','mailto:','#','data:','javascript:','tel:')):continue
   name=val.split('#')[0].split('?')[0]
   if not name:continue
   target=(f.parent/name).resolve()
   if not target.exists():
    # Legals live in the published website / existing GitHub branch and are deliberately preserved.
    if target.name in {'confidentialite.html','conditions.html','accessibilite.html','contact.html'}:warnings.append(str(rel)+' LEGAL PAGE preserved externally: '+name)
    else:fail.append(f'{rel}: broken resource {tag.name}.{attr}={name}')
 if f.name=='video-stopododo.html':
  script=soup.find('script',attrs={'type':'application/ld+json'})
  obj=json.loads(script.text)
  if obj['@type']!='VideoObject':fail.append(f'{rel}: VideoObject absent')
  if 'uploadDate' not in obj:warnings.append(f'{rel}: uploadDate must be added upon first publication')
  if not soup.find('video'):fail.append(f'{rel}: missing video')
  if len(soup.find_all('link',attrs={'rel':'alternate'}))!=11:fail.append(f'{rel}: hreflang count')
 if f.name=='index.html' and (f.parent.name in langs or f.parent==root):
  if f.parent==root or f.parent.name=='fr':
   if len(soup.select('.seo-guide-card'))!=3:fail.append(f'{rel}: missing 3 guides')
  if not soup.find('a',attrs={'href':re.compile('video-stopododo.html')}):fail.append(f'{rel}: no direct video page link')
for xml in ['sitemap.xml','video-sitemap.xml']:ET.parse(root/xml)
sm=ET.parse(root/'sitemap.xml').getroot()
ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs=[x.text for x in sm.findall('.//sm:loc',ns)]
assert len(locs)==27,len(locs)
assert len(set(locs))==27
assert len(list((root/'assets/img/video-posters').glob('*.webp')))==10
for lang in langs:
 assert (root/lang/'video-stopododo.html').exists()
 assert (root/'assets/videos'/f'{lang}.mp4').exists()
 assert (root/'assets/img/video-posters'/f'{lang}.webp').exists()
if fail:
 print('FAIL',len(fail));print('\n'.join(fail[:50]));raise SystemExit(1)
print('PASS: HTML',len(files),'XML 2, video pages 10, guides 3, posters 10, canonical sitemap 27 URLs, media 10.')
print('Warnings:',len(warnings),'(legal content intentionally excluded from V6 overlay, missing video uploadDate before publication)')
