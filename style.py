# -*- coding: utf-8 -*-
"""Feuille de style des deux pages.

AUCUNE COULEUR INVENTEE. Tout sort de la palette deja en ligne sur
influus.com/bulk-order/ et du degrade de la sphere du logo : charbon #1b1922,
gris #8b8698, blanc casse #faf9fc, teinte #f2f0f6, et les tons de la sphere
#f3f1f5 -> #c9c6d0 -> #6f6b7a -> #2b2833. Poser un rose ou un dore « parce
que c'est un concours de miss » aurait donne deux pages qui n'appartiennent
a aucune de ses marques.

Prefixe .cms sur toute la feuille : ces blocs se collent dans un widget HTML
d'un site WordPress existant, et une regle nue comme h1{} du theme hote bat
n'importe quelle regle heritee. Tout est ecrit en descendant de .cms.
"""

CSS = """
.cms{--ink:#1c1a24;--mut:#8b8698;--line:#ececf1;--soft:#faf9fc;--tint:#f2f0f6;
 --acc:#1b1922;--deep:#2b2833;--sph1:#f3f1f5;--sph2:#c9c6d0;--sph3:#6f6b7a;
 font-family:Poppins,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
 color:var(--ink);line-height:1.62;-webkit-font-smoothing:antialiased}
.cms *,.cms *::before,.cms *::after{box-sizing:border-box}
.cms img{max-width:100%;height:auto;display:block}
.cms a{color:inherit}

/* Bandes. Une seule bande sombre par page : au-dela, le charbon cesse
   d'etre un accent et devient le fond. */
.cms-s{padding:74px 0;background:#fff}
.cms-s.soft{background:var(--soft)}
.cms-s.tint{background:var(--tint);border-block:1px solid #e6e3ee}
.cms-s.ink{background:var(--acc);color:#fff}
.cms-s.ink h2,.cms-s.ink h3{color:#fff}
.cms-s.ink p,.cms-s.ink li,.cms-s.ink .cms-sub{color:#c9c6d0}
.cms-s.ink .cms-eb{color:#a5a1b0}
.cms-w{max-width:1120px;margin:0 auto;padding:0 22px}

.cms-eb{font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;
 color:var(--sph3);font-weight:600;margin:0 0 10px}
.cms h1,.cms h2,.cms h3{margin:0 0 14px;font-weight:600;letter-spacing:-.015em;
 color:var(--ink);line-height:1.2}
.cms h1{font-size:44px}
.cms h2{font-size:31px}
.cms h3{font-size:17px;margin-bottom:8px}
.cms p{margin:0 0 14px}
.cms-sub{font-size:18px;color:#4a4753;max-width:64ch}

/* Le filet a quatre segments : les quatre tons de la sphere, dans l'ordre.
   Le premier ton de la sphere (#f3f1f5) est invisible sur blanc — on part
   donc du deuxieme cran, sinon le filet parait casse a gauche. */
.cms-rail{display:flex;gap:0;height:3px;width:132px;margin:0 0 26px;
 border-radius:2px;overflow:hidden}
.cms-rail i{flex:1}
.cms-rail i:nth-child(1){background:#dcd9e4}
.cms-rail i:nth-child(2){background:var(--sph2)}
.cms-rail i:nth-child(3){background:var(--sph3)}
.cms-rail i:nth-child(4){background:var(--deep)}

/* Sphere du logo, en CSS : nette a toutes les tailles, contrairement au GIF. */
.cms-sph{width:46px;height:46px;border-radius:50%;flex:0 0 46px;
 background:radial-gradient(circle at 34% 30%,var(--sph1) 0%,var(--sph2) 34%,
 var(--sph3) 72%,var(--deep) 100%);
 box-shadow:inset -5px -7px 14px rgba(0,0,0,.28),0 4px 12px rgba(27,25,34,.18)}
.cms-brand{display:flex;align-items:center;gap:13px;margin-bottom:26px}
.cms-brand b{font-size:23px;font-weight:600;letter-spacing:-.02em}
.cms-brand .tag{font-size:10px;letter-spacing:.15em;text-transform:uppercase;
 background:var(--acc);color:#fff;padding:4px 9px;border-radius:3px;
 font-weight:600}
.cms-s.ink .cms-brand .tag{background:#fff;color:var(--acc)}

/* Le bouton doit etre ecrit « a.cms-btn » et pas « .cms-btn » : la regle
   generique .cms a{color:inherit} porte une classe ET un element, donc elle
   bat une simple classe. Ecrit .cms-btn seul, le libelle blanc retombait sur
   l'encre heritee — bouton charbon, texte charbon, libelle invisible. */
.cms a.cms-btn,.cms button.cms-btn{display:inline-block;background:var(--acc);
 color:#fff;text-decoration:none;font-weight:600;font-size:15px;
 padding:14px 26px;border-radius:6px;border:1px solid var(--acc);
 cursor:pointer;font-family:inherit;line-height:1.4}
.cms a.cms-btn.ghost,.cms button.cms-btn.ghost{background:transparent;
 color:var(--ink);border-color:#d8d5e0}
.cms-s.ink a.cms-btn,.cms-s.ink button.cms-btn{background:#fff;
 color:var(--acc);border-color:#fff}
.cms-s.ink a.cms-btn.ghost,.cms-s.ink button.cms-btn.ghost{
 background:transparent;color:#fff;border-color:rgba(255,255,255,.4)}

/* Grilles */
.cms-g{display:grid;gap:18px}
.cms-g.c2{grid-template-columns:repeat(2,1fr)}
.cms-g.c3{grid-template-columns:repeat(3,1fr)}
.cms-g.c4{grid-template-columns:repeat(4,1fr)}
.cms-card{background:#fff;border:1px solid var(--line);border-radius:10px;
 padding:22px}
.cms-s.soft .cms-card,.cms-s.tint .cms-card{background:#fff}
.cms-s.ink .cms-card{background:#241f2d;border-color:rgba(255,255,255,.14)}
.cms-card p{font-size:14.8px;color:#4a4753;margin:0}
.cms-s.ink .cms-card p{color:#d6d3de}

/* Etapes numerotees */
.cms-steps{list-style:none;margin:0;padding:0;counter-reset:e}
.cms-steps li{counter-increment:e;display:grid;grid-template-columns:44px 1fr;
 gap:18px;padding:20px 0;border-top:1px solid var(--line)}
.cms-steps li:first-child{border-top:0}
.cms-steps li::before{content:counter(e,decimal-leading-zero);
 font-size:14px;font-weight:600;color:var(--sph3);padding-top:2px}
.cms-steps p{font-size:14.6px;color:#4a4753;margin:0}

/* Tableau de criteres */
.cms-tab{width:100%;border-collapse:collapse;font-size:14.8px}
.cms-tab th,.cms-tab td{text-align:left;padding:13px 14px;
 border-bottom:1px solid var(--line);vertical-align:top}
.cms-tab th{width:180px;font-weight:600;color:var(--ink)}
.cms-tab td{color:#4a4753}

/* Emplacements d'images : le cadre a le ratio final, pose des maintenant.
   Sans lui, la page saute de 300 px le jour ou les photos arrivent. */
.cms-fig{margin:0;border-radius:10px;overflow:hidden;border:1px solid var(--line)}
.cms-fig .ph{aspect-ratio:3/4;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;padding:18px;
 background:radial-gradient(120% 120% at 30% 20%,#f6f5f9 0%,#e9e7ef 55%,
 #dcd9e4 100%)}
.cms-fig .ph b{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
 color:var(--sph3);margin-bottom:6px}
.cms-fig .ph span{font-size:12.5px;color:var(--mut);line-height:1.5;
 word-break:break-all}
.cms-fig figcaption{font-size:12.5px;color:var(--mut);padding:10px 12px;
 background:var(--soft)}

/* Catalogue mannequins */
.cms-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;
 padding:18px;background:#fff;border:1px solid var(--line);border-radius:10px;
 margin-bottom:20px;position:sticky;top:0;z-index:5}
.cms-f{display:flex;flex-direction:column;gap:5px}
.cms-f label{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
 color:var(--sph3);font-weight:600}
.cms-f select,.cms-f input{font:inherit;font-size:14px;padding:9px 11px;
 border:1px solid #d8d5e0;border-radius:6px;background:#fff;color:var(--ink);
 min-width:132px}
.cms-count{margin-left:auto;font-size:14px;color:var(--mut);padding-bottom:9px}
.cms-count b{color:var(--ink)}

.cms-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.cms-mn{border:1px solid var(--line);border-radius:10px;overflow:hidden;
 background:#fff}
.cms-mn .cms-fig{border:0;border-radius:0}
.cms-mn .bd{padding:14px 15px 16px}
.cms-mn .nm{display:flex;align-items:baseline;justify-content:space-between;
 gap:8px;margin-bottom:2px}
.cms-mn .nm b{font-size:16px;font-weight:600}
.cms-mn .nm i{font-style:normal;font-size:11.5px;color:var(--mut)}
.cms-mn .loc{font-size:13px;color:var(--mut);margin-bottom:10px}
.cms-mn dl{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;margin:0;
 font-size:13px}
.cms-mn dt{color:var(--mut)}
.cms-mn dd{margin:0;color:#4a4753}
.cms-mn .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.cms-mn .tags span{font-size:11px;letter-spacing:.04em;background:var(--tint);
 color:#4a4753;padding:4px 9px;border-radius:20px}
.cms-mn .dispo{font-size:11.5px;font-weight:600;padding:3px 9px;
 border-radius:20px;background:#eaf6ee;color:#1f7a45}
.cms-mn .dispo.non{background:#f3f1f5;color:var(--mut)}
.cms-vide{padding:44px 20px;text-align:center;color:var(--mut);
 border:1px dashed #d8d5e0;border-radius:10px;font-size:15px}

/* Formulaire de candidature */
.cms-form{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.cms-form .full{grid-column:1/-1}
.cms-form label{display:block;font-size:12px;letter-spacing:.1em;
 text-transform:uppercase;color:var(--sph3);font-weight:600;margin-bottom:6px}
.cms-form input,.cms-form select,.cms-form textarea{width:100%;font:inherit;
 font-size:15px;padding:12px 13px;border:1px solid #d8d5e0;border-radius:6px;
 background:#fff}
.cms-form textarea{min-height:112px;resize:vertical}
.cms-cons{grid-column:1/-1;display:flex;gap:11px;align-items:flex-start;
 background:var(--soft);border:1px solid var(--line);border-radius:8px;
 padding:15px}
.cms-cons input{width:17px;height:17px;margin-top:3px;flex:0 0 17px}
.cms-cons span{font-size:13.6px;color:#4a4753;line-height:1.55}

.cms-note{font-size:13.4px;color:var(--mut);border-left:2px solid var(--sph2);
 padding-left:14px;margin-top:18px}
.cms-s.ink .cms-note{border-left-color:var(--sph3);color:#a5a1b0}

.cms-faq{border-top:1px solid var(--line)}
.cms-faq details{border-bottom:1px solid var(--line)}
.cms-faq summary{cursor:pointer;padding:17px 0;font-weight:600;font-size:16px;
 list-style:none}
.cms-faq summary::-webkit-details-marker{display:none}
.cms-faq summary::after{content:"+";float:right;color:var(--mut);
 font-weight:400;font-size:20px;line-height:1}
.cms-faq details[open] summary::after{content:"\\2212"}
.cms-faq .a{padding:0 40px 18px 0;font-size:15px;color:#4a4753}

.cms-nav{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:14px;
 padding:16px 0;border-top:1px solid var(--line);
 border-bottom:1px solid var(--line);margin-bottom:0}
.cms-nav a{color:#4a4753;text-decoration:none}
.cms-nav a:hover{color:var(--ink);text-decoration:underline}

@media (max-width:960px){
 .cms-grid{grid-template-columns:repeat(3,1fr)}
 .cms-g.c4{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:760px){
 .cms h1{font-size:32px}
 .cms h2{font-size:25px}
 .cms-s{padding:52px 0}
 .cms-g.c2,.cms-g.c3,.cms-g.c4{grid-template-columns:1fr}
 .cms-grid{grid-template-columns:repeat(2,1fr)}
 .cms-form{grid-template-columns:1fr}
 .cms-bar{position:static}
 .cms-tab th{width:auto;display:block;padding-bottom:2px;border-bottom:0}
 .cms-tab td{display:block;padding-top:0}
}
@media (max-width:460px){
 .cms-grid{grid-template-columns:1fr}
}
"""
