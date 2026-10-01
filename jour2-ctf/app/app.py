#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La Boutique du Capitaine, application DELIBEREMENT VULNERABLE (usage pedagogique).
NE JAMAIS deployer hors d'un environnement isole.

Chaque challenge renvoie un flag HUMANIX{...}. Les flags sont GENERES ALEATOIREMENT
au demarrage du conteneur : ils n'existent nulle part dans le code ni dans le depot.
Un scoreboard local embarque (/scoreboard) valide les flags hors-ligne, sans CTFd.
"""
import os, sqlite3, base64, hmac, hashlib, json, re, secrets, urllib.request
from flask import Flask, request, make_response, redirect, render_template, g, jsonify
from scoreboard import register_scoreboard

DB = "/tmp/boutique.db"
APP_URL = os.environ.get("APP_URL", "http://localhost:8002")

# --- Flags ------------------------------------------------------------------
# AUCUN flag en clair dans le code : chaque flag est forge aleatoirement au
# demarrage (slug memorisable + suffixe aleatoire). Rien a configurer, rien a
# pousser sur GitHub. Le scoreboard local les valide.
def _mk(slug):
    return "HUMANIX{%s_%s}" % (slug, secrets.token_hex(4))

FLAGS = {
    "default_creds":  _mk("p0rte_du_capitaine"),
    "sqli_bypass":    _mk("serrure_en_sucre"),
    "sqli_union":     _mk("carte_derriere_la_carte"),
    "xss_reflected":  _mk("perroquet_bavard"),
    "xss_stored":     _mk("message_grave"),
    "idor":           _mk("profil_du_capitaine"),
    "path_traversal": _mk("cale_aux_tresors"),
    "debug_endpoint": _mk("trappe_oubliee"),
    "jwt_none":       _mk("sceau_du_capitaine"),
    "base64_token":   _mk("message_en_bouteille"),
}
JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_hex(16))

# Metadonnees des challenges (pour le scoreboard local).
CHALLENGES = [
    {"key": "default_creds",  "code": "03", "name": "La porte du capitaine",      "cat": "Auth",      "points": 100},
    {"key": "base64_token",   "code": "07", "name": "Le message en bouteille",    "cat": "Auth",      "points": 150},
    {"key": "jwt_none",       "code": "08", "name": "Le sceau du capitaine",      "cat": "Auth",      "points": 350},
    {"key": "sqli_bypass",    "code": "06", "name": "La serrure en sucre",        "cat": "Injection", "points": 200},
    {"key": "xss_reflected",  "code": "05", "name": "Le perroquet bavard",        "cat": "Injection", "points": 150},
    {"key": "sqli_union",     "code": "13", "name": "La carte derriere la carte", "cat": "Injection", "points": 300},
    {"key": "xss_stored",     "code": "20", "name": "Le message grave",           "cat": "Injection", "points": 400},
    {"key": "idor",           "code": "01", "name": "Le profil du capitaine",     "cat": "Acces",     "points": 150},
    {"key": "debug_endpoint", "code": "04", "name": "La trappe oubliee",          "cat": "Acces",     "points": 100},
    {"key": "path_traversal", "code": "11", "name": "La cale aux tresors",        "cat": "Acces",     "points": 250},
]

app = Flask(__name__)
register_scoreboard(app, FLAGS, CHALLENGES, title="La Boutique du Capitaine")

# --- Base de données --------------------------------------------------------
def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    d = g.pop("db", None)
    if d: d.close()

def init_db():
    con = sqlite3.connect(DB); c = con.cursor()
    c.executescript("""
    DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS messages; DROP TABLE IF EXISTS secrets;
    CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, email TEXT, note TEXT);
    CREATE TABLE messages (id INTEGER PRIMARY KEY, author TEXT, body TEXT);
    CREATE TABLE secrets (name TEXT, value TEXT);
    """)
    c.executemany("INSERT INTO users (username,password,role,email,note) VALUES (?,?,?,?,?)", [
        ("admin", "admin", "admin", "capitaine@boutique.pirate", FLAGS["idor"]),
        ("bob",   "sunshine", "user", "bob@boutique.pirate", "matelot ordinaire"),
        ("alice", "P@ssw0rd!", "user", "alice@boutique.pirate", "quartier-maître"),
        ("mousse","1234", "user", "mousse@boutique.pirate", "compte faible - brute force"),
    ])
    c.execute("INSERT INTO secrets VALUES (?,?)", ("union_loot", FLAGS["sqli_union"]))
    con.commit(); con.close()

# --- Helpers JWT (volontairement permissif : accepte alg:none) --------------
def b64url(d): return base64.urlsafe_b64encode(d).rstrip(b"=").decode()
def b64url_dec(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def jwt_make(payload, alg="HS256"):
    header = {"alg": alg, "typ": "JWT"}
    h = b64url(json.dumps(header).encode()); p = b64url(json.dumps(payload).encode())
    signing = f"{h}.{p}".encode()
    sig = hmac.new(JWT_SECRET.encode(), signing, hashlib.sha256).digest()
    return f"{h}.{p}.{b64url(sig)}"

def jwt_verify(token):
    # FAIBLE : fait confiance au champ 'alg' du token (dont 'none').
    h, p, s = token.split(".")
    header = json.loads(b64url_dec(h)); payload = json.loads(b64url_dec(p))
    if header.get("alg") == "none":
        return payload
    expected = b64url(hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest())
    if hmac.compare_digest(expected, s):
        return payload
    return None

# --- Routes publiques -------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    if request.method == "POST":
        u = request.form.get("username", ""); p = request.form.get("password", "")
        # Requête construite par concaténation → SQLi.
        q = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (u, p)
        try:
            row = db().execute(q).fetchone()
        except Exception as e:
            return render_template("login.html", msg="Erreur SQL : %s" % e)
        if row:
            if row["username"] == "admin" and u == "admin" and p == "admin":
                msg = "Connecté en admin. Flag : " + FLAGS["default_creds"]
            elif u != "admin" and "'" in (u + p):
                msg = "Authentification contournée. Flag : " + FLAGS["sqli_bypass"]
            else:
                msg = "Bienvenue, %s (rôle: %s)." % (row["username"], row["role"])
            resp = make_response(render_template("login.html", msg=msg))
            resp.set_cookie("session_user", row["username"])
            return resp
        return render_template("login.html", msg="Identifiants invalides.")
    return render_template("login.html", msg=msg)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    results, error = [], None
    if q:
        sql = "SELECT username, email FROM users WHERE username LIKE '%%%s%%'" % q
        try:
            rows = db().execute(sql).fetchall()
            results = [dict(r) for r in rows]
        except Exception as e:
            error = str(e)
    return render_template("search.html", q=q, results=results, error=error)

@app.route("/greet")
def greet():
    name = request.args.get("name", "matelot")
    # Rendu non échappé → XSS réfléchie.
    html = '<div class="greet">Ahoy, %s !</div>' % name
    hint = ("Si vous voyez votre script s'exécuter, le flag est : " + FLAGS["xss_reflected"]) \
        if ("<script" in name.lower() or "onerror" in name.lower()) else ""
    return render_template("greet.html", greet_html=html, hint=hint)

@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():
    if request.method == "POST":
        author = request.form.get("author", "anonyme")
        body = request.form.get("body", "")
        db().execute("INSERT INTO messages (author, body) VALUES (?,?)", (author, body))
        db().commit()
        return redirect("/guestbook")
    rows = db().execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    return render_template("guestbook.html", messages=rows)  # rendu non échappé

@app.route("/admin/visit")
def admin_visit():
    """Le 'bot admin' consulte le livre d'or avec son cookie secret (= flag).
    Il modélise un navigateur : si un message contient une exfiltration vers une URL,
    il transmet son cookie à cette URL (challenge XSS stockée + bot)."""
    rows = db().execute("SELECT body FROM messages").fetchall()
    admin_cookie = "admin_session=" + FLAGS["xss_stored"]
    sent = []
    for r in rows:
        body = r["body"] or ""
        # extrait une URL de exfiltration (src=... ou fetch('...'))
        m = re.search(r"""(?:src|href)=['"]([^'"]+)['"]""", body) or \
            re.search(r"""fetch\(['"]([^'"]+)['"]""", body)
        if m:
            url = m.group(1)
            if "cookie" in body.lower():  # le payload tente de lire document.cookie
                sep = "&" if "?" in url else "?"
                target = "%s%sc=%s" % (url, sep, admin_cookie)
                try:
                    urllib.request.urlopen(target, timeout=2)
                    sent.append(target)
                except Exception:
                    sent.append(target + "  (cible injoignable - lancez votre collecteur)")
    return jsonify({"bot": "le capitaine a consulté le livre d'or",
                    "exfiltrations_tentees": sent or "aucun payload d'exfiltration détecté"})

@app.route("/collector")
def collector():
    """Collecteur d'exfiltration fourni pour le TP (joue le rôle du serveur de l'attaquant)."""
    c = request.args.get("c", "")
    if c:
        with open("/tmp/collector.log", "a") as f:
            f.write(c + "\n")
    return "ok"

@app.route("/collector/log")
def collector_log():
    try:
        return "<pre>" + open("/tmp/collector.log").read() + "</pre>"
    except FileNotFoundError:
        return "<pre>(vide - aucune donnée exfiltrée pour l'instant)</pre>"

@app.route("/api/profile/<int:uid>")
def api_profile(uid):
    # IDOR : aucune vérification d'appartenance.
    row = db().execute("SELECT id, username, email, role, note FROM users WHERE id=?", (uid,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))

@app.route("/download")
def download():
    fn = request.args.get("file", "brochure.txt")
    # Path traversal : la saisie n'est pas assainie.
    base = "/app/files/"
    path = base + fn
    try:
        with open(path, "r", errors="ignore") as f:
            data = f.read()
        return "<pre>" + data + "</pre>"
    except Exception as e:
        return "Erreur : %s" % e, 404

@app.route("/debug")
def debug():
    # Endpoint de debug laissé en production (A05).
    return jsonify({
        "env": {k: v for k, v in os.environ.items() if "FLAG" not in k and "SECRET" not in k},
        "routes": [str(r) for r in app.url_map.iter_rules()],
        "message": "Endpoint de debug exposé.",
        "flag": FLAGS["debug_endpoint"],
    })

@app.route("/api/me")
def api_me():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        tok = jwt_make({"user": "bob", "role": "user"})
        return jsonify({"info": "Fournissez un JWT : Authorization: Bearer <token>",
                        "exemple_token_utilisateur": tok})
    payload = jwt_verify(auth[7:])
    if not payload:
        return jsonify({"error": "signature invalide"}), 401
    if payload.get("role") == "admin":
        return jsonify({"user": payload.get("user"), "role": "admin",
                        "flag": FLAGS["jwt_none"]})
    return jsonify({"user": payload.get("user"), "role": payload.get("role"),
                    "note": "Vous n'êtes pas admin."})

@app.route("/token")
def token():
    # "Jeton sécurisé" qui n'est en fait que du Base64 (A02).
    secret = "le-tresor-est-sous-le-palmier::" + FLAGS["base64_token"]
    return jsonify({"token": base64.b64encode(secret.encode()).decode(),
                    "note": "Jeton 'chiffré' du capitaine. Bonne chance pour le lire."})

if __name__ == "__main__":
    os.makedirs("/app/files", exist_ok=True)
    with open("/app/files/brochure.txt", "w") as f:
        f.write("Bienvenue à la Boutique du Capitaine !\n")
    # fichier sensible accessible par path traversal
    with open("/app/files/.secret_cargo", "w") as f:
        f.write("Cargo secret du capitaine. Flag : " + FLAGS["path_traversal"] + "\n")
    init_db()
    app.run(host="0.0.0.0", port=8002, debug=False)
