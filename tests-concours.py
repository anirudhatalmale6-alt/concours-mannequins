# -*- coding: utf-8 -*-
"""Controles sur les deux pages generees.

Ce qui est verifie ici n'est pas « la page existe » mais « la page dit vrai » :
les nombres affiches sortent bien du catalogue, aucune couleur n'a ete
inventee, aucun nom de concours existant n'a ete ecrit, les cases de
consentement sont bien obligatoires, et le catalogue est coherent fiche par
fiche — pas seulement en moyenne.
"""

import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from donnees import CATEGORIES, CONCOURS, mannequins   # noqa: E402
from style import CSS                                   # noqa: E402

OK = []


def t(nom, cond, detail=''):
    OK.append(bool(cond))
    print('%s %s%s' % ('  OK  ' if cond else ' ECHEC',
                       nom, ('   -> ' + str(detail)) if not cond and detail else ''))


subprocess.run([sys.executable, os.path.join(ICI, 'build.py')],
               check=True, stdout=subprocess.DEVNULL)

D = ICI
P = os.path.join(ICI, 'paste')
lire = lambda p: open(p, encoding='utf-8').read()
CONC = lire(os.path.join(D, 'concours.html'))
MANN = lire(os.path.join(D, 'mannequins.html'))
CAT = json.load(open(os.path.join(D, 'catalogue.json'), encoding='utf-8'))
FICHES = mannequins()

print('\n--- le catalogue est coherent fiche par fiche ---')

t('le catalogue JSON contient bien les %d fiches generees' % len(FICHES),
  len(CAT) == len(FICHES) and len(CAT) > 0, len(CAT))

# Chaque fiche doit tenir dans la fourchette de SA categorie principale. Une
# moyenne correcte cacherait un mannequin defile de 1,62 m.
hors = [(m['id'], m['categories'][0], m['taille_cm'])
        for m in CAT
        if not (CATEGORIES[m['categories'][0]][0] <= m['taille_cm']
                <= CATEGORIES[m['categories'][0]][1])]
t('aucune taille hors de la fourchette de sa categorie principale',
  not hors, hors[:4])

horsc = [(m['id'], m['categories'][0], m['confection'])
         for m in CAT
         if not (CATEGORIES[m['categories'][0]][2] <= m['confection']
                 <= CATEGORIES[m['categories'][0]][3])]
t('aucune confection hors de la fourchette de sa categorie principale',
  not horsc, horsc[:4])

# Une deuxieme categorie n'a de sens que si la fiche entre AUSSI dans ses
# fourchettes. « Defile / Grande taille » sur la meme fiche ne veut rien dire.
absurdes = [m['id'] for m in CAT for c in m['categories'][1:]
            if not (CATEGORIES[c][0] <= m['taille_cm'] <= CATEGORIES[c][1]
                    and CATEGORIES[c][2] <= m['confection'] <= CATEGORIES[c][3])]
t('aucune seconde categorie incompatible avec les mensurations',
  not absurdes, absurdes[:4])

t('toutes les confections sont paires, comme les tailles reelles',
  all(m['confection'] % 2 == 0 for m in CAT))

t('chaque fiche parle FR (langue de base du catalogue)',
  all('FR' in m['langues'] for m in CAT))

t('les identifiants sont uniques',
  len({m['id'] for m in CAT}) == len(CAT))

# L'ensemble ne doit pas etre monochrome : une seule categorie partout ferait
# passer tous les controles de fourchette sans qu'il y ait de catalogue.
cats = {c for m in CAT for c in m['categories']}
t('le catalogue couvre au moins 5 des %d categories' % len(CATEGORIES),
  len(cats) >= 5, sorted(cats))
