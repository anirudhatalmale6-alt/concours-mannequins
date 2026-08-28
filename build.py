# -*- coding: utf-8 -*-
"""Genere les deux livrables.

  docs/concours.html     page unique du concours de miss (apercu complet)
  docs/mannequins.html   catalogue mannequins feminin (apercu complet)
  docs/catalogue.json    les fiches, servies au catalogue
  paste/concours.html    LE MEME bloc, sans <html>/<head>, a coller dans un
  paste/mannequins.html  widget HTML (Elementor ou autre) d'un site existant

Aucun chiffre n'est ecrit a la main dans le HTML : le nombre de fiches, le
nombre de villes, les fourchettes de taille sortent tous de donnees.py. Si
le catalogue bouge, on relance et les pages suivent — sinon la page annonce
tot ou tard un nombre que le catalogue ne contient plus.
"""

import html as H
import json
import os

from donnees import (CONCOURS, ETAPES, CRITERES, JURY, PRIX, FAQ, A_TRANCHER,
                     CATEGORIES, mannequins)
from style import CSS

ICI = os.path.dirname(os.path.abspath(__file__))
FONT = ('https://fonts.googleapis.com/css2?'
        'family=Poppins:wght@400;500;600;700&display=swap')

FICHES = mannequins()

# Emplacements d'images. CETTE LISTE EST LA SOURCE UNIQUE : le HTML, le
# LISEZ-MOI et PROMPTS-IMAGES.md en sortent tous. Une liste recopiee a trois
# endroits finit par diverger, et c'est le client qui decouvre le fichier
# manquant.
IMAGES = [
    ('images/concours-scene.jpg', '16/9',
     'La scene de la finale, vue de la salle, lumieres allumees, sans public '
     'reconnaissable.'),
    ('images/concours-coulisses.jpg', '3/4',
     'Coulisses : portants de tenues, miroir de loge, personne au premier plan.'),
    ('images/concours-jury.jpg', '16/9',
     'Une table de jury vide, carnets et micros, salle en arriere-plan floue.'),
    ('images/mannequins-studio.jpg', '16/9',
     'Studio photo vide : fond cyclo, boites a lumiere, trepied. Aucun visage.'),
    ('images/mannequins-book.jpg', '3/4',
     'Un book ouvert sur une table, planches contact, sans photo lisible.'),
]


def e(s):
    return H.escape(str(s), quote=True)


# --------------------------------------------------------------------------
# briques
# --------------------------------------------------------------------------

def rail():
    return '<div class="cms-rail"><i></i><i></i><i></i><i></i></div>'


def brand(nom, tag):
    return ('<div class="cms-brand"><div class="cms-sph"></div>'
            '<b>%s</b><span class="tag">%s</span></div>' % (e(nom), e(tag)))


def figure(src, ratio, legende):
    """Cadre d'image. Tant que le fichier n'est pas depose, on affiche un
    cadre qui NOMME le fichier attendu — deposer le fichier suffit, il n'y a
    aucun HTML a retoucher. Les attributs sont des data- lus par un script,
    jamais un onerror inline : un onerror a guillemets imbriques se casse des
    qu'un editeur reencode le bloc."""
    return (
        '<figure class="cms-fig" data-img="%s" data-ratio="%s">'
        '<div class="ph"><b>Image a deposer</b><span>%s</span></div>'
        '</figure>' % (e(src), e(ratio), e(src)))


SCRIPT_PH = """
/* Remplace chaque cadre par la vraie image des qu'elle existe. On teste le
   chargement AVANT de toucher au DOM : si le fichier manque, le cadre nomme
   reste en place au lieu d'une icone d'image cassee. */
(function(){
 var f=document.querySelectorAll('.cms-fig[data-img]');
 for(var i=0;i<f.length;i++){(function(fig){
  var src=fig.getAttribute('data-img'),im=new Image();
  im.onload=function(){
   var box=fig.querySelector('.ph');if(!box)return;
   im.style.width='100%';im.style.display='block';
   im.style.aspectRatio=fig.getAttribute('data-ratio')||'3/4';
   im.style.objectFit='cover';im.alt='';
   box.parentNode.replaceChild(im,box);
  };
  im.src=src;
 })(f[i]);}
})();
"""


