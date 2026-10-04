# Jour 1 - TP1 : Recon & cartographie (HARD MODE)

On n'exploite pas encore : on enumere, on correle, on reconstitue. Cette cible ne donne rien
gratuitement. Le flag final ne se trouve nulle part en entier : il s'ASSEMBLE a partir de
**3 fragments** caches a des endroits differents.

## Demarrage
```bash
cd jour1-recon
docker compose up -d --build
```
- Cible : **http://localhost:8001**
- Scoreboard : **http://localhost:8001/scoreboard**
- Arret : `docker compose down -v`

## Perimetre (strict)
- Uniquement `localhost:8001` et ses vhosts locaux. Rien d'autre.
- Enumeration raisonnable : la cible **ralentit volontairement** le fuzzing aveugle (tarpit).
  Une liste de mots ciblee vaut mieux qu'un dictionnaire de 100k entrees lance a l'aveugle.

## Objectif
Reconstituer le flag :
```
HUMANIX{recon_<fragment1>_<fragment2>_<fragment3>}
```
puis le valider sur le scoreboard. Les 3 fragments se trouvent par 3 chaines de decouverte
differentes. A vous de les trouver : on ne donne ni la liste des endpoints, ni la methode.

## Ce qu'on attend d'un bac+4
- Ne pas se contenter du menu : enumerer routes, parametres, methodes, en-tetes, **sous-domaines/vhosts**.
- Penser **artefacts de developpement** laisses en prod (gestion de version, fichiers de build,
  schemas d'API, messages d'erreur).
- Lire le **code cote client** serieusement (pas juste le HTML).
- Correler : une decouverte en debloque une autre. Les fragments sont au bout de **chaines**, pas poses en evidence.

## Indices (volontairement maigres)
- Indice 1 : tout ce qu'un dev versionne par erreur peut etre rejoue. Un fichier supprime n'est
  pas forcement parti.
- Indice 2 : un bundle JS minifie n'est pas la source. Cherchez ce qui permet de la reconstruire.
- Indice 3 : une API moderne expose parfois son propre schema a qui sait demander.
- Indice 4 : certaines portes ne s'ouvrent qu'avec le bon nom d'hote.

## Outils conseilles
`ffuf` / `feroxbuster` (liste ciblee), `git-dumper`, un client GraphQL ou `curl` + introspection,
Burp Suite, `jq`, les DevTools (onglet Sources et Reseau).

## Livrable attendu
`carte-surface-attaque.md` rempli : technologies, endpoints (et **comment** trouves), vhosts,
artefacts exposes, chaines de decouverte menant a chaque fragment, et le flag reconstitue.

## Note pedagogique
Le but n'est pas la chance mais la methode : recon systematique, lecture d'artefacts, correlation.
Si vous etes bloques plus de 20 min sur une chaine, documentez ce que vous avez teste : c'est ca,
le vrai livrable d'un pentester.
