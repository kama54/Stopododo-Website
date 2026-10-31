"""Regenerate the 11 localized static landing pages.

Development only: pip install Jinja2. The published site has no Python dependency.
"""
from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT=Path(__file__).resolve().parents[1]
BASE='https://kama54.github.io/Stopododo-Website'
NAMES={'fr':'Français','en':'English','es':'Español','it':'Italiano','de':'Deutsch','nl':'Nederlands','pt':'Português','ar':'العربية','ja':'日本語','ko':'한국어'}
LOCALES={'fr':'fr-FR','en':'en','es':'es','it':'it','de':'de','nl':'nl','pt':'pt','ar':'ar','ja':'ja','ko':'ko'}
T=json.loads((ROOT/'translations.json').read_text(encoding='utf-8'))
assert set(T)==set(NAMES)
assert len({frozenset(x) for x in map(dict.keys,T.values())})==1
ENV=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']))
TMPL=ENV.get_template('index.html.j2')
LANGS=list(LOCALES.items())

def make(lang:str,root_page=False):
    t=T[lang]
    target=ROOT/'index.html' if root_page else ROOT/lang/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    canonical=f'{BASE}/{lang}/index.html'
    schema={'@context':'https://schema.org','@type':'SoftwareApplication','name':'Stopododo','operatingSystem':'Android 7+','applicationCategory':'UtilitiesApplication','isAccessibleForFree':True,'offers':[{'@type':'Offer','price':'0','priceCurrency':'EUR'},{'@type':'Offer','price':'2.99','priceCurrency':'EUR','description':'One-time Premium purchase'}],'description':t['desc'],'url':canonical}
    txt=TMPL.render(t=t,lang=lang,langtag='pt-BR' if lang=='pt' else ('fr-FR' if lang=='fr' else lang),direction='rtl' if lang=='ar' else 'ltr',langs=LANGS,names=NAMES,base=BASE,prefix='' if root_page else '../',home='fr/index.html' if root_page else 'index.html',legal=f'{BASE}/{lang}/',canonical=canonical,structured=json.dumps(schema,ensure_ascii=False).replace('</','<\\/'))
    target.write_text(txt,encoding='utf-8')

for language in NAMES:make(language)
make('fr',root_page=True)
print('Generated 11 HTML homepages.')
