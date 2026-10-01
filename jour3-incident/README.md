# Jour 3 - TP8 : Investigation d'incident à partir de logs

Pas de conteneur : vous recevez les **logs** d'un incident réel (simulé) sur *La Boutique du
Capitaine*. Reconstituez l'intrusion.

## Matériel
- [`logs/access.log`](logs/access.log) - journal d'accès HTTP (format type Apache/Nginx).
- [`logs/auth.log`](logs/auth.log) - tentatives d'authentification applicatives.
- [`logs/app.log`](logs/app.log) - journal applicatif (erreurs, requêtes).

## Mission
1. **Chronologie** : quand commence l'anomalie ?
2. **Point d'entrée** : quelle vulnérabilité a été exploitée en premier ?
3. **Kill Chain** : tracez les actions de l'attaquant, étape par étape.
4. **Impact** : quels comptes / quelles données ont été touchés ?
5. **Remédiation** : rédigez la [fiche d'incident](fiche-incident-template.md) + 3 recommandations priorisées.

## Boîte à outils
Les outils du quotidien suffisent :
```bash
grep -i "union" logs/access.log          # injection SQL ?
grep "401\|403\|500" logs/access.log     # erreurs
awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn   # top IP
grep -c "login" logs/auth.log            # brute force ?
```

> Rappel OWASP A09 : sans logs (ou avec des logs qui fuitent), la détection est impossible.
