# -*- coding: utf-8 -*-
"""Donnees des deux pages : le concours de miss et le catalogue mannequins.

TOUT CE QUI EST ICI EST FICTIF ET ASSUME COMME TEL. Aucune personne reelle,
aucun nom de famille complet, aucune photo de quelqu'un. Un catalogue de
mannequins est exactement l'endroit ou une identite inventee qui ressemble a
une vraie personne devient un probleme : on remplit avec des profils de
demonstration, et le client les remplace par ses mannequins sous contrat.

Le nom du concours est un PLACEHOLDER (voir CONCOURS['nom']). Je n'ecris pas
le nom d'un concours existant : « Miss » suivi d'un pays ou d'une region est,
a peu pres partout, une marque deposee detenue par un organisateur. Le client
met le sien, c'est une seule chaine a changer.

Regle de coherence du tirage : les categories NE SONT PAS tirees a part des
mensurations. Un profil de defile se tire dans les grandes tailles, une fiche
« grande taille » dans les confections hautes. Tire independamment, chaque
fiche reste plausible et l'ensemble devient faux — un mannequin defile de
1,62 m a cote d'une fiche « curve » en taille 34.
"""

import random

# --------------------------------------------------------------------------
# LE CONCOURS
# --------------------------------------------------------------------------

CONCOURS = {
    # <<< A REMPLACER : nom de scene du concours. Placeholder assume. >>>
    'nom': 'Concours Horizon',
    'edition': 'Edition 2027',
    'ville': 'Montreal',
    'lieu': '[SALLE A CONFIRMER]',
    'date_finale': '[DATE A CONFIRMER]',
    'accroche': 'Un concours de miss pense pour les candidates : '
                'un reglement ecrit, un jury nomme, des etapes datees.',
    'sous_accroche': 'Candidatures ouvertes aux residentes du Quebec de '
                     '18 ans et plus. Inscription gratuite.',
}

ETAPES = [
    ('1', 'Candidature en ligne',
     'Le formulaire en bas de page. Deux photos recentes suffisent : une de '
     'visage, une en pied. Pas de book professionnel exige — c\'est justement '
     'ce que le concours doit apporter.'),
    ('2', 'Presalection sur dossier',
     'Le comite lit toutes les candidatures. Chaque candidate recoit une '
     'reponse, retenue ou non. Une candidature sans reponse est une '
     'candidate perdue pour l\'edition suivante.'),
    ('3', 'Casting regional',
     'Rencontre de groupe : presentation, demarche, entretien court. '
     'Filme uniquement avec accord ecrit, et jamais diffuse sans un second '
     'accord.'),
    ('4', 'Demi-finale',
     'Les candidates retenues travaillent la scene avec un coach. '
     'C\'est la que se decide le tableau final.'),
    ('5', 'Finale publique',
     'Soiree ouverte au public, jury nomme a l\'avance, resultats annonces '
     'le soir meme.'),
]

CRITERES = [
    ('Age', '18 ans revolus au jour de la finale.'),
    ('Residence', 'Resider au Quebec depuis au moins six mois.'),
    ('Taille', 'Aucun minimum. Un concours de miss n\'est pas un casting de '
               'defile — le catalogue mannequin, lui, a ses criteres.'),
    ('Etat civil', 'Sans condition. Ni le statut matrimonial ni la '
                   'maternite n\'entrent dans les criteres.'),
    ('Casier', 'Aucune verification n\'est demandee a la candidature. '
               'La lauréate signe un engagement de representation.'),
    ('Frais', 'Aucun. Ni inscription, ni dossier, ni tenue a acheter.'),
]

JURY = [
    ('[NOM]', 'Presidence du jury', 'A nommer avant l\'ouverture des candidatures.'),
    ('[NOM]', 'Direction artistique', 'A nommer.'),
    ('[NOM]', 'Representation des editions precedentes', 'A nommer.'),
    ('[NOM]', 'Partenaire principal', 'A nommer.'),
    ('[NOM]', 'Presse', 'A nommer.'),
]

