# ADR 0005: Sprachmodelle als dokumentierte Vorschlaggeber

Status: angenommen · Datum: 2026-11-20 · Löst [ADR 0002](0002-no-language-model-in-the-pipeline.md) ab

## Kontext

ADR 0002 schloss Sprachmodelle aus der Pipeline aus. Für die Erfassung von
Fällen, Befunden und Positionen ist reine Handarbeit aber zu langsam. Der Stand
der Evidenzsynthese ist ein anderer Weg: Cochrane, Campbell, JBI und CEE
verlangen seit 2025 gemeinsam, dass KI nur unter menschlicher Aufsicht und mit
offener Dokumentation eingesetzt wird (Positionspapier 2025, doi:10.1186/s13750-025-00374-5).
Zwei Befunde schränken das ein:

- Ein wörtlich korrektes Zitat verhindert keinen falschen Schluss. Automatische
  Prüfer erkennen das bei nuancierten Fällen nur in rund 75–80 % der Fälle.
- Prüfende nicken Vorschläge ab (Automation Bias). Schulung verhindert das nicht.
  Man kann es nur messen.

Stefan hat am 20.11.2026 entschieden, Sprachmodelle unter den folgenden
Bedingungen zuzulassen.

## Entscheidung

Abruf, Extraktion und Klassifikation der Gesetzentwürfe bleiben regelbasiert.
Sprachmodelle dürfen in der Vorprüfung **Vorschläge** machen, unter diesen
Bedingungen:

1. **Wörtliches Zitat.** Jeder Vorschlag trägt `locator.quote`. Dieses Zitat muss
   wörtlich im archivierten Quelltext stehen, und der SHA-256 dieses Texts hängt
   an der Quelle. Paraphrasen sind kein Beleg.
2. **Kennzeichnung.** Für jeden Vorschlag gilt `extraction_method: llm` und
   `review_status: proposed`. Modell und Prompt-Version werden dokumentiert.
3. **Nie ungeprüft als geprüft.** Erst ein Mensch setzt `confirmed` oder
   `rejected`, und `reviewed_by` ist dann Pflicht. Das Schema erzwingt das.
   Veröffentlichungen und der MCP-Server zeigen den Prüfstatus an.
4. **Deckungsfrage beim Menschen.** Für jede Aussage prüft ein Mensch: Folgt
   die Aussage aus dem Zitat? Die Wörtlichkeitsprüfung ersetzt diese Prüfung nicht.
5. **Abnicken messen.** Aus allen übernommenen Einträgen wird eine Zufallsstichprobe
   erneut geprüft, auch aus den automatisch übernommenen. Die Fehlerquote wird
   mit Konfidenzintervall veröffentlicht.
6. **Goldstandard.** Er wird doppelt kodiert, Ziel sind etwa 70 Entwürfe.
   Für jede Kategorie wird Krippendorff-α mit Konfidenzintervall berichtet; Ziel
   ist α ≥ 0,800. Das Eval-Ratchet zählt nur bestätigte Labels.
7. Kein Sprachmodell setzt Richtung, Sicherheit oder Übertragbarkeit eines
   Befunds ohne menschliche Bestätigung.

## Folgen

- Die Erfassung wird schneller. Die Prüfqualität ist messbar und öffentlich.
- `ReviewStatus.PENDING` heißt jetzt `PROPOSED` (`proposed`).
- Offen sind noch: die Zitatprüfung gegen archivierte Texte, die Audit-Stichprobe,
  Krippendorff-α im Eval-Skript (bisher nur Cohen-κ) und die Dokumentation von
  Modell und Prompt-Version im Schema.
