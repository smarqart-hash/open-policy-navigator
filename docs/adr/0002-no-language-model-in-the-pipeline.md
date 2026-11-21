# ADR 0002: Kein Sprachmodell in der Pipeline

Status: abgelöst durch [ADR 0005](0005-language-models-as-documented-proposers.md) · Datum: 2026-11-20

## Kontext

Sprachmodelle schreiben Quellen häufig falsch zu und erfinden Zitate. Das
Portal soll Aussagen belegen, nicht erzeugen.

## Entscheidung

- Abruf, Extraktion und Klassifikation sind regelbasiert und deterministisch
  (`extraction_method: rule`). Gleiche Eingabe, gleiche Ausgabe; jede Regel ist
  im Code nachlesbar und durch Tests und das Eval-Ratchet abgesichert.
- Ein Sprachmodell darf höchstens **Vorschläge** machen (`extraction_method: llm`).
  Solche Einträge bleiben `review_status: pending`, bis ein Mensch sie bestätigt
  (`reviewed_by` ist dann Pflicht, im Schema erzwungen).
- Jedes Zitat (`locator.quote`) muss **wörtlich** im archivierten Quelltext stehen.
  Die CI prüft das gegen den Text, dessen SHA-256 an der Quelle steht. Eine
  Paraphrase ist kein Beleg.
- Kein Sprachmodell bewertet Befunde (Richtung, Sicherheit, Übertragbarkeit).

## Folgen

- Erfassung ist langsamer, dafür prüfbar.
- Der Code des Projekts entsteht KI-assistiert; das ist von dieser Entscheidung
  getrennt (siehe README, „Einsatz von KI-Werkzeugen“). Hier geht es um die Daten.
- Offen: Die Zitatprüfung gegen archivierte Texte ist noch nicht gebaut
  (Roadmap-Issue 3).
