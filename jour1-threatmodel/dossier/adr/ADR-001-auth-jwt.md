# ADR-001 : Authentification par JWT

## Contexte
On veut une auth stateless entre le frontend, la gateway et les services.

## Decision
- JWT signes en **HS256**. La **cle de signature est partagee** entre auth-svc et api-gateway
  (meme variable d'environnement, injectee par le CI/CD).
- Token valide **24h**, **pas de liste de revocation**.
- La gateway lit l'en-tete `alg` du token recu pour choisir comment le verifier.
- Le role (`user`/`admin`) est un claim dans le payload du token.

## Consequences
- Simplicite de deploiement.
- (A vous d'identifier les consequences de securite non listees ici.)