PRIX = [
    ('La lauréate', [
        'Le titre pour un an et le contrat de representation qui va avec.',
        'Un book professionnel complet, shoote et retouche.',
        'Une dotation en numeraire — montant a fixer, annonce avant '
        'l\'ouverture des candidatures.',
    ]),
    ('Les deux dauphines', [
        'Book professionnel.',
        'Entree directe au catalogue mannequins.',
    ]),
    ('Toutes les finalistes', [
        'Les photos de la finale, libres d\'usage pour leur propre book.',
        'Une fiche au catalogue si elles le souhaitent.',
    ]),
]

FAQ = [
    ('Le concours est-il payant ?',
     'Non. Ni inscription, ni frais de dossier, ni tenue a acheter. Un '
     'concours qui fait payer ses candidates n\'est pas un concours, c\'est '
     'une billetterie.'),
    ('Faut-il un book ou de l\'experience ?',
     'Non. Deux photos prises au telephone suffisent pour candidater.'),
    ('Que deviennent mes photos si je ne suis pas retenue ?',
     'Elles sont effacees a la fin de l\'edition. Elles ne servent a rien '
     'd\'autre qu\'a la selection, et surement pas a une publicite.'),
    ('Puis-je candidater si j\'ai moins de 18 ans ?',
     'Pas a cette edition. Ouvrir aux mineures demande un cadre a part : '
     'accord ecrit des deux parents, horaires encadres, categories separees. '
     'Ce n\'est pas une case a cocher, c\'est un reglement different.'),
    ('Y a-t-il une epreuve en maillot ?',
     'Non. Le format retenu est : presentation, tenue de ville, tenue de '
     'soiree, entretien.'),
    ('Ou est le reglement complet ?',
     'Il doit etre en ligne et telechargeable AVANT la premiere candidature. '
     'Tant qu\'il n\'y est pas, la page affiche un lien inactif plutot qu\'un '
     'lien qui ment.'),
]

# Ce que le client doit trancher avant que la page parte en ligne. Affiche
# tel quel dans le LISEZ-MOI : une page de concours sans ces reponses est
# une page qui prend des engagements que personne n'a valides.
A_TRANCHER = [
    'Le nom du concours (placeholder « Concours Horizon » partout).',
    'La date et la salle de la finale.',
    'Le montant de la dotation, annonce avant l\'ouverture des candidatures.',
    'Les cinq membres du jury.',
    'Le reglement complet, ecrit et telechargeable, avant la premiere '
    'candidature.',
    'L\'entite juridique organisatrice, pour les mentions legales.',
    'Ou arrivent les candidatures : adresse de reception du formulaire.',
]

# --------------------------------------------------------------------------
# LE CATALOGUE MANNEQUINS
# --------------------------------------------------------------------------

PRENOMS = [
    'Amelie', 'Sarah', 'Ines', 'Camille', 'Noemie', 'Lea', 'Yasmine',
    'Charlotte', 'Maya', 'Elodie', 'Rania', 'Juliette', 'Sofia', 'Clara',
    'Nadia', 'Emma', 'Anais', 'Lina', 'Rosalie', 'Manon', 'Kenza', 'Alice',
    'Florence', 'Imane', 'Marion', 'Chloe', 'Selma', 'Beatrice', 'Naima',
    'Justine', 'Dounia', 'Victoria', 'Salma', 'Gabrielle', 'Lydia', 'Eve',
    'Meriem', 'Coralie', 'Assia', 'Sandrine', 'Hana', 'Marilou', 'Nour',
    'Ophelie', 'Samira', 'Delphine', 'Leila', 'Audrey',
]

VILLES = [
    ('Montreal', 'QC', 34), ('Laval', 'QC', 10), ('Longueuil', 'QC', 8),
    ('Quebec', 'QC', 10), ('Gatineau', 'QC', 6), ('Sherbrooke', 'QC', 4),
    ('Trois-Rivieres', 'QC', 3),
    ('Toronto', 'ON', 14), ('Ottawa', 'ON', 7), ('Mississauga', 'ON', 4),
]

