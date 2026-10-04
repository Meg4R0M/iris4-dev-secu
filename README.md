# IRIS4 Dev, Securite applicative Dev / Data / IA

> CTF pedagogique conteneurise, support de TP du module **Cybersecurite orientee Dev / Data / IA**
> IRIS Mediaschool Montpellier, Humanix Cybersecurity, 2025-2026

De l'attaque a la remediation, une approche **pratico-pratique** : on exploite reellement des
vulnerabilites dans des environnements **isoles et conteneurises**, puis on les corrige.

Chaque stack embarque son propre **scoreboard local** : aucun serveur central ni CTFd a installer,
tout tourne sur le poste de l'etudiant.

---

## Cadre legal & ethique, a lire avant tout

Les techniques offensives de ce depot s'exercent **exclusivement** sur les environnements fournis
ici (conteneurs Docker isoles, tournant sur **votre** poste). **Toute manipulation hors de ce
perimetre est interdite.**

- Aucun test sur des systemes tiers, en production, ou sans autorisation.
- Les atteintes aux systemes de traitement automatise de donnees sont reprimees par les
  **articles 323-1 et suivants du Code penal**.
- La signature de la **charte d'usage responsable** ([`docs/charte-usage-responsable.md`](docs/charte-usage-responsable.md))
  est un prerequis au module.
- **Finalite strictement defensive** : comprendre l'attaque pour mieux proteger.

---

## Prerequis

| Outil | Role |
|-------|------|
| **Docker** + **Docker Compose** | executer les environnements (chaque TP est conteneurise) |
| Navigateur recent | manipuler les applications et le scoreboard |
| **Burp Suite Community** (ou equivalent) | proxy d'interception (rejouer / muter les requetes) |
| Ligne de commande + `git` | lancer les TP, investiguer les logs |

Verifier l'installation :

```bash
docker --version
docker compose version
```

---

## Structure du depot

| Dossier | Jour | TP | Theme |
|---------|------|----|-------|
| [`jour1-recon/`](jour1-recon/) | J1 | TP1 | Recon & cartographie de surface d'attaque |
| [`jour1-threatmodel/`](jour1-threatmodel/) | J1 | TP2 | Threat modeling (STRIDE), atelier papier |
| [`jour2-ctf/`](jour2-ctf/) | J2 | TP3-6 | CTF web : OWASP Top 10 exploite puis corrige |
| [`jour3-llm/`](jour3-llm/) | J3 | TP7 | Prompt injection sur une application d'IA |
| [`jour3-incident/`](jour3-incident/) | J3 | TP8 | Investigation d'incident a partir de logs |
| [`docs/`](docs/) | - | - | Charte, matrice de remediation, ressources |
| [`enonces/`](enonces/) | tous | TP1-8 | Fiches de TP (PDF) a destination des etudiants |

Chaque dossier contient son propre `README.md` avec l'enonce du TP.

---

## Demarrage rapide

Chaque TP se lance independamment depuis son dossier, sans aucune configuration :

```bash
# Exemple, le CTF du Jour 2
cd jour2-ctf
docker compose up -d --build
```

- Application cible : **http://localhost:8002**
- Scoreboard local : **http://localhost:8002/scoreboard**

Pour tout arreter et nettoyer :

```bash
docker compose down -v
```

---

## Les flags et le scoreboard

Les challenges renvoient des flags au format **`HUMANIX{...}`** lorsqu'ils sont resolus.

- Les flags sont **generes aleatoirement au demarrage** de chaque conteneur : ils ne figurent
  **nulle part dans le code** ni dans ce depot, et different d'un poste a l'autre.
- Vous validez vos flags sur le **scoreboard local** embarque (`/scoreboard`) : il verifie le flag
  hors-ligne et suit votre progression (stockee dans votre navigateur). Aucun CTFd requis.

> Le flag seul ne suffit pas. L'evaluation porte a **40 %** sur la **remediation** : pour chaque
> vulnerabilite exploitee, vous produisez une correction aux **trois niveaux** (code, architecture,
> organisation), voir [`docs/matrice-remediation-template.md`](docs/matrice-remediation-template.md).

---

## Evaluation du module

| Epreuve | Modalite | Poids |
|---------|----------|-------|
| Score CTF offensif (scoreboard local) | Individuel | 40 % |
| Livrable de remediation (3-5 vulns, grille 3 niveaux + priorisation) | Individuel | 40 % |
| Restitution de l'escape game Data / IA | Groupe | 20 % |

---

*Support pedagogique, Humanix Cybersecurity. Les corriges ne sont pas publies dans ce depot.*
