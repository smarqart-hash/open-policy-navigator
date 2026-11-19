import os, json, re, time, urllib.request, urllib.parse, sys
KEY = os.environ["DIP_API_KEY"]
out = open(sys.argv[2], "w", encoding="utf-8")
def fetch(wp):
    cursor = None
    while True:
        p = {"f.drucksachetyp": "Gesetzentwurf", "f.wahlperiode": wp, "f.zuordnung": "BT", "format": "json"}
        if cursor: p["cursor"] = cursor
        req = urllib.request.Request("https://search.dip.bundestag.de/api/v1/drucksache-text?" + urllib.parse.urlencode(p), headers={"Authorization": "ApiKey " + KEY})
        d = json.load(urllib.request.urlopen(req, timeout=90))
        docs = d.get("documents", [])
        for doc in docs:
            yield doc
        if not docs or d.get("cursor") == cursor: break
        cursor = d["cursor"]; time.sleep(0.4)
SEC = re.compile(r"C\.\s*Alternative[n]?\s*(.{0,700}?)\s*(?:D\.\s|$)", re.S)
n = 0
for wp in sys.argv[1].split(","):
    for doc in fetch(wp):
        t = doc.get("text", "")
        m = SEC.search(t[:20000])
        sec = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        urh = ";".join(u.get("titel", "") for u in doc.get("urheber", []))
        out.write(json.dumps({"wp": wp, "nr": doc.get("dokumentnummer"), "datum": doc.get("datum"), "titel": doc.get("titel"), "urheber": urh, "alt": sec}, ensure_ascii=False) + "\n")
        n += 1
print("docs", n)