# --------------------------------------------------------------------------
# page 1 : le concours
# --------------------------------------------------------------------------

def page_concours():
    C = CONCOURS
    o = []
    A = o.append

    A('<div class="cms">')

    # Hero
    A('<section class="cms-s"><div class="cms-w">')
    A(brand(C['nom'], C['edition']))
    A(rail())
    A('<h1>%s</h1>' % e(C['accroche']))
    A('<p class="cms-sub">%s</p>' % e(C['sous_accroche']))
    # La date et la salle de la finale, en haut. Elles manquaient : une page
    # de concours qui ne dit pas QUAND ni OU est la finale demande a des
    # candidates de s'engager sur une soiree dont elles ignorent la date.
    # Tant qu'elles ne sont pas fixees, on affiche le trou, on ne le cache pas.
    A('<table class="cms-tab" style="max-width:560px;margin-top:24px">'
      '<tr><th>Finale</th><td>%s</td></tr>'
      '<tr><th>Lieu</th><td>%s, %s</td></tr>'
      '<tr><th>Candidatures</th><td>Gratuites, en ligne, jusqu\'a '
      '[DATE A CONFIRMER]</td></tr></table>'
      % (e(C['date_finale']), e(C['lieu']), e(C['ville'])))
    A('<p style="margin-top:22px">'
      '<a class="cms-btn" href="#candidature">Deposer ma candidature</a> '
      '<a class="cms-btn ghost" href="#etapes">Voir les etapes</a></p>')
    A('<nav class="cms-nav" style="margin-top:34px">'
      '<a href="#etapes">Les etapes</a><a href="#criteres">Qui peut '
      'candidater</a><a href="#prix">Ce que gagnent les finalistes</a>'
      '<a href="#jury">Le jury</a><a href="#candidature">Candidature</a>'
      '<a href="#faq">Questions</a></nav>')
    A('</div></section>')

    # Ce que c'est
    A('<section class="cms-s soft"><div class="cms-w">')
    A('<div class="cms-g c2" style="gap:44px;align-items:center">')
    A('<div>')
    A('<p class="cms-eb">Le principe</p>')
    A('<h2>Un concours ou tout est ecrit avant de commencer</h2>')
    A('<p>Les dates, les criteres, le jury, la dotation : tout est publie '
      'avant l\'ouverture des candidatures, pas annonce au fur et a mesure. '
      'Une candidate doit savoir a quoi elle s\'engage le jour ou elle '
      'remplit le formulaire.</p>')
    A('<p>L\'inscription est gratuite, sans frais de dossier et sans tenue a '
      'acheter. Chaque candidature recoit une reponse, retenue ou non.</p>')
    A('</div>')
    A(figure('images/concours-scene.jpg', '16/9',
             'La scene de la finale'))
    A('</div></div></section>')

    # Etapes
    A('<section class="cms-s" id="etapes"><div class="cms-w">')
    A('<p class="cms-eb">Le parcours</p>')
    A('<h2>Cinq etapes, de la candidature a la finale</h2>')
    A(rail())
    A('<ol class="cms-steps">')
    for _, titre, texte in ETAPES:
        A('<li><div><h3>%s</h3><p>%s</p></div></li>' % (e(titre), e(texte)))
    A('</ol>')
    A('</div></section>')

    # Criteres
    A('<section class="cms-s tint" id="criteres"><div class="cms-w">')
    A('<div class="cms-g c2" style="gap:44px;align-items:start">')
    A('<div>')
    A('<p class="cms-eb">Admissibilite</p>')
    A('<h2>Qui peut candidater</h2>')
    A('<table class="cms-tab">')
    for quoi, texte in CRITERES:
        A('<tr><th>%s</th><td>%s</td></tr>' % (e(quoi), e(texte)))
    A('</table>')
    A('<p class="cms-note">Ces criteres sont ceux du reglement. Tant que le '
      'reglement complet n\'est pas en ligne et telechargeable, cette page '
      'affiche un lien inactif plutot qu\'un lien qui promet un document '
      'inexistant.</p>')
    A('</div>')
    A(figure('images/concours-coulisses.jpg', '3/4', 'Coulisses'))
    A('</div></div></section>')

    # Prix
    A('<section class="cms-s" id="prix"><div class="cms-w">')
    A('<p class="cms-eb">Dotation</p>')
    A('<h2>Ce que gagnent les finalistes</h2>')
    A(rail())
    A('<div class="cms-g c3">')
    for titre, lignes in PRIX:
        A('<div class="cms-card"><h3>%s</h3><ul style="margin:0;'
          'padding-left:18px;font-size:14.6px;color:#4a4753">' % e(titre))
        for l in lignes:
            A('<li>%s</li>' % e(l))
        A('</ul></div>')
    A('</div>')
    A('<p class="cms-note">Le montant de la dotation en numeraire doit etre '
      'fixe et annonce AVANT l\'ouverture des candidatures. Un montant '
      'annonce apres coup se discute ; un montant annonce d\'avance engage '
      'l\'organisateur, et c\'est ce qui rassure les candidates.</p>')
    A('</div></section>')

    # Jury — bande sombre, la seule de la page
    A('<section class="cms-s ink" id="jury"><div class="cms-w">')
    A('<p class="cms-eb">Le jury</p>')
    A('<h2>Nomme avant l\'ouverture des candidatures</h2>')
    A('<p class="cms-sub" style="color:#c9c6d0">Un jury annonce apres la '
      'selection ne rassure personne. Cinq sieges, chacun nomme et publie '
      'ici avec sa fonction.</p>')
    A('<div class="cms-g c3" style="margin-top:26px">')
    for nom, role, note in JURY:
        A('<div class="cms-card"><h3>%s</h3><p style="font-size:13px;'
          'letter-spacing:.05em;text-transform:uppercase;color:#a5a1b0;'
          'margin-bottom:6px">%s</p><p>%s</p></div>'
          % (e(nom), e(role), e(note)))
    A('</div>')
    A('<div style="max-width:620px;margin-top:30px">')
    A(figure('images/concours-jury.jpg', '16/9', 'La table du jury'))
    A('</div>')
    A('</div></section>')

    # Candidature
    A('<section class="cms-s soft" id="candidature"><div class="cms-w">')
    A('<p class="cms-eb">Candidature</p>')
    A('<h2>Deposer sa candidature</h2>')
    A(rail())
    A('<p class="cms-sub">Inscription gratuite. Deux photos recentes '
      'suffisent : une de visage, une en pied, prises au telephone.</p>')
    A('<form class="cms-form" style="margin-top:26px" method="post" '
      'action="#" onsubmit="return false">')
    for lab, nom, typ in [
            ('Prenom', 'prenom', 'text'), ('Nom', 'nom', 'text'),
            ('Date de naissance', 'naissance', 'date'),
            ('Ville de residence', 'ville', 'text'),
            ('Telephone', 'tel', 'tel'),
            ('Taille (cm)', 'taille', 'number')]:
        A('<div><label for="c-%s">%s</label>'
          '<input id="c-%s" name="%s" type="%s" required></div>'
          % (nom, e(lab), nom, nom, typ))
    A('<div class="full"><label for="c-photo">Photos (visage + en pied)'
      '</label><input id="c-photo" name="photos" type="file" accept="image/*" '
      'multiple></div>')
    A('<div class="full"><label for="c-mot">Pourquoi ce concours ?</label>'
      '<textarea id="c-mot" name="motivation" '
      'placeholder="Quelques lignes suffisent."></textarea></div>')

    # Les deux cases a cocher qui manquent presque toujours.
    A('<label class="cms-cons"><input type="checkbox" name="droit_image" '
      'required><span><b>Droit a l\'image.</b> J\'autorise l\'organisateur a '
      'utiliser les photos que je depose <b>pour la seule selection</b>. '
      'Toute autre utilisation — affiche, reseaux sociaux, presse — fera '
      'l\'objet d\'un accord ecrit distinct.</span></label>')
    A('<label class="cms-cons"><input type="checkbox" name="donnees" '
      'required><span><b>Donnees personnelles.</b> Mes coordonnees servent a '
      'traiter ma candidature et a rien d\'autre. Elles sont effacees a la '
      'fin de l\'edition si je ne suis pas retenue. Je peux demander leur '
      'suppression a tout moment.</span></label>')
    A('<div class="full"><button class="cms-btn" type="submit">'
      'Envoyer ma candidature</button></div>')
    A('</form>')
    A('<p class="cms-note"><b>Ce formulaire n\'envoie encore rien.</b> Il '
      'attend deux choses : l\'adresse ou arrivent les candidatures, et '
      'l\'entite juridique organisatrice pour les mentions legales. Un '
      'formulaire branche avant d\'avoir ces deux reponses collecte des '
      'donnees que personne n\'est en mesure de traiter.</p>')
    A('</div></section>')

    # FAQ
    A('<section class="cms-s" id="faq"><div class="cms-w">')
    A('<p class="cms-eb">Questions</p>')
    A('<h2>Ce que les candidates demandent</h2>')
    A(rail())
    A('<div class="cms-faq">')
    for q, a in FAQ:
        A('<details><summary>%s</summary><div class="a">%s</div></details>'
          % (e(q), e(a)))
    A('</div>')
    A('</div></section>')

    A('</div>')
    return '\n'.join(o)


