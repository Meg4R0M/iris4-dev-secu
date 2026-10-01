# Matrice de remédiation à 3 niveaux (livrable - 40 % de la note)

Pour **3 à 5 vulnérabilités** exploitées, décrire la remédiation aux trois niveaux, puis prioriser.
On ne s'arrête pas au correctif de code : on raisonne aussi **architecture** et **organisation**.

## Vulnérabilité 1 : _______________  (OWASP A__)

| Niveau | Contre-mesure |
|--------|---------------|
| **Code** | |
| **Architecture** | |
| **Organisationnel** | |

**Preuve de correction** (l'attaque échoue désormais) :

---

## Vulnérabilité 2 : _______________  (OWASP A__)
| Niveau | Contre-mesure |
|--------|---------------|
| **Code** | |
| **Architecture** | |
| **Organisationnel** | |

---

## Priorisation globale
| # | Vulnérabilité | Probabilité | Impact | Priorité | Effort de correction |
|---|---------------|-------------|--------|----------|----------------------|
| 1 | | | | | |
| 2 | | | | | |

## Exemple de référence (fourni)
| Niveau | IDOR (A01) |
|--------|------------|
| Code | Contrôle d'ownership à chaque accès (`resource.owner_id == current_user.id`) |
| Architecture | Autorisation centralisée (middleware / policy engine), références indirectes |
| Organisationnel | Tests d'autorisation en CI, revue de code obligatoire sur endpoints sensibles |
