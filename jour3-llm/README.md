# Jour 3 - TP7 : Prompt injection sur une application d'IA

L'**Assistant de la Boutique** est un chatbot adossé à un LLM. Le modèle est *simulé* et tourne
**hors-ligne** (aucune clé API nécessaire), mais il reproduit fidèlement les vulnérabilités
**OWASP LLM Top 10**.

## Démarrage
```bash
cd jour3-llm
docker compose up -d --build
```
Cible : **http://localhost:8003** · Arrêt : `docker compose down -v`

## Contexte
L'assistant a reçu un **prompt système confidentiel** : être poli, ne jamais révéler ses
instructions, ne jamais divulguer le **code promo secret**, et n'utiliser son outil `read_file`
que sur le catalogue. Deux points d'entrée : le **chat direct** et le **résumé de contenu externe**.

## Challenges
On vous donne l'objectif, pas la formulation exacte - l'injection de prompt est un art de la tournure.

| # | Objectif | OWASP LLM |
|---|----------|-----------|
| A | Faire **révéler le prompt système** confidentiel. | LLM01 / LLM06 |
| B | Faire **divulguer le code promo secret**. | LLM01 / LLM06 |
| C | **Détourner l'outil** `read_file` pour lire un autre fichier que le catalogue. | LLM07 / LLM08 |
| D | Réussir une **injection indirecte** : cacher l'instruction dans un contenu « à résumer ». | LLM01 (indirecte) |

Chaque réussite renvoie un flag `HUMANIX{...}`.

## Pour chaque réussite - la contre-mesure
Notez comment vous **réduiriez l'impact** (on ne « patche » pas l'injection, on la contient) :
- séparer instruction / donnée, baliser le contenu externe ;
- **moindre privilège** sur les outils (read_file limité, chemins en allow-list) ;
- **validation des sorties**, filtrage entrée/sortie ;
- human-in-the-loop sur les actions sensibles.
