# Canevas DFD (à compléter)

Dessinez (sur papier/tableau ou en ASCII) :

```
[ Externe ]  --(flux)-->  [ Processus ]  --(flux)-->  [ Dépôt de données ]
       \___ LIMITE DE CONFIANCE ___/
```

## Éléments à placer
- [ ] Entités externes (visiteur, client, admin, attaquant)
- [ ] Processus (serveur web, API, assistant IA)
- [ ] Dépôts de données (base users/messages/secrets, fichiers serveur)
- [ ] Flux de données (chaque flèche)
- [ ] **Limites de confiance** (en pointillés)

## Règle d'or
Chaque **flèche qui traverse une limite de confiance** = au moins une menace STRIDE à analyser.
Toute entrée externe est **non fiable** par défaut.