CHEVEUX = [('Bruns', 34), ('Noirs', 22), ('Chatains', 20), ('Blonds', 15),
           ('Roux', 5), ('Colores', 4)]
YEUX = [('Bruns', 42), ('Noisette', 20), ('Verts', 16), ('Bleus', 14),
        ('Gris', 8)]
LANGUES = [('FR', 100), ('EN', 78), ('AR', 16), ('ES', 12), ('IT', 6)]

# Categorie -> (taille min, taille max, confection min, confection max)
# C'est la table qui tient la coherence : la categorie CHOISIT la fourchette,
# elle n'est pas plaquee apres coup sur des mensurations tirees au hasard.
CATEGORIES = {
    'Defile':        (174, 182, 32, 36),
    'Editorial':     (172, 181, 32, 38),
    'Commercial':    (163, 178, 34, 42),
    'Beaute':        (160, 178, 34, 42),
    'Grande taille': (170, 180, 44, 52),
    'Evenementiel':  (162, 178, 34, 42),
}
POIDS_CAT = {'Commercial': 28, 'Beaute': 20, 'Evenementiel': 18,
             'Defile': 14, 'Editorial': 12, 'Grande taille': 8}

EXPERIENCE = [('Debutante', 30), ('Confirmee', 45), ('Professionnelle', 25)]


def _pondere(rng, table):
    """Tirage pondere. `table` = liste de (valeur, poids) ou (a, b, poids)."""
    total = sum(t[-1] for t in table)
    x = rng.uniform(0, total)
    for t in table:
        x -= t[-1]
        if x <= 0:
            return t[0] if len(t) == 2 else t[:-1]
    return table[-1][0] if len(table[-1]) == 2 else table[-1][:-1]


def mannequins(n=48, graine=20260828):
    """Profils de DEMONSTRATION. Deterministe : meme graine, meme catalogue,
    donc les captures d'ecran et les controles parlent du meme jeu."""
    rng = random.Random(graine)
    fiches = []
    for i in range(n):
        cat = _pondere(rng, [(c, p) for c, p in POIDS_CAT.items()])
        tmin, tmax, cmin, cmax = CATEGORIES[cat]
        taille = rng.randint(tmin, tmax)
        # Confection par pas de 2, comme les tailles reelles.
        conf = rng.randrange(cmin, cmax + 1, 2)
        ville, prov = _pondere(rng, VILLES)

        # Une seconde categorie n'est possible que si les fourchettes se
        # recouvrent vraiment : sinon on affiche « Defile / Grande taille »
        # sur la meme fiche, ce qui ne veut rien dire.
        autres = [c for c in CATEGORIES
                  if c != cat
                  and CATEGORIES[c][0] <= taille <= CATEGORIES[c][1]
                  and CATEGORIES[c][2] <= conf <= CATEGORIES[c][3]]
        cats = [cat] + ([rng.choice(autres)] if autres and rng.random() < .45 else [])

        langues = ['FR']
        for lg, p in LANGUES[1:]:
            if rng.uniform(0, 100) < p:
                langues.append(lg)

        fiches.append({
            'id': 'MN-%03d' % (i + 1),
            'prenom': PRENOMS[i % len(PRENOMS)],
            'initiale': chr(rng.randrange(65, 91)) + '.',
            'ville': ville,
            'province': prov,
            'taille_cm': taille,
            'confection': conf,
            'pointure': rng.randint(36, 41),
            'cheveux': _pondere(rng, CHEVEUX),
            'yeux': _pondere(rng, YEUX),
            'categories': cats,
            'langues': langues,
            'experience': _pondere(rng, EXPERIENCE),
            'disponible': rng.random() < .72,
            'photo': 'mannequins/%s.jpg' % ('MN-%03d' % (i + 1)),
        })
    return fiches