# --------------------------------------------------------------------------
# page 2 : le catalogue mannequins
# --------------------------------------------------------------------------

def page_mannequins():
    villes = sorted({f['ville'] for f in FICHES})
    cats = sorted({c for f in FICHES for c in f['categories']})
    tmin = min(f['taille_cm'] for f in FICHES)
    tmax = max(f['taille_cm'] for f in FICHES)

    o = []
    A = o.append
    A('<div class="cms">')

    A('<section class="cms-s"><div class="cms-w">')
    A(brand('Catalogue', 'Mannequins'))
    A(rail())
    A('<h1>Le catalogue mannequin feminin</h1>')
    # Les nombres sortent du catalogue, jamais de la main.
    A('<div class="cms-g c2" style="gap:44px;align-items:center">')
    A('<div>')
    A('<p class="cms-sub">%d profils, %d villes, %d categories, de %d a '
      '%d cm. Filtrez, puis demandez le book complet des profils qui vous '
      'interessent.</p>' % (len(FICHES), len(villes), len(cats), tmin, tmax))
    A('<p style="margin-top:18px"><a class="cms-btn" href="#cms-grid">'
      'Parcourir le catalogue</a> <a class="cms-btn ghost" '
      'href="#candidature-mannequin">Deposer mon book</a></p>')
    A('</div>')
    A(figure('images/mannequins-studio.jpg', '16/9', 'Studio'))
    A('</div>')
    A('</div></section>')

    A('<section class="cms-s soft"><div class="cms-w">')

    # Barre de filtres
    A('<div class="cms-bar">')
    A('<div class="cms-f"><label for="f-cat">Categorie</label>'
      '<select id="f-cat"><option value="">Toutes</option>%s</select></div>'
      % ''.join('<option>%s</option>' % e(c) for c in cats))
    A('<div class="cms-f"><label for="f-ville">Ville</label>'
      '<select id="f-ville"><option value="">Toutes</option>%s</select></div>'
      % ''.join('<option>%s</option>' % e(v) for v in villes))
    A('<div class="cms-f"><label for="f-taille">Taille mini (cm)</label>'
      '<select id="f-taille"><option value="">Sans minimum</option>%s</select>'
      '</div>' % ''.join('<option value="%d">%d cm et plus</option>' % (t, t)
                         for t in range(160, 182, 2)))
    A('<div class="cms-f"><label for="f-exp">Experience</label>'
      '<select id="f-exp"><option value="">Toutes</option>'
      '<option>Debutante</option><option>Confirmee</option>'
      '<option>Professionnelle</option></select></div>')
    A('<div class="cms-f"><label for="f-lg">Langue</label>'
      '<select id="f-lg"><option value="">Toutes</option><option>FR</option>'
      '<option>EN</option><option>AR</option><option>ES</option>'
      '<option>IT</option></select></div>')
    A('<div class="cms-f"><label for="f-dispo">Disponibilite</label>'
      '<select id="f-dispo"><option value="">Tous</option>'
      '<option value="1">Disponibles</option></select></div>')
    A('<div class="cms-count" id="cms-count"></div>')
    A('</div>')

    A('<div class="cms-grid" id="cms-grid"></div>')
    A('<div class="cms-vide" id="cms-vide" style="display:none">'
      'Aucun profil ne correspond a ces filtres. Elargissez un critere.</div>')

    A('<p class="cms-note" style="margin-top:24px"><b>Fiches de '
      'demonstration.</b> Les %d profils ci-dessus sont inventes et servent a '
      'montrer la mise en page et les filtres. Ils sont a remplacer par les '
      'mannequins sous contrat, une ligne par fiche dans le fichier de '
      'donnees.</p>' % len(FICHES))
    A('</div></section>')

    # Pourquoi la fiche publique est courte — bande sombre, la seule.
    A('<section class="cms-s ink"><div class="cms-w">')
    A('<p class="cms-eb">Ce que la fiche publique affiche, et ce qu\'elle '
      'garde</p>')
    A('<h2>Le book complet ne s\'affiche pas en acces libre</h2>')
    A('<div class="cms-g c3" style="margin-top:24px">')
    A('<div class="cms-card"><h3>En public</h3><p>Prenom et initiale, ville, '
      'taille, categories, langues, disponibilite. De quoi faire une '
      'presalection serieuse.</p></div>')
    A('<div class="cms-card"><h3>Sur demande</h3><p>Nom complet, mensurations '
      'completes, book integral, video de presentation, tarifs. Transmis au '
      'client identifie, pour un projet nomme.</p></div>')
    A('<div class="cms-card"><h3>Pourquoi</h3><p>Une page publique qui donne '
      'nom complet, ville, mensurations et disponibilite de jeunes femmes '
      'est un annuaire pour n\'importe qui. Ce n\'est pas de la pudeur, '
      'c\'est de la securite — et les agences serieuses fonctionnent toutes '
      'comme ca.</p></div>')
    A('</div>')
    A('</div></section>')

    # Deposer sa candidature au catalogue
    A('<section class="cms-s"><div class="cms-w">')
    A('<div class="cms-g c2" style="gap:44px;align-items:center">')
    A('<div>')
    A('<p class="cms-eb">Rejoindre le catalogue</p>')
    A('<h2>Le catalogue grandit par candidature, pas par recopiage</h2>')
    A(rail())
    A('<p>Chaque fiche appartient a une personne qui a signe. C\'est la '
      'seule facon de batir un catalogue qui tient : une photo reprise '
      'ailleurs, c\'est le book d\'une autre agence et le droit a l\'image '
      'de quelqu\'un qui n\'a rien accepte.</p>')
    A('<p><a class="cms-btn" href="#candidature-mannequin">Deposer mon '
      'book</a></p>')
    A('</div>')
    A(figure('images/mannequins-book.jpg', '3/4', 'Un book ouvert'))
    A('</div></div></section>')

    A('<section class="cms-s tint" id="candidature-mannequin">'
      '<div class="cms-w">')
    A('<p class="cms-eb">Candidature mannequin</p>')
    A('<h2>Deposer son book</h2>')
    A(rail())
    A('<form class="cms-form" style="margin-top:22px" method="post" '
      'action="#" onsubmit="return false">')
    for lab, nom, typ in [('Prenom', 'prenom', 'text'), ('Nom', 'nom', 'text'),
                          ('Ville', 'ville', 'text'),
                          ('Taille (cm)', 'taille', 'number'),
                          ('Telephone', 'tel', 'tel'),
                          ('Date de naissance', 'naissance', 'date')]:
        A('<div><label for="m-%s">%s</label>'
          '<input id="m-%s" name="%s" type="%s" required></div>'
          % (nom, e(lab), nom, nom, typ))
    A('<div class="full"><label for="m-cat">Categories visees</label>'
      '<select id="m-cat" name="categories" multiple size="4">%s</select>'
      '</div>' % ''.join('<option>%s</option>' % e(c) for c in sorted(CATEGORIES)))
    A('<div class="full"><label for="m-book">Photos (visage, en pied, profil)'
      '</label><input id="m-book" name="book" type="file" accept="image/*" '
      'multiple></div>')
    A('<label class="cms-cons"><input type="checkbox" name="majeure" required>'
      '<span><b>J\'ai 18 ans ou plus.</b> Les candidatures de mineures '
      'demandent l\'accord ecrit des deux parents et un cadre distinct ; '
      'elles ne passent pas par ce formulaire.</span></label>')
    A('<label class="cms-cons"><input type="checkbox" name="droit_image" '
      'required><span><b>Droit a l\'image.</b> J\'autorise la publication de '
      'ma fiche <b>prenom, initiale et ville uniquement</b>. Mon nom complet '
      'et mon book ne sont transmis qu\'a un client identifie, pour un projet '
      'nomme, et je peux retirer ma fiche a tout moment.</span></label>')
    A('<div class="full"><button class="cms-btn" type="submit">Envoyer mon '
      'book</button></div>')
    A('</form>')
    A('<p class="cms-note"><b>Ce formulaire n\'envoie encore rien</b> — il '
      'attend l\'adresse de reception et l\'entite juridique, comme celui du '
      'concours.</p>')
    A('</div></section>')

    A('</div>')
    return '\n'.join(o)


