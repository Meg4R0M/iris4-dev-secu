# ADR-002 : Assistant IA avec outils

## Contexte
On veut un assistant capable de repondre precisement aux clients.

## Decision
- Le service `llm-assistant` recoit les messages clients et dispose de 3 outils :
  - `fetch_url(url)` : recupere une page (ex. fiche produit) pour enrichir sa reponse.
  - `read_file(path)` : lit un document interne (FAQ, catalogue).
  - `sql_query(q)` : interroge la base pour des infos produit/stock.
- Les reponses de l'assistant sont **affichees telles quelles** dans l'interface de chat.
- Le service est joignable depuis le reseau `edge` et le reseau `internal`.

## Consequences
- Reponses riches.
- (A vous d'identifier les risques : que peut faire un client malveillant via le prompt ?
  Que peut faire chaque outil s'il est detourne ?)
