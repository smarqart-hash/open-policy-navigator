import json, re, collections, sys
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
def who(u):
    if "Bundesregierung" in u: return "Bundesregierung"
    if "Bundesrat" in u: return "Bundesrat"
    if "Fraktion" in u or "Gruppe" in u: return "Fraktionen"
    return "andere"
EU = re.compile(r"Richtlinie|Verordnung \(EU\)|Umsetzung|Durchführung der Verordnung|EU\)|Unionsrecht", re.I)
def cls(a):
    if a is None: return "kein Abschnitt gefunden"
    s = a.lower()
    if re.match(r"^(keine|keine\.|keine,|keine;)", s): return "Keine" if len(s) < 25 else "Keine + Begründung"
    if s.startswith("die ") and ("beibehaltung" in s or "rechtslage" in s): return "Status quo genannt"
    return "Alternativen benannt/diskutiert"
# dedupe by nr
seen = {}
for r in rows: seen[r["nr"]] = r
rows = list(seen.values())
print("unique", len(rows))
for wp in ("20", "21"):
    for g in ("Bundesregierung", "Fraktionen", "Bundesrat"):
        sub = [r for r in rows if r["wp"] == wp and who(r["urheber"]) == g]
        c = collections.Counter(cls(r["alt"]) for r in sub)
        print(f"WP{wp} {g:16} n={len(sub):4}", dict(c.most_common()))
gov = [r for r in rows if who(r["urheber"]) == "Bundesregierung"]
eu = [r for r in gov if EU.search(r["titel"] or "")]
ne = [r for r in gov if not EU.search(r["titel"] or "")]
k = lambda L: sum(cls(r["alt"]) in ("Keine", "Keine + Begründung") for r in L)
found = lambda L: [r for r in L if r["alt"] is not None]
print("Regierung gesamt mit Abschnitt", len(found(gov)), "davon Keine*", k(found(gov)))
print("Regierung EU-Bezug im Titel", len(found(eu)), "Keine*", k(found(eu)))
print("Regierung ohne EU-Bezug", len(found(ne)), "Keine*", k(found(ne)))
import random; random.seed(1)
for r in random.sample([r for r in found(ne) if cls(r["alt"]) == "Keine + Begründung"], 4) + random.sample([r for r in found(gov) if cls(r["alt"]) == "Alternativen benannt/diskutiert"], 4):
    print("-", r["nr"], r["titel"][:80], "|", r["alt"][:160])