SCRIPT_CAT = """
/* Le catalogue lit ses fiches dans catalogue.json : le HTML ne contient
   aucune fiche en dur. Ajouter un mannequin = une ligne de donnees, pas une
   ligne de page. */
(function(){
 var grid=document.getElementById('cms-grid');
 if(!grid)return;
 var vide=document.getElementById('cms-vide'),cnt=document.getElementById('cms-count');
 var F=[];
 var sel={cat:'f-cat',ville:'f-ville',taille:'f-taille',exp:'f-exp',
          lg:'f-lg',dispo:'f-dispo'},el={};
 for(var k in sel)el[k]=document.getElementById(sel[k]);

 function esc(s){return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

 function carte(m){
  return '<article class="cms-mn">'
   +'<figure class="cms-fig" data-img="'+esc(m.photo)+'" data-ratio="3/4">'
   +'<div class="ph"><b>Photo a deposer</b><span>'+esc(m.photo)+'</span></div>'
   +'</figure><div class="bd">'
   +'<div class="nm"><b>'+esc(m.prenom)+' '+esc(m.initiale)+'</b>'
   +'<span class="dispo'+(m.disponible?'':' non')+'">'
   +(m.disponible?'Disponible':'En mission')+'</span></div>'
   +'<div class="loc">'+esc(m.ville)+' &middot; '+esc(m.province)
   +' &middot; '+esc(m.id)+'</div>'
   +'<dl><dt>Taille</dt><dd>'+esc(m.taille_cm)+' cm</dd>'
   +'<dt>Confection</dt><dd>'+esc(m.confection)+'</dd>'
   +'<dt>Cheveux</dt><dd>'+esc(m.cheveux)+'</dd>'
   +'<dt>Yeux</dt><dd>'+esc(m.yeux)+'</dd>'
   +'<dt>Langues</dt><dd>'+m.langues.map(esc).join(', ')+'</dd>'
   +'<dt>Profil</dt><dd>'+esc(m.experience)+'</dd></dl>'
   +'<div class="tags">'+m.categories.map(function(c){
     return '<span>'+esc(c)+'</span>';}).join('')+'</div>'
   +'</div></article>';
 }

 function garde(m){
  if(el.cat.value && m.categories.indexOf(el.cat.value)<0)return false;
  if(el.ville.value && m.ville!==el.ville.value)return false;
  if(el.taille.value && m.taille_cm<parseInt(el.taille.value,10))return false;
  if(el.exp.value && m.experience!==el.exp.value)return false;
  if(el.lg.value && m.langues.indexOf(el.lg.value)<0)return false;
  if(el.dispo.value==='1' && !m.disponible)return false;
  return true;
 }

 function rendre(){
  var v=F.filter(garde);
  grid.innerHTML=v.map(carte).join('');
  vide.style.display=v.length?'none':'block';
  /* On annonce le sous-ensemble ET le total : « 12 profils » tout court
     laisse croire que le catalogue en compte 12. */
  cnt.innerHTML='<b>'+v.length+'</b> profil'+(v.length>1?'s':'')
   +' sur '+F.length;
  if(window.cmsImages)window.cmsImages();
 }

 for(var k2 in el)el[k2].addEventListener('change',rendre);

 var x=new XMLHttpRequest();
 x.open('GET','catalogue.json',true);
 x.onload=function(){
  if(x.status<200||x.status>=300){
   /* Le catalogue n'a pas ete lu : on le DIT. Une grille vide qui se tait
      ressemble a un catalogue vide, et c'est un mensonge different. */
   vide.textContent='Le catalogue n\\'a pas pu etre charge (HTTP '
    +x.status+'). Les fiches sont dans catalogue.json, a cote de cette page.';
   vide.style.display='block';cnt.textContent='';return;
  }
  F=JSON.parse(x.responseText);rendre();
 };
 x.onerror=function(){
  vide.textContent='Le catalogue n\\'a pas pu etre charge. Verifiez que '
   +'catalogue.json est bien depose a cote de cette page.';
  vide.style.display='block';
 };
 x.send();
})();
"""

