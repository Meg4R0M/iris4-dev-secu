#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cible de reconnaissance - Jour 1, TP1.
Application volontairement « bavarde » : en-têtes révélateurs, endpoints oubliés,
cookies mal configurés, messages d'erreur verbeux. L'objectif du TP n'est PAS
d'exploiter mais de CARTOGRAPHIER la surface d'attaque.
"""
import os, secrets
from flask import Flask, request, jsonify, make_response, render_template
from scoreboard import register_scoreboard

app = Flask(__name__)
# Aucun flag en clair : forge aleatoirement au demarrage.
TOKEN = "HUMANIX{surface_cartographiee_%s}" % secrets.token_hex(4)
CHALLENGES = [
    {"key": "recon", "code": "1", "name": "Cartographie de la surface d'attaque", "cat": "Recon", "points": 100},
]
register_scoreboard(app, {"recon": TOKEN}, CHALLENGES, title="Recon")

@app.after_request
def leaky_headers(resp):
    # En-têtes qui trahissent la stack (mauvaise pratique volontaire).
    resp.headers["Server"] = "Werkzeug/old-Python/3.12 BoutiquePirate/0.3.1"
    resp.headers["X-Powered-By"] = "Flask-Boutique-Framework"
    resp.headers["X-Debug-Mode"] = "on"
    # Cookie sans HttpOnly / Secure / SameSite.
    if not request.cookies.get("visitor"):
        resp.set_cookie("visitor", "guest-0001")
    return resp

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/robots.txt")
def robots():
    # Révèle des chemins "cachés" (classique en recon).
    body = ("User-agent: *\n"
            "Disallow: /admin-panel\n"
            "Disallow: /debug\n"
            "Disallow: /api/v1/\n"
            "Disallow: /backup/\n")
    return app.response_class(body, mimetype="text/plain")

@app.route("/admin-panel")
def admin_panel():
    return jsonify({
        "message": "Panneau d'admin oublié (non protégé).",
        "surface": {
            "endpoints": ["/", "/login (démo)", "/api/v1/status", "/api/v1/users",
                          "/debug", "/backup/dump.sql", "/admin-panel"],
            "techno": "Flask / Python / SQLite",
            "note": "Vous avez cartographié la surface ! " + TOKEN,
        },
    })

@app.route("/debug")
def debug():
    return jsonify({"debug": True, "routes": [str(r) for r in app.url_map.iter_rules()],
                    "python": os.sys.version})

@app.route("/api/v1/status")
def status():
    return jsonify({"status": "ok", "version": "0.3.1", "build": "dev-unstable"})

@app.route("/api/v1/users")
def users():
    # Expose trop de données (A06 / API).
    return jsonify([{"id": 1, "user": "admin", "email": "admin@boutique.pirate"},
                    {"id": 2, "user": "bob", "email": "bob@boutique.pirate"}])

@app.route("/backup/dump.sql")
def backup():
    return app.response_class("-- sauvegarde SQL oubliée dans la webroot\n"
                              "-- (fuite de structure : encore de la recon)\n"
                              "CREATE TABLE users (id, username, password_hash, role);\n",
                              mimetype="text/plain")

@app.route("/product")
def product():
    pid = request.args.get("id", "")
    if not pid.isdigit():
        # Message d'erreur verbeux (fuite d'info).
        return ("TypeError: product id must be int, got %r at app.py:product() "
                "[stack: boutique.handlers.product -> db.query]" % pid), 500
    return jsonify({"id": int(pid), "name": "longue-vue", "price": 42})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)
