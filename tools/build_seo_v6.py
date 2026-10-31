"""Build the SEO additions to Stopododo V5 without publishing anything.

The 10 original MP4s are reused without changes. VideoObject.uploadDate is omitted until a
truthful first public release date is known. This is a prepublication candidate.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET
from datetime import timedelta
import html, json, re, subprocess, os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT=Path(__file__).resolve().parents[1]
BASE='https://kama54.github.io/Stopododo-Website'
LANGS={'fr':'fr-FR','en':'en','es':'es','it':'it','de':'de','nl':'nl','pt':'pt-BR','ar':'ar','ja':'ja','ko':'ko'}
NAMES={'fr':'Français','en':'English','es':'Español','it':'Italiano','de':'Deutsch','nl':'Nederlands','pt':'Português','ar':'العربية','ja':'日本語','ko':'한국어'}
T=json.loads((ROOT/'translations.json').read_text(encoding='utf-8'))
ENV=Environment(loader=FileSystemLoader(ROOT/'templates'),autoescape=select_autoescape(['html']))

VIDEO_SUFFIX='video-stopododo.html'
GUIDES={
  'assombrir-ecran-android.html': {
    'title': 'Comment assombrir son écran Android au-delà du minimum ?',
    'description': 'Écran Android trop lumineux la nuit ? Comparez la luminosité système, Extra Dim et un filtre d’écran supplémentaire. Guide et captures Stopododo.',
    'heading': 'Comment assombrir son écran Android quand le minimum reste trop lumineux ?',
    'lead': 'Même avec la luminosité au plus bas, un smartphone peut rester gênant dans une pièce sombre. Voici les réglages à essayer, leurs limites et la place d’un filtre d’assombrissement.',
    'featured_img': 'screen-ready.webp',
    'featured_alt': 'Capture réelle de Stopododo montrant le minuteur et les commandes d’assombrissement',
    'sections': [
      ('1. Commencer par les réglages du téléphone', [
          'Ouvrez les réglages rapides et baissez le curseur de luminosité au minimum compatible avec votre appareil. Si la luminosité adaptative est activée, essayez de la désactiver temporairement pour vérifier qu’elle ne remonte pas l’éclairage.',
          'Activez le thème sombre dans les paramètres d’affichage. Il change les couleurs de nombreuses interfaces, mais n’abaisse pas forcément le niveau de lumière de toutes les zones de l’écran. Le résultat peut être différent selon l’application utilisée.'
      ]),
      ('2. Vérifier si Android propose « Extra Dim »', [
          'Certains smartphones disposent d’un réglage d’assombrissement supplémentaire, souvent nommé « Extra Dim », « Réduction de la luminosité » ou un terme voisin. Son emplacement dépend de la marque, de la version Android et du modèle. Regardez dans Paramètres > Accessibilité, dans les options d’affichage ou dans les réglages rapides.',
          'Sur certains Google Pixel, Google documente précisément une fonction Extra Dim destinée à rendre l’écran plus sombre que son minimum standard. Cela ne signifie pas que tous les smartphones possèdent cette option. Si elle est absente, passez à l’étape suivante.'
      ]),
      ('3. Utiliser un filtre d’écran supplémentaire', [
          'Un filtre d’écran agit en superposant une couche assombrissante à l’affichage. C’est le principe de la fonctionnalité d’assombrissement de Stopododo : elle permet un réglage complémentaire à la luminosité habituelle du téléphone, selon les autorisations Android disponibles.',
          'Dans Stopododo, réglez le niveau d’assombrissement progressivement plutôt que de choisir directement une valeur très élevée. Conservez suffisamment de visibilité pour les appels, les notifications importantes et les boutons de sécurité. Le filtre avancé plein écran fait partie des fonctions Premium et peut nécessiter l’activation volontaire d’un service d’accessibilité.'
      ]),
      ('4. Ne pas confondre assombrissement et filtre lumière bleue', [
          'L’assombrissement vise à réduire la lumière perçue. Le filtre lumière bleue change surtout la teinte de l’image, généralement vers des couleurs plus chaudes. Les deux fonctions peuvent se compléter, mais elles ne font pas exactement la même chose.',
          'Stopododo propose un filtre lumière bleue parmi ses fonctions Premium. Évitez toutefois de présenter un filtre comme une garantie de meilleur sommeil : le confort visuel est personnel et dépend aussi de vos habitudes et de votre appareil.'
      ]),
      ('5. Associer le filtre à un minuteur', [
          'Si vous regardez des vidéos sur votre téléphone avant de dormir, vous pouvez associer l’assombrissement à un minuteur. Dans Stopododo, la version gratuite permet une durée allant jusqu’à 15 minutes ; Premium étend cette limite à 240 minutes.',
          'À la fin du décompte, Stopododo peut couper le son multimédia, tenter la mise en pause d’un lecteur vidéo compatible ou verrouiller l’écran si les autorisations nécessaires sont accordées. La pause n’est pas garantie pour tous les lecteurs.'
      ])
    ],
    'faq': [
      ('Pourquoi mon téléphone reste-t-il lumineux au minimum ?', 'La luminosité minimale dépend de l’écran et de ses réglages. Le thème sombre, Extra Dim quand il existe et un filtre supplémentaire peuvent aider à adapter l’affichage.'),
      ('Un filtre d’écran remplace-t-il la luminosité Android ?', 'Non. Commencez par le réglage système : le filtre est un complément et certaines zones peuvent rester soumises aux limites d’Android.'),
      ('Stopododo marche-t-il sur Android TV ?', 'Non. Stopododo est conçu pour les smartphones et tablettes Android compatibles, pas pour les téléviseurs Android TV.')
    ],
    'source': ('Aide officielle Android — paramètres d’affichage et Extra Dim', 'https://support.google.com/accessibility/android/answer/11183305?hl=fr')
  },
  'minuteur-sommeil-android.html': {
    'title':'Minuteur de sommeil Android : programmer l’arrêt du son et des vidéos',
    'description':'Comment utiliser un minuteur de sommeil sur Android ? Durées, son, pause des vidéos compatibles et verrouillage : guide pratique avec Stopododo.',
    'heading':'Comment programmer un minuteur de sommeil sur Android ?',
    'lead':'Un minuteur de sommeil peut arrêter le son ou tenter de mettre une vidéo en pause après une durée définie. Voici comment organiser une routine simple sans laisser votre téléphone fonctionner inutilement toute la nuit.',
    'featured_img':'screen-running.webp',
    'featured_alt':'Capture réelle du minuteur Stopododo en fonctionnement sur Android',
    'sections':[
      ('1. Choisir ce qui doit se passer à la fin du minuteur',[
        'Avant de lancer le compte à rebours, décidez du résultat souhaité : couper le son, mettre en pause une lecture vidéo compatible, ou verrouiller l’écran. Ces actions n’ont pas toutes la même portée et certaines peuvent demander une autorisation Android.',
        'Par exemple, couper le volume multimédia n’est pas identique à fermer une application de streaming. Si une vidéo continue d’être lue sans son, cela dépend du lecteur et de son comportement. Choisissez donc l’action adaptée à votre usage.'
      ]),
      ('2. Régler la durée',[
        'Lancez Stopododo sur votre smartphone Android. Depuis le cadran circulaire ou les durées proposées, choisissez le temps voulu. La version gratuite permet de programmer jusqu’à 15 minutes. Avec l’achat Premium à 2,99 € une seule fois, la durée peut atteindre 240 minutes.',
        'Vous pouvez commencer par une courte durée et l’ajuster les soirs suivants. Il n’existe pas une durée unique qui convienne à tout le monde : elle dépend de vos habitudes de lecture et du temps que vous souhaitez garder avant l’arrêt.'
      ]),
      ('3. Régler le son ou la pause vidéo',[
        'Activez l’option de coupure du son si vous ne souhaitez plus entendre l’audio après le délai choisi. Pour la mise en pause, gardez à l’esprit que tous les lecteurs n’acceptent pas les mêmes commandes : l’application peut tenter la pause lorsqu’elle est prise en charge.',
        'Si vous choisissez le verrouillage de l’écran, Android peut vous demander une autorisation spécifique d’administration de l’appareil. La décision vous appartient et vous pouvez contrôler les autorisations dans les réglages du téléphone.'
      ]),
      ('4. Assombrir l’écran pendant le décompte',[
        'Un minuteur devient encore plus pratique lorsqu’il est associé à un filtre d’assombrissement. Stopododo peut rendre l’écran plus sombre que le niveau habituel du téléphone, selon les autorisations disponibles. Le filtre lumière bleue et le filtre plein écran avancé font partie du Premium.',
        'Veillez à conserver une luminosité suffisante pour lire les commandes importantes. Si un filtre n’agit pas sur toutes les zones, vérifiez les restrictions de votre version Android.'
      ]),
      ('5. Faire un essai avant le coucher',[
        'Pour vérifier le comportement avec votre lecteur habituel, programmez une courte minuterie et observez ce qui se passe réellement à l’échéance. Vérifiez séparément le son, la pause vidéo et le verrouillage de l’écran.',
        'Stopododo n’est pas un lecteur vidéo et ne garantit pas la pause de chaque application. Il est destiné aux smartphones et tablettes Android compatibles, pas à Android TV.'
      ])
    ],
    'faq':[
      ('Peut-on programmer un arrêt automatique du son ?', 'Oui, Stopododo propose la coupure du volume multimédia à la fin du compte à rebours.'),
      ('La version gratuite suffit-elle ?', 'Elle permet un minuteur jusqu’à 15 minutes. Les minuteries jusqu’à 240 minutes et des réglages avancés font partie de Premium.'),
      ('La pause vidéo fonctionnera-t-elle partout ?', 'Non. Elle dépend du support de la commande de pause par le lecteur utilisé.')
    ]
  },
  'arreter-video-automatiquement.html':{
    'title':'Arrêter une vidéo automatiquement sur Android : ce qui est possible',
    'description':'Vous vous endormez devant des vidéos sur Android ? Découvrez comment programmer la coupure du son, demander la pause et verrouiller l’écran avec un minuteur.',
    'heading':'Comment arrêter une vidéo automatiquement sur Android ?',
    'lead':'Vous lancez une vidéo avant de dormir puis le téléphone continue de jouer ? Un minuteur peut aider, mais la coupure du son, la mise en pause et le verrouillage de l’écran sont trois actions différentes.',
    'featured_img':'screen-ready.webp',
    'featured_alt':'Capture réelle de Stopododo avec les options de durée et de pause vidéo',
    'sections':[
      ('1. Comprendre les différentes possibilités',[
        'Couper le son signifie ramener le volume multimédia à zéro à une heure ou après une durée. Le contenu peut continuer de défiler silencieusement selon le lecteur. Une commande de pause essaie d’arrêter la lecture de la vidéo elle-même. Le verrouillage coupe l’accès à l’écran, mais son effet sur la lecture dépend aussi du comportement de l’application vidéo.',
        'Il est important de distinguer ces trois fonctions pour ne pas promettre l’arrêt de toutes les applications de streaming. Sur Android, le comportement des commandes multimédia varie selon le lecteur et les versions du système.'
      ]),
      ('2. Régler un minuteur avant de regarder',[
        'Ouvrez Stopododo et choisissez une durée correspondant à votre soirée. Le minuteur gratuit va jusqu’à 15 minutes. Un achat Premium unique à 2,99 € permet des durées jusqu’à 240 minutes.',
        'Sélectionnez les actions de fin de minuterie souhaitées, puis démarrez le compte à rebours. Vous pouvez ensuite revenir à votre application vidéo habituelle sur le smartphone.'
      ]),
      ('3. Essayer la mise en pause compatible',[
        'Quand le délai arrive à zéro, Stopododo peut essayer d’envoyer une commande de pause au lecteur. Certains lecteurs la prennent en compte, d’autres l’ignorent ou n’exposent pas de commandes multimédias adaptées. Ce n’est pas un défaut de connexion et l’application ne promet pas une compatibilité universelle.',
        'Effectuez un essai court avec l’application vidéo que vous utilisez réellement. N’en déduisez pas une compatibilité avec un autre lecteur : le résultat peut changer après une mise à jour.'
      ]),
      ('4. Prévoir une solution de repli : le son et l’écran',[
        'Si la pause ne fonctionne pas avec un lecteur, l’option de coupure du volume multimédia reste une autre possibilité. Elle permet d’éviter que le son continue après votre endormissement, même si l’image peut continuer à défiler.',
        'Le verrouillage de l’écran nécessite une autorisation Android spécifique si vous choisissez cette action. Vérifiez qu’il n’interrompt pas un usage important et que vous pouvez déverrouiller votre appareil normalement.'
      ]),
      ('5. Garder un écran confortable pendant la lecture',[
        'L’assombrissement supplémentaire de Stopododo réduit l’éclat affiché au-delà du réglage habituel, selon les autorisations du téléphone. Il peut s’utiliser en complément du minuteur.',
        'Stopododo fonctionne sur les smartphones et tablettes Android compatibles, pas sur Android TV. L’application elle-même n’héberge pas de films ni de séries : elle agit sur certains paramètres et commandes de l’appareil.'
      ])
    ],
    'faq':[
      ('Stopododo ferme-t-il automatiquement YouTube ou Netflix ?', 'Ce n’est pas une fonction garantie. Il peut tenter de mettre en pause les lecteurs compatibles, mais ne promet pas de fermer une application.'),
      ('Si la vidéo ne se met pas en pause, que faire ?', 'Essayez la coupure du son multimédia ou le verrouillage de l’écran, puis vérifiez le comportement avec votre lecteur.'),
      ('Faut-il installer un lecteur vidéo spécial ?', 'Non. Stopododo n’est pas un lecteur vidéo et s’utilise avec les applications compatibles de votre appareil.')
    ]
  }
}

# Descriptions should match content: no invented claim of global compatibility.
for key,post in GUIDES.items():
 assert len(post['sections'])>=4


def duration_s(lang):
 p=ROOT/'assets/videos'/f'{lang}.mp4'
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nk=1:nw=1',str(p)],capture_output=True,text=True,check=True)
 return round(float(r.stdout.strip()))

def video_poster(lang):
 target=ROOT/'assets/img/video-posters'/f'{lang}.webp'
 target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():
  subprocess.run(['ffmpeg','-v','error','-y','-ss','00:00:03','-i',str(ROOT/'assets/videos'/f'{lang}.mp4'),'-frames:v','1','-vf','scale=480:-2','-quality','78',str(target)],check=True)
 return target

def write_videos():
 tmpl=ENV.get_template('video.html.j2')
 for lang,locale in LANGS.items():
  t=T[lang]
  sec=duration_s(lang)
  page=ROOT/lang/VIDEO_SUFFIX
  schema={'@context':'https://schema.org','@type':'VideoObject','name':t['videoLabel'],'description':t['videoDesc']+' '+t['lead'],'thumbnailUrl':f'{BASE}/assets/img/video-posters/{lang}.webp','contentUrl':f'{BASE}/assets/videos/{lang}.mp4','duration':f'PT{sec}S','inLanguage':locale,'url':f'{BASE}/{lang}/{VIDEO_SUFFIX}'}
  # Google requires uploadDate for video rich results. Do not fabricate it in a draft.
  release_date=os.getenv('STOPODODO_VIDEO_PUBLICATION_DATE','').strip()
  if release_date:
   d=datetime.fromisoformat(release_date)
   if not d.tzinfo:raise ValueError('STOPODODO_VIDEO_PUBLICATION_DATE must have a timezone offset')
   schema['uploadDate']=release_date
  page.write_text(tmpl.render(t=t,lang=lang,langtag=locale,direction='rtl' if lang=='ar' else 'ltr',lang_map=LANGS,lang_names=NAMES,base=BASE,canonical=f'{BASE}/{lang}/{VIDEO_SUFFIX}',prefix='../',schema=json.dumps(schema,ensure_ascii=False).replace('</','<\\/'),seconds=sec),encoding='utf-8')


def write_guides():
 tmpl=ENV.get_template('guide.html.j2')
 for name,p in GUIDES.items():
  path=ROOT/'fr'/name
  crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Accueil Stopododo','item':f'{BASE}/fr/index.html'},{'@type':'ListItem','position':2,'name':p['heading'],'item':f'{BASE}/fr/{name}'}]}
  path.write_text(tmpl.render(post=p,slug=name,all_guides=GUIDES,base=BASE,canonical=f'{BASE}/fr/{name}',crumbs=json.dumps(crumbs,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')


def write_sitemaps():
 ns='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'; vn='http://www.google.com/schemas/sitemap-video/1.1'
 ET.register_namespace('',ns); ET.register_namespace('xhtml',xhtml); ET.register_namespace('video',vn)
 root=ET.Element(f'{{{ns}}}urlset')
 def add_url(path,alternate=None):
  u=ET.SubElement(root,f'{{{ns}}}url')
  ET.SubElement(u,f'{{{ns}}}loc').text=f'{BASE}/{path}'
  if alternate:
   for lang,code in LANGS.items():ET.SubElement(u,f'{{{xhtml}}}link',{'rel':'alternate','hreflang':code,'href':f'{BASE}/{lang}/{alternate}'})
   ET.SubElement(u,f'{{{xhtml}}}link',{'rel':'alternate','hreflang':'x-default','href':f'{BASE}/fr/{alternate}'})
 for lang in LANGS: add_url(f'{lang}/index.html','index.html')
 for lang in LANGS: add_url(f'{lang}/{VIDEO_SUFFIX}',VIDEO_SUFFIX)
 for name in GUIDES: add_url(f'fr/{name}')
 # The 4 historic root legal URLs are already public on main. They must be retained at deployment.
 for name in ['confidentialite.html','conditions.html','accessibilite.html','contact.html']:add_url(name)
 ET.ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)

 vroot=ET.Element(f'{{{ns}}}urlset')
 for lang in LANGS:
  t=T[lang];u=ET.SubElement(vroot,f'{{{ns}}}url');ET.SubElement(u,f'{{{ns}}}loc').text=f'{BASE}/{lang}/{VIDEO_SUFFIX}'
  v=ET.SubElement(u,f'{{{vn}}}video')
  for key,value in {'thumbnail_loc':f'{BASE}/assets/img/video-posters/{lang}.webp','title':t['videoLabel'],'description':t['videoDesc']+' '+t['lead'],'content_loc':f'{BASE}/assets/videos/{lang}.mp4','duration':str(duration_s(lang))}.items(): ET.SubElement(v,f'{{{vn}}}{key}').text=value
 ET.ElementTree(vroot).write(ROOT/'video-sitemap.xml',encoding='utf-8',xml_declaration=True)
 (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/video-sitemap.xml\n',encoding='utf-8')


def main():
 with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(video_poster,LANGS))
 write_videos();write_guides();write_sitemaps()
 print('SEO V6 generated: 10 video watch pages, 3 French articles, 2 sitemaps, robots.txt and 10 real video thumbnails.')
if __name__=='__main__': main()
