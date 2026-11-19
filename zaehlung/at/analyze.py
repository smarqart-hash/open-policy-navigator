import json, re, collections, sys, random
R = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
def cls(r):
    if r["status"] != "ok": return r["status"][:30]
    if not r.get("full"): return "vereinfacht: kein Alternativen-Feld"
    a = (r.get("alt") or "")
    if not a: return "voll: Abschnitt nicht extrahiert"
    s = a.lower()
    if re.search(r"keine (sinnvolle[n]? |zweckmäßige[n]? |gleichwertige[n]? |realistische[n]? )?alternativ|alternativen? (bestehen|gibt es) nicht|alternativen?[^.]{0,80}nicht (bekannt|ersichtlich|gegeben|vorhanden)|keine\.?$|^keine", s): return "voll: keine Alternative"
    if "alternativ" in s: return "voll: Alternative benannt/diskutiert"
    return "voll: nur Nullszenario"
for gp in ("XXVIII", "XXVII"):
    sub = [r for r in R if r["gp"] == gp]
    print(gp, len(sub), dict(collections.Counter(cls(r) for r in sub).most_common()))
allr = [r for r in R if r["status"] == "ok"]
full = [r for r in allr if r.get("full")]
c = collections.Counter(cls(r) for r in full)
print("gesamt ok", len(allr), "voll", len(full), dict(c))
random.seed(3)
for k in ["voll: keine Alternative", "voll: nur Nullszenario", "voll: Alternative benannt/diskutiert", "voll: Abschnitt nicht extrahiert"]:
    xs = [r for r in full if cls(r) == k]
    for r in random.sample(xs, min(3, len(xs))):
        print(k[:12], "|", r["nr"], r["gp"], r["titel"][:55], "|", (r.get("alt") or "")[:170])
