import json, os, re, subprocess, sys, time, urllib.request
BASE = "https://www.parlament.gv.at"
UA = {"User-Agent": "research-script", "Content-Type": "application/json"}
pdfdir, out = sys.argv[2], open(sys.argv[3], "w", encoding="utf-8")
def get(url, data=None):
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=UA), timeout=90).read()
for gp in sys.argv[1].split(","):
    d = json.loads(get(BASE + "/Filter/api/filter/data/101?js=eval&showAll=true", json.dumps({"NRBR": ["NR"], "GP_CODE": [gp], "VHG": ["RV"]}).encode()))
    for row in d["rows"]:
        his, title, date = row[14], row[6], row[4]
        rec = {"gp": gp, "nr": row[7], "datum": date, "titel": title, "his": his}
        try:
            c = json.loads(get(BASE + his + "?json=true"))["content"]
            link = next((x["link"] for g in c.get("documents") or [] if "Vorblatt" in g.get("title", "") for x in g["documents"] if x["type"] == "PDF"), None)
            if not link:
                rec["status"] = "kein Vorblatt-Dokument"
            else:
                p = os.path.join(pdfdir, re.sub(r"\W", "_", his) + ".pdf")
                open(p, "wb").write(get(BASE + link))
                t = subprocess.run(["pdftotext", "-enc", "UTF-8", p, "-"], capture_output=True).stdout.decode("utf-8", "replace")
                os.remove(p)
                rec["full"] = bool(re.search(r"Nullszenario", t))
                rec["simplified"] = "Vereinfachte wirkungsorientierte" in t
                m = re.search(r"Nullszenario und allfällige Alternativen\s*(.{0,600}?)(?:\n\s*\n[A-ZÄÖÜ][^\n]{0,60}\n|Vorhandene Studien|Interne Evaluierung|Ziele\b)", t, re.S)
                rec["alt"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
                rec["alt_any"] = len(re.findall(r"[Aa]lternativ", t))
                rec["status"] = "ok"
        except Exception as e:
            rec["status"] = "fehler: " + str(e)[:80]
        out.write(json.dumps(rec, ensure_ascii=False) + "\n"); out.flush()
        time.sleep(0.3)
print("fertig")
