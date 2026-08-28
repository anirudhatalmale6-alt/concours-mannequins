# Concours de miss + catalogue mannequin feminin

Deux pages autonomes. Elles se collent dans un site existant ou se servent
telles quelles.

```
docs/concours.html      la page unique du concours (apercu complet)
docs/mannequins.html    le catalogue mannequin feminin
docs/catalogue.json     les fiches du catalogue
paste/concours.html     LE MEME contenu, sans <html>/<head>, a coller dans
paste/mannequins.html   un widget HTML (Elementor ou autre)
```

Pour poser les pages sur un site WordPress : ouvre `paste/concours.html`,
copie tout, colle dans un widget HTML d'une page vide. Le style et la police
voyagent avec le bloc — rien a installer, aucun theme a toucher. Pour le
catalogue, depose en plus `catalogue.json` a cote de la page.

---

## Le nom du concours est un placeholder

Partout dans la page : **« Concours Horizon »**. C'est un nom de
remplacement, a changer d'un seul coup dans `donnees.py`.

Je n'ai ecrit le nom d'aucun concours existant, et c'est volontaire :
« Miss » suivi d'un pays, d'une province ou d'une ville est presque partout
une marque deposee, detenue par un organisateur qui accorde des licences
regionales. Ce n'est pas un detail de forme — c'est ce qui decide si le
concours peut porter son nom en public.

Sont aussi laisses visibles comme tels, exprès :
`[DATE A CONFIRMER]`, `[SALLE A CONFIRMER]`, `[NOM]` pour les cinq sieges du
jury. Une page qui invente une date fait candidater des femmes sur une
soiree qui n'existe pas.

## Ce qu'il faut trancher avant de mettre la page en ligne

1. Le nom du concours.
2. La date et la salle de la finale.
3. Le montant de la dotation — **annonce avant l'ouverture des
   candidatures**, pas apres. Un montant annonce d'avance engage
   l'organisateur ; annonce apres, il se discute.
4. Les cinq membres du jury.
5. Le reglement complet, ecrit et telechargeable, **avant la premiere
   candidature**. Tant qu'il n'existe pas, la page le dit plutot que
   d'afficher un lien qui ment.
6. L'entite juridique organisatrice, pour les mentions legales.
7. L'adresse ou arrivent les candidatures.

Tant que 6 et 7 manquent, **les deux formulaires n'envoient rien** et le
disent. C'est deliberé : un formulaire branche avant d'avoir une adresse de
reception et une entite responsable collecte des noms, des dates de
naissance et des photos que personne n'est en mesure de traiter.

## Les deux cases a cocher

Chaque formulaire porte deux cases obligatoires, et elles ne sont pas
decoratives :

- **Droit a l'image.** L'autorisation donnee couvre la *selection*
  uniquement. Toute autre utilisation — affiche, reseaux sociaux, presse —
  demande un accord ecrit distinct. Sans cette separation, tu ne peux pas
  publier la photo d'une candidate non retenue, et avec une case unique et
  large tu obtiens un consentement qui ne vaut rien.
- **Donnees personnelles.** Ce que tu collectes (nom, date de naissance,
  photos) est une donnee personnelle : il faut dire a quoi elle sert,
  combien de temps elle est gardee, et comment la faire effacer. La page
  annonce l'effacement en fin d'edition pour les candidatures non retenues.

Les mineures ne passent pas par ces formulaires. Ouvrir aux moins de 18 ans
demande un cadre distinct — accord ecrit des deux parents, horaires
encadres, categories separees. Ce n'est pas une case a cocher, c'est un
reglement different.

---

## Le catalogue mannequins

48 fiches de **demonstration**, inventees, deterministes : meme graine, meme
catalogue. Elles montrent la mise en page et les filtres, et se remplacent
par les mannequins sous contrat — une entree par fiche dans `donnees.py`,
zero ligne de HTML a toucher.

Filtres : categorie, ville, taille minimale, experience, langue,
disponibilite. Le compteur affiche toujours **le sous-ensemble ET le
total** (« 12 profils sur 48 ») : « 12 profils » tout court laisse croire
que le catalogue en compte douze.

### Ce que la fiche publique montre, et ce qu'elle garde

En public : prenom + initiale, ville, taille, confection, cheveux, yeux,
langues, categories, disponibilite. De quoi faire une presalection serieuse.

Sur demande : nom complet, mensurations completes, book integral, tarifs —
transmis a un client identifie, pour un projet nomme.

Ce decoupage n'est pas de la pudeur. Une page publique qui donne le nom
complet, la ville, les mensurations et la disponibilite de jeunes femmes est
un annuaire exploitable par n'importe qui. Les agences serieuses
fonctionnent toutes ainsi, et c'est aussi ce qui te permet de dire aux
mannequins ce qui sera publie d'elles.

### Les photos

Elles ne se generent pas. Chaque carte attend `mannequins/MN-0xx.jpg` : la
photo de la personne concernee, avec son accord ecrit. Je ne genere pas de
visages pour un catalogue de mannequins — un visage genere ressemble
toujours a quelqu'un qui n'a rien signe, et c'est precisement le reproche
qu'un catalogue de mannequins ne peut pas se permettre.

Tant qu'une photo manque, la carte affiche un cadre qui **nomme le fichier
attendu**. Deposer le fichier suffit ; il n'y a aucun HTML a modifier.

---

## Les couleurs

Aucune couleur inventee. Tout sort de la palette deja en ligne sur
`influus.com/bulk-order/` et du degrade de la sphere du logo : charbon
`#1b1922`, gris `#8b8698`, blanc casse `#faf9fc`, teinte `#f2f0f6`, et les
tons de la sphere. Un controle refuse toute couleur hors de cette liste.

Je n'ai pas mis de rose ni de dore « parce que c'est un concours de miss » :
ca aurait donne deux pages qui n'appartiennent a aucune de tes marques.

## Verification

```
python3 tests-concours.py     57 controles sur les fichiers generes
python3 tests-rendu.py        24 controles dans un vrai navigateur
python3 build.py              regenere les pages
python3 prompts.py            regenere PROMPTS-IMAGES.md
python3 shots.py              refait les captures
```

**81 controles, tous verts.** Ceux qui portent le plus :

- les nombres affiches (48 profils, 8 villes, 6 categories, 160-182 cm) sont
  **compares au catalogue**, pas relus dans la page ;
- chaque fiche tient dans la fourchette de **sa** categorie — une moyenne
  correcte cacherait un mannequin defile de 1,62 m ;
- filtrer rend un **sous-ensemble strict** : un controle qui verifierait
  « 48 == 48 » passerait aussi bien avec le filtre supprime ;
- les couleurs et le contraste sont **mesures a l'ecran**, pas lus dans le
  CSS ;
- aucun nom de concours existant n'apparait dans les deux pages ;
- chaque case de consentement est bien `required` ;
- aucune fiche ne porte de nom de famille complet.

`tests-rendu.py` existe a cause d'un bogue que `tests-concours.py` n'a pas
vu : le bouton principal etait charbon sur charbon, libelle invisible. La
regle `.cms a{color:inherit}` porte une classe **et** un element, donc elle
battait `.cms-btn{color:#fff}`. Une regle presente dans la feuille n'est pas
une regle appliquee — d'ou les mesures de contraste dans un vrai navigateur.
