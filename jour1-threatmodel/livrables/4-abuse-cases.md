# Livrable 4 - Cas de mesusage (a produire)

Ecrivez des "user stories inversees" : ce qu'un acteur malveillant veut faire.

| Acteur malveillant | Objectif | Via quel flux / composant | Precondition |
|--------------------|----------|---------------------------|--------------|
| ex. client authentifie | lire la facture d'un autre | /api/profile/{id}, /download | avoir un compte |
| ex. visiteur | detourner l'assistant | /assistant/chat (prompt injection) | aucune |
| | | | |
