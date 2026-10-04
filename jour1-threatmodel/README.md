# Jour 1 - TP2 : Threat modeling (HARD MODE)

Atelier en equipes. Pas de conteneur. Mais cette fois, **aucun DFD n'est fourni** : vous le
reconstruisez a partir d'un dossier realiste et imparfait, comme en vrai. Puis vous modelisez les
menaces en profondeur, et une passe adverse viendra challenger votre travail.

## Le dossier fourni (a analyser)
Tout est dans [`dossier/`](dossier/) :
- [`openapi.yaml`](dossier/openapi.yaml) : la spec de l'API de la Boutique (certains endpoints trahissent des choix discutables).
- [`docker-compose.reference.yml`](dossier/docker-compose.reference.yml) : l'architecture cible (services, reseaux, dependances).
- [`user-stories.md`](dossier/user-stories.md) : les parcours fonctionnels + exigences non fonctionnelles.
- [`adr/`](dossier/adr/) : 3 decisions d'architecture (ADR). Chacune contient des choix a challenger.

Rien ne vous dit ou sont les failles : a vous de les deduire.

## La demarche (4 questions de Shostack)
1. Qu'est-ce qu'on construit ? -> **reconstituez le DFD** + limites de confiance.
2. Qu'est-ce qui peut mal tourner ? -> STRIDE par element + **arbres d'attaque** sur les joyaux.
3. Qu'est-ce qu'on fait ? -> contre-mesures priorisees + **risque residuel**.
4. A-t-on bien travaille ? -> **passe adverse** (une autre equipe tente de contourner vos mitigations).

## Livrables (barre relevee)
A produire dans [`livrables/`](livrables/) :
1. [`1-dfd.md`](livrables/1-dfd.md) : DFD reconstruit + limites de confiance.
2. [`2-stride.md`](livrables/2-stride.md) : STRIDE par element du DFD.
3. [`3-attack-trees.md`](livrables/3-attack-trees.md) : arbres d'attaque pour 2 joyaux (PII clients, capacite admin).
4. [`4-abuse-cases.md`](livrables/4-abuse-cases.md) : cas de mesusage (misuse cases).
5. [`5-risk-scoring.md`](livrables/5-risk-scoring.md) : cotation justifiee (DREAD ou vraisemblance x impact).
6. [`6-mitigations-residuel.md`](livrables/6-mitigations-residuel.md) : plan de remediation + risque residuel.
7. [`7-prediction-scellee.md`](livrables/7-prediction-scellee.md) : vos 8 vulns anticipees pour le CTF du Jour 2 (scellees).

## Deux mecaniques qui corsent l'exercice
- **Passe adverse** : voir [`passe-adverse.md`](passe-adverse.md). Vos mitigations seront attaquees.
- **Prediction scellee** : vos 8 vulns anticipees seront confrontees a la realite du CTF demain.
  Bien anticiper = bien modeliser.

## Ce qu'on attend d'un bac+4
- Reconstituer une archi depuis des sources heterogenes (spec, compose, ADR, stories).
- Reperer les **limites de confiance non evidentes** : service IA a outils, appels serveur-a-serveur,
  API "interne" exposee, metadonnees cloud, secrets CI/CD, cle JWT partagee.
- Ne pas cocher STRIDE mecaniquement : raisonner chemins d'attaque et impact metier reel.
- Prioriser et assumer un risque residuel (on ne corrige jamais tout).
