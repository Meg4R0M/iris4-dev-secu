# Jour 1 - TP2 : Atelier threat modeling (STRIDE)

Atelier **papier** (pas de conteneur). En équipes, vous modélisez les menaces de l'application
fil rouge - *La Boutique du Capitaine* (celle du Jour 2) - **avant** de l'attaquer.

## Déroulé (~1h45)
1. Lire [`architecture.md`](architecture.md) : composants et flux de l'application.
2. Tracer le **DFD** (schéma de flux de données) et marquer les **limites de confiance** →
   canevas : [`canvas-dfd.md`](canvas-dfd.md).
3. Appliquer **STRIDE** sur chaque flux et chaque dépôt de données →
   grille : [`grille-stride.md`](grille-stride.md).
4. **Prioriser** chaque menace (probabilité × impact) →
   grille : [`grille-priorisation.md`](grille-priorisation.md).
5. Proposer **1 contre-mesure** par menace prioritaire (code / archi / orga).
6. Restitution : 5 min par équipe.

## Les 4 questions (Shostack)
1. Qu'est-ce qu'on construit ? (DFD)
2. Qu'est-ce qui peut mal tourner ? (STRIDE)
3. Qu'est-ce qu'on fait ? (contre-mesures)
4. A-t-on bien travaillé ? (revue)

## STRIDE - rappel
| Lettre | Menace | Propriété visée | Contre-mesure type |
|--------|--------|-----------------|--------------------|
| **S** | Spoofing (usurpation) | Authentification | auth forte, MFA |
| **T** | Tampering (altération) | Intégrité | validation, signatures |
| **R** | Repudiation (déni d'action) | Non-répudiation | logs, audit |
| **I** | Information disclosure (fuite) | Confidentialité | chiffrement, contrôle d'accès |
| **D** | Denial of service | Disponibilité | rate-limit, quotas |
| **E** | Elevation of privilege | Autorisation | moindre privilège |
