# Architecture - La Boutique du Capitaine (fil rouge)

Application web de boutique en ligne (démo pédagogique).

## Composants
- **Navigateur client** (utilisateurs : visiteur, client authentifié, admin/capitaine).
- **Serveur web / API** (Flask) : pages + endpoints `/login`, `/search`, `/guestbook`,
  `/api/profile/<id>`, `/download`, `/api/me` (JWT), `/token`, `/debug`.
- **Base de données** (SQLite) : table `users` (dont mots de passe et rôle), `messages`, `secrets`.
- **Assistant IA** (Jour 3) : service LLM avec un outil `read_file` et un prompt système secret.
- **Système de fichiers serveur** : dossier `/app/files` servi par `/download`.

## Flux de données principaux
1. Client → Serveur : identifiants de connexion (login).
2. Client → Serveur : requêtes de recherche, messages du livre d'or (contenu non fiable).
3. Serveur → Base : requêtes SQL.
4. Client → API : jeton JWT dans l'en-tête Authorization.
5. Serveur → Fichiers : lecture de fichiers via le paramètre `file`.
6. Client → Assistant IA → outil/fichiers internes.

## Acteurs & valeurs (assets)
- Données personnelles des clients (emails, profils).
- Mots de passe / rôles.
- Secrets applicatifs (clé JWT, code promo).
- Disponibilité du service.

## À vous
Tracez le DFD, placez les **limites de confiance** (navigateur ↔ serveur, serveur ↔ base,
serveur ↔ IA), puis déroulez STRIDE.
