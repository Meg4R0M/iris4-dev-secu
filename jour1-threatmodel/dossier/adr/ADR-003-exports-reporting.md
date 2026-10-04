# ADR-003 : Exports comptables & reporting

## Contexte
Les admins ont besoin d'exports CSV du grand livre (ledger).

## Decision
- L'admin declenche un export via la console ; un **job** est pousse dans **Redis** (sans auth).
- Un **worker** consomme le job, lit la base et ecrit le CSV dans le **bucket object-store**.
- Le bucket est joignable depuis l'edge ; les objets sont nommes `export-<id>.csv` avec un
  `<id>` sequentiel.
- L'endpoint `/api/internal/v2/ledger` sert ces donnees ; considere **interne**, il n'a pas d'auth.
- Les instances tournent dans le cloud avec un **role IAM** attache (metadonnees sur
  169.254.169.254).

## Consequences
- Exports rapides et decouples.
- (A vous d'identifier : exposition de l'API interne, previsibilite des noms d'objets, acces au
  bucket, SSRF vers les metadonnees, file de jobs non authentifiee.)
