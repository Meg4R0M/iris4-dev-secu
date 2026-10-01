# Jour 1 - TP1 : Recon & cartographie de surface d'attaque

On n'attaque pas encore : on **observe**. La moitié du travail d'un attaquant, c'est comprendre
la cible avant de la toucher.

## Démarrage
```bash
cd jour1-recon
docker compose up -d --build
```
Cible : **http://localhost:8001** · Arrêt : `docker compose down -v`

## Objectif
Dresser la **carte de surface d'attaque** de l'application, sans l'exploiter.
Remplissez [`carte-surface-attaque.md`](carte-surface-attaque.md).

## Étapes
1. Ouvrez l'application dans le navigateur, proxy d'interception actif (Burp).
2. Inspectez les **en-têtes de réponse** (`Server`, `X-Powered-By`, `X-Debug-Mode`…).
3. Regardez les **cookies** posés : `HttpOnly` ? `Secure` ? `SameSite` ?
4. Consultez `/robots.txt` - que révèle-t-il ?
5. Provoquez une **erreur** (ex. `/product?id=abc`) : que fuite le message ?
6. Énumérez les **endpoints** non listés dans le menu.
7. Produisez la carte et identifiez **3 points d'entrée prioritaires** pour le Jour 2.

## Ce qu'on debriefe ensemble
En-têtes révélateurs → CVE connues · endpoints oubliés = dette de sécurité ·
cookies mal configurés = sessions volables · stack traces = cadeau à l'attaquant.
