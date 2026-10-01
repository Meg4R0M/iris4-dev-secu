#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scoreboard local embarque (remplace CTFd, 100% hors-ligne).
Les flags sont generes aleatoirement a l'execution par l'application : ils
n'existent nulle part dans le code ni dans le depot. Le scoreboard les valide
en memoire ; la progression de l'etudiant est stockee cote navigateur
(localStorage), donc aucune base ni compte a gerer.
"""
import hmac
from flask import Blueprint, request, jsonify, render_template_string

def register_scoreboard(app, flags, challenges, title="CTF"):
    """flags: {key: valeur_flag}. challenges: [{key, code, name, cat, points}]."""
    by_flag = {v: c for c in challenges for k, v in flags.items() if k == c["key"]}
    total_pts = sum(c["points"] for c in challenges)

    @app.route("/scoreboard")
    def scoreboard():
        return render_template_string(_PAGE, challenges=challenges,
                                      title=title, total=len(challenges),
                                      total_pts=total_pts)

    @app.route("/api/score/check", methods=["POST"])
    def score_check():
        data = request.get_json(silent=True) or request.form
        submitted = (data.get("flag") or "").strip()
        for flagval, chall in by_flag.items():
            if hmac.compare_digest(submitted, flagval):
                return jsonify({"valid": True, "key": chall["key"],
                                "name": chall["name"], "code": chall["code"],
                                "points": chall["points"]})
        return jsonify({"valid": False})

    return app

_PAGE = r"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scoreboard - {{ title }}</title>
<style>
:root{--bg:#0A0E1A;--card:#141927;--grid:#2A3148;--green:#00FF9C;--cyan:#00D4FF;--pink:#FF3399;--amber:#FFB800;--txt:#E8EAF0;--muted:#8892B0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font-family:-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5}
header{border-bottom:1px solid var(--grid);padding:14px 22px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
header .brand{color:var(--green);font-weight:700;font-family:ui-monospace,Consolas,monospace}
header a{color:var(--muted);text-decoration:none;font-size:14px}header a:hover{color:var(--cyan)}
main{max-width:860px;margin:30px auto;padding:0 22px}h1{font-size:26px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 18px}
.bar{height:12px;background:#0d1322;border:1px solid var(--grid);border-radius:99px;overflow:hidden;margin:10px 0}
.bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--green),var(--cyan));transition:width .4s}
.stat{font-family:ui-monospace,Consolas,monospace;color:var(--cyan)}
.submit{display:flex;gap:8px;margin:16px 0}
.submit input{flex:1;background:#0d1322;color:var(--txt);border:1px solid var(--grid);border-radius:6px;padding:11px;font:inherit}
.submit button{background:var(--green);color:#04121a;font-weight:700;border:none;border-radius:6px;padding:11px 20px;cursor:pointer;font:inherit}
#msg{min-height:22px;font-family:ui-monospace,Consolas,monospace;font-size:14px;margin-bottom:10px}
.cat{color:var(--amber);font-family:ui-monospace,Consolas,monospace;font-size:13px;margin:18px 0 6px;text-transform:uppercase;letter-spacing:.06em}
.ch{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid var(--grid);border-left:4px solid var(--grid);border-radius:8px;padding:11px 14px;margin:7px 0}
.ch.ok{border-left-color:var(--green)}
.ch .code{font-family:ui-monospace,Consolas,monospace;color:var(--muted);width:30px}
.ch .name{flex:1}.ch.ok .name{color:var(--green)}
.ch .pts{font-family:ui-monospace,Consolas,monospace;color:var(--muted);font-size:13px}
.ch .tick{width:20px;text-align:center;color:var(--muted)}.ch.ok .tick{color:var(--green)}
.reset{background:none;border:1px solid var(--grid);color:var(--muted);border-radius:6px;padding:7px 12px;cursor:pointer;font:inherit;font-size:13px}
footer{color:#5B6680;text-align:center;padding:30px;font-size:12px;font-family:ui-monospace,monospace}
</style></head><body>
<header><span class="brand">&#9875; Scoreboard</span>
<a href="/">Accueil</a><a href="/scoreboard">Scoreboard</a></header>
<main>
<h1>{{ title }}</h1>
<p class="sub">Soumettez les flags <code>HUMANIX{...}</code> que vous capturez. Validation hors-ligne,
progression enregistree dans votre navigateur.</p>
<div class="bar"><i id="bar"></i></div>
<p><span class="stat" id="prog">0 / {{ total }}</span> challenges &nbsp;&middot;&nbsp;
<span class="stat" id="pts">0 / {{ total_pts }}</span> points</p>
<div class="submit">
  <input id="flag" placeholder="HUMANIX{...}" autocomplete="off" autofocus>
  <button onclick="submitFlag()">Valider</button>
</div>
<div id="msg"></div>
{% set cats = challenges|map(attribute='cat')|list %}
{% for cat in cats|unique %}
  <div class="cat">{{ cat }}</div>
  {% for c in challenges if c.cat == cat %}
  <div class="ch" id="ch-{{ c.key }}" data-key="{{ c.key }}" data-pts="{{ c.points }}">
    <span class="code">{{ c.code }}</span>
    <span class="name">{{ c.name }}</span>
    <span class="pts">{{ c.points }} pts</span>
    <span class="tick">&#9675;</span>
  </div>
  {% endfor %}
{% endfor %}
<p style="margin-top:22px"><button class="reset" onclick="resetAll()">Reinitialiser ma progression</button></p>
<footer>Scoreboard local - IRIS4 Dev - Humanix Cybersecurity</footer>
</main>
<script>
const KEY = "iris4_solved_{{ title|replace(' ','_') }}";
const TOTAL = {{ total }}, TOTAL_PTS = {{ total_pts }};
function solved(){ try{ return JSON.parse(localStorage.getItem(KEY)||"[]"); }catch(e){ return []; } }
function save(a){ try{ localStorage.setItem(KEY, JSON.stringify(a)); }catch(e){} }
function render(){
  const s = solved(); let pts = 0;
  document.querySelectorAll(".ch").forEach(el=>{
    const ok = s.includes(el.dataset.key);
    el.classList.toggle("ok", ok);
    el.querySelector(".tick").innerHTML = ok ? "&#10003;" : "&#9675;";
    if(ok) pts += parseInt(el.dataset.pts,10);
  });
  document.getElementById("prog").textContent = s.length + " / " + TOTAL;
  document.getElementById("pts").textContent = pts + " / " + TOTAL_PTS;
  document.getElementById("bar").style.width = (TOTAL? (s.length/TOTAL*100):0) + "%";
}
async function submitFlag(){
  const v = document.getElementById("flag").value.trim();
  const msg = document.getElementById("msg");
  if(!v){ return; }
  let j;
  try{
    const r = await fetch("/api/score/check",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({flag:v})});
    j = await r.json();
  }catch(e){ msg.style.color="var(--pink)"; msg.textContent="Erreur reseau."; return; }
  if(j.valid){
    const s = solved();
    if(s.includes(j.key)){ msg.style.color="var(--amber)"; msg.textContent="Deja valide : "+j.name; }
    else{ s.push(j.key); save(s); msg.style.color="var(--green)"; msg.textContent="Flag correct ! ["+j.code+"] "+j.name+" (+"+j.points+" pts)"; }
    document.getElementById("flag").value="";
    render();
  }else{ msg.style.color="var(--pink)"; msg.textContent="Flag incorrect."; }
}
function resetAll(){ if(confirm("Reinitialiser toute votre progression ?")){ save([]); render(); } }
document.getElementById("flag").addEventListener("keydown",e=>{ if(e.key==="Enter") submitFlag(); });
render();
</script></body></html>"""
