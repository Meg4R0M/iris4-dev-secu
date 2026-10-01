# Jour 2 - CTF « La Boutique du Capitaine » (TP3 → TP6)

Application web **délibérément vulnérable**, conteneurisée. Vous allez l'**exploiter** (TP3-5)
puis la **corriger** (TP6).

## Démarrage

```bash
cd jour2-ctf
docker compose up -d --build
```

- Application cible : **http://localhost:8002**
- Scoreboard local : **http://localhost:8002/scoreboard** (validez vos flags ici)

Arrêt / nettoyage :

```bash
docker compose down -v
```

## Outils conseillés

- **Burp Suite Community** en proxy : interception, onglet *Repeater* pour rejouer/muter les requêtes.
- La ligne de commande (`curl`) et les outils du navigateur (DevTools).
- `jwt.io` pour décoder/forger un JWT, `hashcat`/`john` pour un hash.

## Les challenges

Chaque challenge renvoie un flag **`HUMANIX{...}`**. On vous donne l'objectif, **pas la méthode** :
c'est tout l'exercice. Repérez d'abord la **surface d'attaque** (toutes les routes ne sont pas dans le menu).

### TP3 - Injection & XSS (OWASP A03)

| # | Challenge | Indice d'objectif |
|---|-----------|-------------------|
| 06 | **La serrure en sucre** | Connectez-vous **sans** connaître le mot de passe d'un compte. |
| 13 | **La carte derrière la carte** | La recherche d'équipage en dit plus qu'elle ne le croit. Faites-lui cracher la table des secrets. |
| 05 | **Le perroquet bavard** | L'accueil matelot vous répète. Faites-lui exécuter **votre** code. |
| 20 | **Le message gravé** | Le capitaine relit son livre d'or. Faites-lui livrer son propre cookie. |

### TP4 - Contrôle d'accès (OWASP A01)

| # | Challenge | Indice d'objectif |
|---|-----------|-------------------|
| 01 | **Le profil du capitaine** | L'API expose les profils. Accédez à celui qui ne vous appartient pas. |
| 11 | **La cale aux trésors** | Le téléchargement de brochure n'aime pas rester dans son dossier. |
| 04 | **La trappe oubliée** | Une porte de service a été laissée ouverte en production. |

### TP5 - Authentification & intégrité (OWASP A07 / A02 / A08)

| # | Challenge | Indice d'objectif |
|---|-----------|-------------------|
| 03 | **La porte du capitaine** | Certains comptes gardent les identifiants d'usine. |
| 08 | **Le sceau du capitaine** | L'API `/api/me` lit votre JWT. Devenez admin sans en connaître la clé. |
| 07 | **Le message en bouteille** | Le « jeton chiffré » du capitaine (`/token`) n'est peut-être pas si chiffré. |

> Challenge bonus **12 - Le coffre mal fermé** : un compte a un mot de passe très faible et le login
> n'a **aucune limite de tentatives**. À vous de jouer (sans DoS : restez raisonnable).

### TP6 - Bascule défensive (remédiation)

Le **code source** de l'application est fourni dans [`app/`](app/). Choisissez **3 vulnérabilités**
exploitées aujourd'hui et écrivez leur correction :

1. Modifiez le code de `app/app.py`.
2. Relancez (`docker compose up -d --build`) et **re-tentez l'attaque** : elle doit échouer.
3. Remplissez la [matrice de remédiation à 3 niveaux](../docs/matrice-remediation-template.md)
   (code / architecture / organisation) pour chaque vulnérabilité corrigée.

C'est **ce livrable** qui compte pour 40 % de la note - pas seulement le flag.

## Comptes de départ

L'application contient plusieurs comptes d'équipage. Lesquels ? Une partie du TP3/TP4 consiste
justement à les découvrir. (Aucun identifiant n'est donné ici volontairement.)

## Flags & scoreboard

Les flags ne sont **pas** dans le code : chaque conteneur les **genere aleatoirement au demarrage**
(rien en clair, rien a pousser). Vous les capturez en resolvant les challenges, puis vous les
validez sur le **scoreboard local** embarque : http://localhost:8002/scoreboard. La progression est
suivie dans votre navigateur. Aucun CTFd ni serveur central n'est necessaire.
