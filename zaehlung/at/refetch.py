import json, os, re, subprocess, sys, time, urllib.request
BASE = "https://www.parlament.gv.at"; UA = {"User-Agent": "research-script"}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
R = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
n = 0
for r in R:
    if not (r.get("full") and not r.get("alt")): continue
    c = json.loads(get(BASE + r["his"] + "?json=true"))["content"]
    link = next(x["link"] for g in c["documents"] if "Vorblatt" in g["title"] for x in g["documents"] if x["type"] == "PDF")
    p = os.path.join(sys.argv[2], "tmp.pdf"); open(p, "wb").write(get(BASE + link))
    t = subprocess.run(["pdftotext", "-enc", "UTF-8", p, "-"], capture_output=True).stdout.decode("utf-8", "replace"); os.remove(p)
    i = t.find("Nullszenario")
    seg = re.sub(r"\s+", " ", t[i:i + 900])
    seg = re.sub(r"^Nullszenario\s*(und allfällige Alternativen)?\s*", "", seg)
    seg = re.split(r"(Vorhandene Studien|Interne Evaluierung|Beitrag zu Wirkungsziel|Ziele Ziel 1)", seg)[0].strip()
    r["alt"] = seg[:600]; r["alt_src"] = "refetch"; n += 1; time.sleep(0.3)
open(sys.argv[1], "w", encoding="utf-8").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in R))
print("refetched", n)
