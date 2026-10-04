# Passe adverse (Q4 de Shostack) et prediction scellee

## 1. Passe adverse (revue croisee)
Une fois les livrables 1 a 6 produits, chaque equipe transmet son **plan de mitigations**
(livrable 6) a une autre equipe. L'equipe receveuse joue l'attaquant :

- Pour chaque mitigation proposee, trouver un **contournement** plausible ou une **lacune**
  (ex. "le controle d'ownership est cote gateway mais les services internes se font confiance :
  un SSRF depuis l'assistant rejoue l'appel sans passer par la gateway").
- Rendre une **fiche de contournement** : mitigation visee, faiblesse, scenario de bypass.

L'equipe d'origine amende alors son modele (livrable 6 v2 + risque residuel mis a jour).
C'est la vraie reponse a la question 4 : "a-t-on bien travaille ?".

## 2. Prediction scellee
Chaque equipe remet le livrable 7 (8 vulns anticipees) avant de commencer le Jour 2.
Le lendemain, on confronte a ce qui est reellement exploite dans le CTF.

Baremes indicatifs :
- Passe adverse : qualite et realisme des contournements trouves + qualite de l'amendement.
- Prediction : +1 par vulnerabilite correctement anticipee (type OWASP + localisation plausible).

## 3. Ce qui separe une bonne copie d'une excellente
- Avoir vu les limites de confiance NON evidentes (IA a outils, appels serveur-a-serveur,
  API "interne" exposee, metadonnees cloud, cle JWT partagee, file Redis non authentifiee,
  bucket a noms previsibles, compte DB unique a droits larges).
- Avoir raisonne CHEMINS d'attaque (enchainements) et pas menaces isolees.
- Avoir assume un risque residuel plutot que pretendre tout corriger.
