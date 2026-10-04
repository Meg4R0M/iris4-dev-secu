#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cible de reconnaissance - Jour 1, TP1 (HARD MODE).
Rien n'est servi sur un plateau : il faut enchainer plusieurs decouvertes.
Le flag final s'ASSEMBLE a partir de 3 fragments trouves a des endroits differents :
  - fragment 1 : via la fuite .git -> chemin interne -> endpoint "ledger"
  - fragment 2 : via l'introspection GraphQL -> internalNotes(userId: 0)
  - fragment 3 : via la source map du bundle JS
Format du flag : HUMANIX{recon_<frag1>_<frag2>_<frag3>}
"""
import os, json, time, collections
from flask import Flask, request, jsonify, make_response, render_template, send_from_directory, abort
from graphql import build_schema, graphql_sync
from scoreboard import register_scoreboard

FRAG = json.load(open("/app/secrets/fragments.json"))
FINAL_FLAG = "HUMANIX{recon_%s_%s_%s}" % (FRAG["git"], FRAG["graphql"], FRAG["js"])
INTERNAL = FRAG["internal"]            # ex: /api/internal/v2/ledger

app = Flask(__name__)
CHALLENGES = [
    {"key": "recon", "code": "1", "name": "Surface d'attaque reconstituee (3 fragments)",
     "cat": "Recon", "points": 300},
]
register_scoreboard(app, {"recon": FINAL_FLAG}, CHALLENGES, title="Recon")

# --- Tarpit : punit le fuzzing aveugle (trop de 404 -> 429 temporaire) ------
_hits = collections.defaultdict(list)
_blocked = {}
def tarpit():
    ip = request.remote_addr or "?"
    now = time.time()
    if _blocked.get(ip, 0) > now:
        return True
    _hits[ip] = [t for t in _hits[ip] if now - t < 30]
    return False
def note_404():
    ip = request.remote_addr or "?"
    now = time.time()
    _hits[ip].append(now)
    if len(_hits[ip]) > 40:
        _blocked[ip] = now + 20

@app.after_request
def headers(resp):
    # En-tetes volontairement discrets : peu d'infos gratuites (fingerprinting plus dur)
    resp.headers["Server"] = "nginx"
    resp.headers.pop("X-Powered-By", None)
    return resp

# --- Frontend --------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/catalogue")
def catalogue():
    return jsonify({"items": ["longue-vue", "boussole", "perroquet"]})

@app.route("/static/<path:p>")
def static_files(p):
    return send_from_directory("/app/static", p)

# --- Fuite .git (volontairement exposee) -----------------------------------
@app.route("/.git/<path:p>")
def git_leak(p):
    full = os.path.join("/srv/site/.git", p)
    if os.path.isfile(full):
        return send_from_directory("/srv/site/.git", p)
    note_404(); abort(404)

# --- API publique + oracle d'erreur verbeuse -------------------------------
@app.route("/api/v1/products")
def products():
    # Oracle : une entree inattendue fait "fuiter" une trace interne.
    sort = request.args.get("sort")
    if request.is_json or request.content_type and "xml" in (request.content_type or ""):
        return ("ParseError: unsupported media type at gateway.parse() "
                "-> proxy_pass %s [trace: boutique.api.v1.products]" % INTERNAL), 400
    if sort and not sort.isalnum():
        return ("TypeError: sort must be alphanumeric, got %r at "
                "boutique.api.v1.products.sort() -> see %s" % (sort, INTERNAL)), 500
    return jsonify([{"id": 1, "name": "longue-vue"}, {"id": 2, "name": "boussole"}])

# --- Endpoint "interne" revele par le .env (chemin dans INTERNAL) ----------
@app.route(INTERNAL)
def internal_ledger():
    # "Interne" mais expose : renvoie le fragment 1.
    return jsonify({"ledger": "ok", "note": "acces interne - usage restreint",
                    "fragment_1": FRAG["git"]})

# --- Console d'admin (revelee par la source map) + vhost Host header -------
@app.route("/console-6f3a")
def admin_console():
    # Accessible uniquement avec le bon vhost (en-tete Host).
    host = (request.headers.get("Host") or "").split(":")[0]
    if host != "admin.boutique.pirate":
        note_404(); abort(404)
    return jsonify({
        "console": "exports & notes internes",
        "astuce": "les notes systeme sont exposees via GraphQL : internalNotes(userId: 0)",
    })

# --- GraphQL avec introspection activee (fragment 2) -----------------------
SDL = """
type Query {
  products: [Product!]!
  internalNotes(userId: Int!): String
}
type Product { id: Int!  name: String! }
"""
schema = build_schema(SDL)
def _resolve_products(obj, info): return [{"id": 1, "name": "longue-vue"}]
def _resolve_notes(obj, info, userId):
    # userId 0 = compte systeme : sa note contient le fragment 2.
    return ("Note systeme. fragment_2=%s" % FRAG["graphql"]) if userId == 0 else "aucune note"
schema.query_type.fields["products"].resolve = _resolve_products
schema.query_type.fields["internalNotes"].resolve = _resolve_notes

@app.route("/graphql", methods=["GET", "POST"])
def graphql_endpoint():
    if request.method == "GET":
        return ("GraphQL endpoint. POST { query } ici. (introspection: activee)", 200)
    data = request.get_json(silent=True) or {}
    result = graphql_sync(schema, data.get("query", ""),
                          variable_values=data.get("variables"))
    out = {}
    if result.data is not None: out["data"] = result.data
    if result.errors: out["errors"] = [str(e) for e in result.errors]
    return jsonify(out)

# --- Leurres + tarpit ------------------------------------------------------
@app.route("/admin")
@app.route("/backup")
@app.route("/old")
@app.route("/.env")
def decoys():
    note_404()
    return ("Not Found", 404)

@app.errorhandler(404)
def not_found(e):
    if tarpit():
        return ("Too Many Requests - ralentissez votre enumeration", 429)
    note_404()
    return ("Not Found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
