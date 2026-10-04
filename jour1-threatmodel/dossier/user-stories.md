# User stories & exigences - Boutique du Capitaine

## Parcours fonctionnels
1. En tant que visiteur, je parcours le catalogue sans compte.
2. En tant que client, je me connecte et je reste connecte (token) pendant ma session.
3. En tant que client, je consulte mes factures et je telecharge la mienne au format PDF.
4. En tant que client, je pose une question a l'assistant IA, qui peut consulter le catalogue,
   recuperer une page produit par URL, et parfois lire un document interne pour me repondre.
5. En tant qu'admin (capitaine), je declenche un export comptable (CSV) depuis la console.
6. En tant qu'admin, je recupere l'export genere via un lien.

## Exigences non fonctionnelles (extraits)
- Les exports doivent etre disponibles "rapidement" -> traitement asynchrone (file de jobs).
- L'assistant doit etre "utile" -> on lui a donne des outils (fetch_url, read_file, sql_query).
- "On est presse de livrer" -> l'API interne de reporting n'a pas ete mise derriere l'auth,
  elle est consideree comme non exposee.
- Les tokens durent 24h pour "eviter de redemander le login".
- Un seul compte de base de donnees pour simplifier le deploiement.

## Donnees manipulees (assets)
- Donnees personnelles clients (identite, emails, adresses, factures).
- Identifiants et roles.
- Secrets applicatifs (cle JWT, mots de passe DB, cles d'acces au bucket, role IAM cloud).
- Disponibilite de la boutique.
