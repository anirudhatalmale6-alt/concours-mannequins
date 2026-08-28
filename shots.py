# -*- coding: utf-8 -*-
"""Captures des deux pages, servies pour de vrai par un serveur local.

Pas d'ouverture en file:// : le catalogue est charge en XHR et un navigateur
refuse la requete depuis file://. La grille serait restee vide et la capture
aurait montre un catalogue sans fiches — une capture qui ment sur le
livrable est pire que pas de capture.

On scrolle VERS UN SELECTEUR, jamais vers un offset en pixels : un offset est
juste le jour ou on l'ecrit et photographie le milieu de nulle part des qu'on
insere une section.
"""

import http.server
import os
import socket
import threading
import time

from playwright.sync_api import sync_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
DOCS = ICI
SHOTS = os.path.join(ICI, 'shots')


def port_libre():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Muet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    os.makedirs(SHOTS, exist_ok=True)
    port = port_libre()
    srv = http.server.ThreadingHTTPServer(
        ('127.0.0.1', port),
        lambda *a, **k: Muet(*a, directory=DOCS, **k))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = 'http://127.0.0.1:%d/' % port

    plan = [
        ('concours.html', 'concours-1-haut', None),
        ('concours.html', 'concours-2-etapes', '#etapes'),
        ('concours.html', 'concours-3-jury', '#jury'),
        ('concours.html', 'concours-4-candidature', '#candidature'),
        ('mannequins.html', 'mannequins-1-haut', None),
        ('mannequins.html', 'mannequins-2-grille', '#cms-grid'),
        ('mannequins.html', 'mannequins-3-filtre', 'FILTRE'),
        ('mannequins.html', 'mannequins-4-prive', None),
    ]

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        for page, nom, cible in plan:
            pg = nav.new_page(viewport={'width': 1280, 'height': 800})
            pg.goto(base + page, wait_until='networkidle')

            # On verifie que c'est bien NOTRE page avant de la photographier.
            assert pg.locator('.cms').count() > 0, page

            if page == 'mannequins.html':
                # La grille est remplie en XHR : on attend une carte, pas un
                # delai. Un sleep passe au vert le jour ou la machine est
                # rapide et photographie du vide le jour ou elle ne l'est pas.
                pg.wait_for_selector('.cms-mn', timeout=10000)

            if cible == 'FILTRE':
                pg.select_option('#f-cat', 'Defile')
                pg.select_option('#f-taille', '176')
                pg.wait_for_timeout(250)
                pg.locator('.cms-bar').scroll_into_view_if_needed()
            elif cible:
                pg.locator(cible).scroll_into_view_if_needed()
            elif nom.endswith('prive'):
                pg.locator('.cms-s.ink').scroll_into_view_if_needed()
            pg.wait_for_timeout(300)

            chemin = os.path.join(SHOTS, nom + '.png')
            pg.screenshot(path=chemin)
            print('%-34s %7d o' % (nom + '.png', os.path.getsize(chemin)))
            pg.close()
        nav.close()
    srv.shutdown()


if __name__ == '__main__':
    main()
