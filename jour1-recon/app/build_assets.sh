#!/usr/bin/env bash
# Genere, AU BUILD de l'image, les artefacts de reconnaissance avec des fragments
# ALEATOIRES (donc differents sur chaque poste qui build). Rien n'est en clair dans
# le depot : tout nait ici.
set -euo pipefail

rnd() { head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n' | cut -c1-10; }

F_GIT=$(rnd)       # fragment cache dans l'historique git
F_GQL=$(rnd)       # fragment expose via GraphQL
F_JS=$(rnd)        # fragment cache dans la source map JS
INTERNAL="/api/internal/v2/ledger"   # chemin interne revele par le .env supprime
APIKEY="sk_live_$(rnd)$(rnd)"        # fausse cle (leurre + hygiene VCS)

mkdir -p /app/secrets /app/static
cat > /app/secrets/fragments.json <<JSON
{"git":"$F_GIT","graphql":"$F_GQL","js":"$F_JS","internal":"$INTERNAL"}
JSON

# ---------------------------------------------------------------------------
# 1) Fuite .git : un depot avec un .env supprime... mais toujours dans l'historique
# ---------------------------------------------------------------------------
export GIT_AUTHOR_NAME="dev" GIT_AUTHOR_EMAIL="dev@boutique.pirate"
export GIT_COMMITTER_NAME="dev" GIT_COMMITTER_EMAIL="dev@boutique.pirate"
SITE=/srv/site
rm -rf "$SITE"; mkdir -p "$SITE"; cd "$SITE"
git init -q
cat > app.py <<PY
# Boutique du Capitaine - backend (extrait versionne par erreur)
# TODO: retirer les endpoints internes avant la mise en prod
ROUTES = ["/", "/catalogue", "/panier", "/api/v1/products"]
PY
cat > .env <<ENV
# Configuration locale - NE PAS COMMITER
DB_PASSWORD=dev-password
STRIPE_KEY=$APIKEY
# Endpoint interne (reporting) - acces restreint cote reseau normalement
INTERNAL_LEDGER=$INTERNAL
# Fragment de reconnaissance (laisse par le dev, honteux)
RECON_FRAGMENT_GIT=$F_GIT
ENV
git add . >/dev/null; git commit -qm "init boutique backend + config"
git rm -q .env >/dev/null
echo ".env" > .gitignore
git add .gitignore >/dev/null
git commit -qm "chore: retire .env du depot (secrets)"   # trop tard : reste dans l'historique
cd /app

# ---------------------------------------------------------------------------
# 2) Bundle JS minifie + source map revelant routes et fragment
# ---------------------------------------------------------------------------
cat > /app/static/app.min.js <<JS
(function(){var r=["/","/catalogue","/panier"];function boot(){console.log("boutique ready")}boot();})();
//# sourceMappingURL=app.min.js.map
JS

ORIG_SRC=$(cat <<SRC
// app.js (source originale - ne devrait pas etre expose via la source map)
// Table de routes complete du frontend, y compris l'espace d'administration.
const ROUTES = {
  public: ["/", "/catalogue", "/panier"],
  api:    ["/api/v1/products", "/graphql"],
  // Interface interne - non liee dans le menu
  admin:  ["/console-6f3a", "/console-6f3a/exports"]
};
// Laisse par un dev : fragment de reconnaissance
const RECON_FRAGMENT_JS = "$F_JS";
// NB: l'introspection GraphQL est restee activee en prod (oups)
SRC
)
python3 - "$ORIG_SRC" <<'PYMAP'
import json, sys
src = sys.argv[1]
m = {"version":3,"file":"app.min.js","sources":["app.js"],
     "names":[],"mappings":"","sourcesContent":[src]}
open("/app/static/app.min.js.map","w").write(json.dumps(m))
PYMAP

echo "build_assets: fragments generes (git=$F_GIT gql=$F_GQL js=$F_JS)"