# Le remplacement d'images doit pouvoir etre rappele apres chaque rendu de
# la grille : les cartes sont creees APRES le premier passage.
SCRIPT_PH_FN = SCRIPT_PH.replace('(function(){', 'window.cmsImages=function(){') \
                        .replace('})();', '};window.cmsImages();')


def enveloppe(titre, corps, scripts):
    return (
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>%s</title>\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="%s">\n'
        '<style>%s</style>\n%s\n<script>%s</script>\n'
        % (H.escape(titre), FONT, CSS, corps, scripts))


def bloc(corps, scripts):
    """Bloc a coller : pas de <html>, pas de <head>, la police et le style
    voyagent avec le bloc. Colle dans un widget HTML, il s'affiche pareil."""
    return ('<link rel="stylesheet" href="%s">\n<style>%s</style>\n%s\n'
            '<script>%s</script>\n' % (FONT, CSS, corps, scripts))


def main():
    # Les pages sont ecrites A LA RACINE, pas dans docs/ : c'est de la que
    # GitHub Pages les sert, et une meme page presente a deux endroits finit
    # par diverger — celle qu'on regarde n'est plus celle qu'on modifie.
    docs = ICI
    paste = os.path.join(ICI, 'paste')
    os.makedirs(paste, exist_ok=True)

    c, m = page_concours(), page_mannequins()

    ecrits = []
    for chemin, contenu in [
        (os.path.join(docs, 'concours.html'),
         enveloppe('%s — %s' % (CONCOURS['nom'], CONCOURS['edition']),
                   c, SCRIPT_PH)),
        (os.path.join(docs, 'mannequins.html'),
         enveloppe('Catalogue mannequins', m, SCRIPT_PH_FN + SCRIPT_CAT)),
        (os.path.join(paste, 'concours.html'), bloc(c, SCRIPT_PH)),
        (os.path.join(paste, 'mannequins.html'),
         bloc(m, SCRIPT_PH_FN + SCRIPT_CAT)),
        (os.path.join(docs, 'catalogue.json'),
         json.dumps(FICHES, ensure_ascii=False, indent=1)),
    ]:
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(contenu)
        ecrits.append((chemin, len(contenu.encode('utf-8'))))

    # index d'apercu
    idx = ('<meta charset="utf-8"><title>JNCORP — apercus</title>'
           '<style>body{font:16px/1.6 system-ui;max-width:640px;margin:60px '
           'auto;padding:0 20px}a{display:block;padding:14px 0;'
           'border-bottom:1px solid #eee;color:#1b1922}</style>'
           '<h1>Apercus</h1>'
           '<a href="concours.html">Concours de miss — page unique</a>'
           '<a href="mannequins.html">Catalogue mannequin feminin '
           '(%d fiches)</a>' % len(FICHES))
    p = os.path.join(docs, 'index.html')
    open(p, 'w', encoding='utf-8').write(idx)
    ecrits.append((p, len(idx.encode('utf-8'))))

    for chemin, n in ecrits:
        print('%-58s %7d o' % (os.path.relpath(chemin, ICI), n))
    print('\n%d fiches, %d villes, %d categories'
          % (len(FICHES), len({f['ville'] for f in FICHES}),
             len({c for f in FICHES for c in f['categories']})))


if __name__ == '__main__':
    main()
