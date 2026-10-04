# Enonces des TP (version etudiant)

Fiches de travaux pratiques en PDF, a utiliser pendant le module. Chaque fiche donne le contexte,
l'objectif, le deroule guide et des indices progressifs. Les solutions ne sont pas publiees.

| TP | Fiche | Stack a lancer |
|----|-------|----------------|
| TP1 | [Recon & cartographie](TP1-recon.pdf) | `jour1-recon/` (port 8001) |
| TP2 | [Threat modeling (STRIDE)](TP2-threat-modeling.pdf) | `jour1-threatmodel/` (atelier papier) |
| TP3 | [Injection SQL & XSS](TP3-injection-xss.pdf) | `jour2-ctf/` (port 8002) |
| TP4 | [Controle d'acces](TP4-controle-acces.pdf) | `jour2-ctf/` (port 8002) |
| TP5 | [Auth, JWT, crypto](TP5-auth-jwt-crypto.pdf) | `jour2-ctf/` (port 8002) |
| TP6 | [Remediation](TP6-remediation.pdf) | `jour2-ctf/` (port 8002) |
| TP7 | [Prompt injection (LLM)](TP7-prompt-injection.pdf) | `jour3-llm/` (port 8003) |
| TP8 | [Investigation d'incident](TP8-incident.pdf) | `jour3-incident/` (logs) |

Chaque stack se lance avec `docker compose up -d --build` depuis son dossier. Les flags
`HUMANIX{...}` se valident sur le scoreboard local (`/scoreboard`) de chaque stack.