gros = max(sum(1 for m in CAT if m['categories'][0] == c) for c in cats)
t('aucune categorie ne represente plus de la moitie du catalogue',
  gros <= len(CAT) // 2, '%d/%d' % (gros, len(CAT)))

print('\n--- les nombres affiches sortent du catalogue ---')

villes = {m['ville'] for m in CAT}
tmin = min(m['taille_cm'] for m in CAT)
tmax = max(m['taille_cm'] for m in CAT)
t('la page annonce le vrai nombre de profils (%d)' % len(CAT),
  '%d profils' % len(CAT) in MANN)
t('la page annonce le vrai nombre de villes (%d)' % len(villes),
  '%d villes' % len(villes) in MANN)
t('la page annonce le vrai nombre de categories (%d)' % len(cats),
  '%d categories' % len(cats) in MANN)
t('la page annonce la vraie fourchette de tailles (%d-%d cm)' % (tmin, tmax),
  'de %d a\n%d cm' % (tmin, tmax) in MANN or 'de %d a %d cm' % (tmin, tmax) in MANN)

# Aucune fiche n'est ecrite en dur dans le HTML : elles viennent du JSON.
en_dur = [m['id'] for m in CAT if m['id'] in MANN]
t('aucune fiche n\'est ecrite en dur dans la page',
  not en_dur, en_dur[:4])

print('\n--- le filtre filtre vraiment ---')


def garde(m, cat=None, ville=None, taille=None, exp=None, lg=None, dispo=None):
    """Meme logique que le filtre du navigateur, rejouee ici."""
    if cat and cat not in m['categories']:
        return False
    if ville and m['ville'] != ville:
        return False
    if taille and m['taille_cm'] < taille:
        return False
    if exp and m['experience'] != exp:
        return False
    if lg and lg not in m['langues']:
        return False
    if dispo and not m['disponible']:
        return False
    return True


# Une assertion dont les deux cotes valent la population entiere passerait
# meme si le filtre etait supprime. On EXIGE donc un sous-ensemble strict.
sel = [m for m in CAT if garde(m, cat='Defile')]
t('le filtre Defile rend un sous-ensemble STRICT et non vide',
  0 < len(sel) < len(CAT), '%d/%d' % (len(sel), len(CAT)))
t('toutes les fiches rendues par le filtre Defile portent bien Defile',
  all('Defile' in m['categories'] for m in sel))

sel2 = [m for m in CAT if garde(m, taille=176)]
t('le filtre « 176 cm et plus » est strict et non vide',
  0 < len(sel2) < len(CAT), '%d/%d' % (len(sel2), len(CAT)))
t('aucune fiche sous 176 cm ne passe le filtre 176',
  all(m['taille_cm'] >= 176 for m in sel2))

sel3 = [m for m in CAT if garde(m, dispo=True)]
t('le filtre disponibilite est strict et non vide',
  0 < len(sel3) < len(CAT), '%d/%d' % (len(sel3), len(CAT)))

sel4 = [m for m in CAT if garde(m, cat='Defile', ville='Montreal', taille=178)]
t('trois filtres combines restent coherents',
  all('Defile' in m['categories'] and m['ville'] == 'Montreal'
      and m['taille_cm'] >= 178 for m in sel4))

t('le compteur annonce le sous-ensemble ET le total, jamais le seul sous-ensemble',
  "' sur '+F.length" in MANN)

t('un catalogue illisible est annonce, pas affiche comme un catalogue vide',
  'n\\\'a pas pu etre charge' in MANN)

print('\n--- aucune couleur inventee ---')

PALETTE = {
    '#1c1a24', '#8b8698', '#ececf1', '#faf9fc', '#f2f0f6', '#1b1922',
    '#2b2833', '#f3f1f5', '#c9c6d0', '#6f6b7a', '#dcd9e4', '#e6e3ee',
    '#d8d5e0', '#241f2d', '#a5a1b0', '#d6d3de', '#f6f5f9', '#e9e7ef',
    '#4a4753', '#fff', '#eaf6ee', '#1f7a45', '#eee',
}
trouvees = {c.lower() for c in re.findall(r'#[0-9a-fA-F]{3,6}\b', CSS)}
t('la feuille de style n\'utilise que la palette Influus + 2 tons de statut',
  trouvees <= PALETTE, sorted(trouvees - PALETTE))

print('\n--- le style ne peut pas etre ecrase par le theme hote ---')

# Un h1{} nu dans le theme du client bat n'importe quelle regle heritee : la
# feuille doit donc TOUT cibler en descendant de .cms.
regles = [r.split('{')[0].strip()
          for r in re.split(r'}', re.sub(r'/\*.*?\*/', '', CSS, flags=re.S))
          if '{' in r and not r.strip().startswith('@')]
selecteurs = [s for r in regles for s in r.split(',')]
nus = [s.strip() for s in selecteurs
       if s.strip() and not s.strip().startswith('.cms')
       and not s.strip().startswith('@')]
t('toutes les regles descendent de .cms (aucun selecteur nu)', not nus, nus[:5])

t('la page reste lisible sur telephone (points de rupture presents)',
  '@media (max-width:760px)' in CSS and '@media (max-width:460px)' in CSS)

print('\n--- le concours n\'engage rien qui ne soit valide ---')

# « Miss » + un pays ou une region est une marque deposee a peu pres partout.
INTERDITS = ['miss france', 'miss univers', 'miss universe', 'miss world',
             'miss monde', 'miss canada', 'miss quebec', 'miss belgique',
             'miss earth', 'miss international', 'miss teen']
bas = (CONC + MANN).lower()
present = [m for m in INTERDITS if m in bas]
t('aucun nom de concours existant n\'est ecrit dans les pages',
  not present, present)

t('le nom du concours est le placeholder, donc remplacable d\'un seul coup',
  CONC.count(CONCOURS['nom']) >= 1 and CONCOURS['nom'] == 'Concours Horizon')

t('les champs a trancher restent visibles comme tels ([A CONFIRMER], [NOM])',
  '[NOM]' in CONC and 'A CONFIRMER' in CONC.upper())

t('la page dit que l\'inscription est gratuite',
  'gratuit' in CONC.lower())

t('la page annonce l\'age minimum sans ambiguite',
  '18 ans' in CONC)

print('\n--- consentement et donnees personnelles ---')

for nom, page in (('concours', CONC), ('mannequins', MANN)):
    cases = re.findall(r'<input type="checkbox"[^>]*>', page)
    t('%s : au moins deux cases de consentement' % nom, len(cases) >= 2,
      len(cases))
    t('%s : chaque case de consentement est obligatoire' % nom,
      all('required' in c for c in cases),
      [c for c in cases if 'required' not in c])
    t('%s : le droit a l\'image est nomme explicitement' % nom,
      'Droit a l\'image' in page or "Droit a l&#x27;image" in page)

t('le concours dit ce que deviennent les photos non retenues',
  'effac' in CONC.lower())
t('le catalogue exige la majorite a la candidature',
  '18 ans ou plus' in MANN)

# Un formulaire branche avant d'avoir une adresse de reception collecte des
# donnees personnelles que personne n'est en mesure de traiter.
actions = re.findall(r'<form[^>]*action="([^"]*)"', CONC + MANN)
t('aucun formulaire n\'envoie vers une adresse inventee',
  all(a == '#' for a in actions), actions)
t('les deux pages disent que le formulaire n\'envoie encore rien',
  CONC.count('n\'envoie encore rien') + MANN.count('n\'envoie encore rien') >= 2
  or (CONC + MANN).count('envoie encore rien') >= 2)

print('\n--- vie privee du catalogue ---')

t('aucune fiche ne porte un nom de famille complet, seulement une initiale',
  all(re.fullmatch(r'[A-Z]\.', m['initiale']) for m in CAT))
t('les mensurations completes ne sont pas dans le catalogue public',
  not any(k in json.dumps(CAT) for k in ('poitrine', 'hanches', 'buste')))
t('la page explique pourquoi le book complet n\'est pas en acces libre',
  'securite' in MANN.lower() and 'Sur demande' in MANN)
t('la page dit que les fiches sont des demonstrations',
  'demonstration' in MANN.lower())

print('\n--- les images ---')

from build import IMAGES   # noqa: E402
manquantes = [src for src, _, _ in IMAGES
              if src.startswith('images/') and src not in CONC + MANN]
t('chaque emplacement d\'image declare apparait bien dans une page',
  not manquantes, manquantes)
t('un emplacement vide NOMME le fichier attendu au lieu d\'une image cassee',
  'Image a deposer' in CONC and 'data-img=' in CONC)
# La regle vise l'ATTRIBUT HTML onerror="..." — un onerror a guillemets
# imbriques se casse des qu'un editeur reencode le bloc. Un handler pose en
# JavaScript (x.onerror = function(){}) n'a pas ce probleme : la premiere
# version du controle interdisait les deux et signalait un faux positif.
inline = [p for p in (CONC, MANN) if 'onerror="' in p or "onerror='" in p]
t('aucun attribut onerror inline (le remplacement passe par des data-)',
  not inline, len(inline))
t('les cartes du catalogue nomment aussi leur photo manquante',
  'Photo a deposer' in MANN)
t('le ratio est pose d\'avance pour que la page ne saute pas',
  'aspect-ratio' in CSS)

print('\n--- le bloc a coller ---')

for nom in ('concours', 'mannequins'):
    b = lire(os.path.join(P, nom + '.html'))
    t('%s : le bloc a coller ne contient ni <html> ni <head>' % nom,
      '<html' not in b.lower() and '<head' not in b.lower())
    t('%s : le bloc emporte sa police et son style' % nom,
      'fonts.googleapis.com' in b and '<style>' in b)
    t('%s : le bloc et la page d\'apercu montrent le meme contenu' % nom,
      b.count('cms-s') == lire(os.path.join(D, nom + '.html')).count('cms-s'))

print('\n--- echappement ---')

t('le HTML genere n\'a pas de balise ouverte non fermee evidente',
  CONC.count('<section') == CONC.count('</section>')
  and MANN.count('<section') == MANN.count('</section>'))
t('les apostrophes des donnees ne cassent pas le JSON du catalogue',
  json.loads(json.dumps(CAT)) == CAT)

print('\n%d controles, %d verts, %d rouges'
      % (len(OK), sum(OK), len(OK) - sum(OK)))
sys.exit(0 if all(OK) else 1)
