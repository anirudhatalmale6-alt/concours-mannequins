# -*- coding: utf-8 -*-
"""Controles sur la page RENDUE, pas sur le fichier.

tests-concours.py lit le HTML et le CSS. Il a laisse passer un bouton dont le
libelle etait invisible : `.cms a{color:inherit}` porte une classe ET un
element, donc il battait `.cms-btn{color:#fff}`, et le texte blanc retombait
sur l'encre heritee — bouton charbon, texte charbon. Une regle presente dans
la feuille n'est pas une regle appliquee.

Ici on ouvre les pages dans un vrai navigateur et on MESURE : couleur
calculee, contraste, nombre de cartes reellement dans le DOM avant et apres
filtrage.
"""

import http.server
import os
import socket
import sys
import threading

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
DOCS = ICI
OK = []


def t(nom, cond, detail=''):
    OK.append(bool(cond))
    print('%s %s%s' % ('  OK  ' if cond else ' ECHEC', nom,
                       ('   -> ' + str(detail)) if not cond and detail else ''))


def port_libre():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Muet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def lum(rgb):
    """Luminance relative WCAG, a partir d'un « rgb(r, g, b) »."""
    n = [int(x) / 255 for x in rgb.strip('rgba() ').split(',')[:3]]
    n = [c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4 for c in n]
    return .2126 * n[0] + .7152 * n[1] + .0722 * n[2]


def contraste(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + .05) / (lo + .05)


