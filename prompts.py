# -*- coding: utf-8 -*-
"""Ecrit PROMPTS-IMAGES.md a partir de la liste IMAGES de build.py.

La liste des emplacements n'est ecrite qu'a UN endroit. Recopiee ici a la
main, elle finirait par diverger du HTML, et c'est le client qui
decouvrirait le fichier manquant.
"""

import os

from build import IMAGES

ICI = os.path.dirname(os.path.abspath(__file__))

REGLES = """\
Trois regles a garder sur ces images, quel que soit l'outil :

1. **Aucun logo, aucune marque, aucun texte lisible.** Un generateur invente
   des logos qui ressemblent a ceux de vraies enseignes : ce serait la marque
   d'un tiers posee sur ta page.
2. **Aucun visage reconnaissable.** De dos, de loin, hors champ, ou
   simplement absent. Un visage genere ressemble toujours a quelqu'un qui
   n'a rien signe — et sur une page de concours de miss et un catalogue de
   mannequins, c'est exactement le reproche qu'on ne peut pas se permettre.
3. **La palette du site** : charbon, gris perle, blanc casse. Lumiere douce,
   pas de saturation, pas de neon. Les pages sont volontairement sobres ;
   une image survoltee les casse.

Format : JPG, 1600 px de large minimum, moins de 400 ko apres compression.
Depose le fichier au chemin indique, a cote de la page. Il n'y a AUCUN HTML
a modifier : tant que le fichier n'existe pas, la page affiche un cadre qui
nomme le fichier attendu, et des qu'il existe elle affiche l'image.
"""

STYLE = ('Photographie realiste, lumiere naturelle douce, palette sobre '
         '(charbon, gris perle, blanc casse), sans saturation, sans texte, '
         'sans logo, sans visage reconnaissable.')


def main():
    # Le nombre est COMPTE, jamais ecrit : la premiere version disait « six »
    # pour cinq emplacements, et un document qui se trompe sur ce qu'il
    # contient lui-meme n'est plus une reference.
    o = ['# Les images des deux pages', '',
         '%d emplacements, %d fichiers a deposer.' % (len(IMAGES), len(IMAGES)),
         '', REGLES, '', '---', '']
    for i, (src, ratio, sujet) in enumerate(IMAGES, 1):
        o += ['## %d. `%s`' % (i, src),
              '',
              '- Ratio : **%s**' % ratio,
              '- Sujet : %s' % sujet,
              '',
              '> %s %s' % (sujet, STYLE),
              '']
    # Les photos du catalogue ne sont PAS a generer : ce sont les vraies.
    o += ['---', '',
          '## Les photos du catalogue mannequins', '',
          'Elles ne se generent pas et ne se telechargent nulle part.',
          '',
          'Chaque carte attend un fichier `mannequins/MN-0xx.jpg` — la photo',
          'de la mannequin concernee, prise ou fournie par elle, avec son',
          'accord ecrit. Une photo reprise ailleurs, c\'est le book d\'une',
          'autre agence et le droit a l\'image de quelqu\'un qui n\'a rien',
          'accepte. Tant que la photo n\'est pas la, la carte affiche un',
          'cadre qui nomme le fichier attendu : le catalogue reste',
          'presentable pendant qu\'il se remplit.', '',
          'Ratio des photos de fiche : **3/4** (portrait), 1200 px de large',
          'minimum.', '']

    p = os.path.join(ICI, 'PROMPTS-IMAGES.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(o))
    print('%s  %d octets, %d emplacements'
          % (p, os.path.getsize(p), len(IMAGES)))


if __name__ == '__main__':
    main()