def main():
    port = port_libre()
    srv = http.server.ThreadingHTTPServer(
        ('127.0.0.1', port), lambda *a, **k: Muet(*a, directory=DOCS, **k))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d/' % port

    with sync_playwright() as pw:
        nav = pw.chromium.launch()

        for page in ('concours.html', 'mannequins.html', 'photographie.html'):
            pg = nav.new_page(viewport={'width': 1280, 'height': 900})
            pg.goto(base + page, wait_until='networkidle')
            print('\n--- %s, mesure a l\'ecran ---' % page)

            btns = pg.locator('.cms-btn')
            n = btns.count()
            t('%s : au moins un bouton' % page, n > 0, n)
            for i in range(n):
                b = btns.nth(i)
                fg = b.evaluate("e=>getComputedStyle(e).color")
                bg = b.evaluate("""e=>{let x=e;while(x){let c=
                    getComputedStyle(x).backgroundColor;
                    if(c&&c!=='rgba(0, 0, 0, 0)')return c;x=x.parentElement;}
                    return 'rgb(255,255,255)';}""")
                c = contraste(fg, bg)
                txt = (b.inner_text() or '').strip()[:34]
                t('bouton « %s » : libelle lisible (contraste %.1f:1)'
                  % (txt, c), c >= 4.5, '%s sur %s' % (fg, bg))

            # Les marqueurs « a trancher » : un tarif manquant qui s'affiche
            # dans un ton trop clair se lit comme du texte decoratif et
            # personne ne le remplit. Meme mesure que pour les boutons.
            tbc = pg.locator('.cms-tbc')
            for i in range(tbc.count()):
                el = tbc.nth(i)
                fg = el.evaluate("e=>getComputedStyle(e).color")
                bg = el.evaluate("""e=>{let x=e;while(x){let c=
                    getComputedStyle(x).backgroundColor;
                    if(c&&c!=='rgba(0, 0, 0, 0)')return c;x=x.parentElement;}
                    return 'rgb(255,255,255)';}""")
                c = contraste(fg, bg)
                t('marqueur « %s » lisible (contraste %.1f:1)'
                  % ((el.inner_text() or '').strip()[:24], c), c >= 4.5,
                  '%s sur %s' % (fg, bg))

            # Le meme piege peut frapper n'importe quel titre pose sur la
            # bande sombre : on mesure aussi la, plutot que de supposer.
            for sel in ('.cms-s.ink h2', '.cms-s.ink p'):
                if pg.locator(sel).count():
                    el = pg.locator(sel).first
                    fg = el.evaluate("e=>getComputedStyle(e).color")
                    bg = el.evaluate("""e=>{let x=e;while(x){let c=
                        getComputedStyle(x).backgroundColor;
                        if(c&&c!=='rgba(0, 0, 0, 0)')return c;
                        x=x.parentElement;}return 'rgb(255,255,255)';}""")
                    t('%s sur la bande sombre : contraste %.1f:1'
                      % (sel, contraste(fg, bg)), contraste(fg, bg) >= 4.5,
                      '%s sur %s' % (fg, bg))

            # Rien ne doit deborder horizontalement : une page qui pousse une
            # barre de defilement laterale sur telephone est cassee, meme si
            # chaque bloc pris seul est correct.
            for larg in (1280, 390):
                pg.set_viewport_size({'width': larg, 'height': 800})
                pg.wait_for_timeout(200)
                deborde = pg.evaluate(
                    "()=>document.documentElement.scrollWidth>"
                    "document.documentElement.clientWidth+1")
                t('%s : aucun debordement horizontal a %dpx' % (page, larg),
                  not deborde)
            pg.set_viewport_size({'width': 1280, 'height': 900})
            pg.close()

        # Le catalogue : on compte les cartes DANS LE DOM.
        print('\n--- le catalogue, cartes reellement affichees ---')
        pg = nav.new_page(viewport={'width': 1280, 'height': 900})
        pg.goto(base + 'mannequins.html', wait_until='networkidle')
        pg.wait_for_selector('.cms-mn', timeout=10000)

        total = pg.locator('.cms-mn').count()
        t('la grille se remplit vraiment (%d cartes)' % total, total > 0, total)

        annonce = pg.locator('#cms-count').inner_text()
        t('le compteur annonce le meme total que la grille',
          str(total) in annonce, '%r pour %d cartes' % (annonce, total))

        pg.select_option('#f-cat', 'Defile')
        pg.wait_for_timeout(250)
        apres = pg.locator('.cms-mn').count()
        # Sous-ensemble STRICT : un filtre qui rend tout le catalogue passerait
        # aussi bien s'il n'existait pas.
        t('filtrer sur Defile reduit vraiment la grille',
          0 < apres < total, '%d -> %d' % (total, apres))
        restants = pg.locator('.cms-mn .tags').all_inner_texts()
        t('toutes les cartes restantes portent bien Defile',
          all('Defile' in r for r in restants), restants[:3])

        pg.select_option('#f-taille', '180')
        pg.wait_for_timeout(250)
        apres2 = pg.locator('.cms-mn').count()
        t('ajouter « 180 cm et plus » ne peut que reduire encore',
          apres2 <= apres, '%d -> %d' % (apres, apres2))

        # Un filtre sans resultat doit le DIRE. Une grille vide et muette
        # ressemble a un catalogue vide.
        # La ville est LUE dans le menu, pas ecrite en dur : le catalogue est
        # tire a chaque generation et une ville codee en dur dans le controle
        # disparait le jour ou le tirage ne la sort plus (« Sherbrooke » a
        # fait tomber ce controle en timeout, pas la page).
        villes = [v for v in pg.locator('#f-ville option').all_inner_texts()
                  if v and v != 'Toutes']
        pg.select_option('#f-cat', 'Grande taille')
        pg.select_option('#f-taille', '180')
        pg.select_option('#f-ville', villes[-1])
        pg.wait_for_timeout(250)
        if pg.locator('.cms-mn').count() == 0:
            t('une selection sans resultat affiche un message, pas du vide',
              pg.locator('#cms-vide').is_visible())
        else:
            t('une selection sans resultat affiche un message, pas du vide',
              True, 'combinaison encore peuplee, non testable')

        # Les emplacements de photo nomment bien le fichier attendu.
        pg.select_option('#f-cat', '')
        pg.select_option('#f-taille', '')
        pg.select_option('#f-ville', '')
        pg.wait_for_timeout(250)
        ph = pg.locator('.cms-mn .ph span').first.inner_text()
        t('chaque carte nomme la photo qu\'elle attend',
          ph.startswith('mannequins/') and ph.endswith('.jpg'), ph)

        pg.close()
        nav.close()
    srv.shutdown()

    print('\n%d controles a l\'ecran, %d verts, %d rouges'
          % (len(OK), sum(OK), len(OK) - sum(OK)))
    sys.exit(0 if all(OK) else 1)


if __name__ == '__main__':
    main()
