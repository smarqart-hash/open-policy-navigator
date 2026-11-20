# Open Policy Navigator: Hintergrund und Stand der Forschung

Stand: 20.11.2026. Diese Seite ordnet das Projekt in Forschung und bestehende Angebote ein. Kennzeichnung: [P] Primärquelle gelesen, [S] Sekundärquelle oder nur Abstract.

## 1. Das Problem in Zahlen

- Die Begründung eines Gesetzentwurfs muss darlegen, „ob andere Lösungsmöglichkeiten bestehen … gegebenenfalls welche Erwägungen zu ihrer Ablehnung geführt haben“ (§ 43 Abs. 1 Nr. 3 GGO); das Vorblatt fasst das unter „C. Alternativen“ zusammen (§ 42 Abs. 1 mit Anlage 3). [P] Text Stand 2009, [vzbv-PDF](https://www.vzbv.de/sites/default/files/downloads/gemeinsame_geschaeftsordnung_bundesministerien.pdf)
- Eigene Zählung über die DIP-API: Bei 422 von 532 erkannten Regierungsentwürfen der Wahlperioden 20 und 21 beginnt der Abschnitt mit „Keine“ (79 %), bei 326 steht nur dieses Wort. 87 von 619 Regierungsentwürfen erkennt das Muster noch nicht. Manche Entwürfe verweisen vom Vorblatt in die Begründung (z. B. JStG 2026, BR-Drs. 447/26). Skripte und Daten: `zaehlung/` bzw. Paket `open_policy_navigator`.
- Österreich: 470 Regierungsvorlagen (XXVII./XXVIII. GP) mit Vorblatt und Folgenabschätzung; 286 haben eine vereinfachte Folgenabschätzung ohne Feld für Alternativen; von 184 vollen nennen 2 eine echte Alternative (von Hand geprüft).

Grenze: Gezählt wird, was öffentlich im Vorblatt steht, nicht, was Ministerien intern geprüft haben.

## 2. Der Diskurs: bekannt, aber nie gemessen

| Wer | Befund | Beleg |
|---|---|---|
| Matthias Rossi (Universität Augsburg), „Phantasie in der Gesetzgebung“, 2013 | „Keine“ als fehlender Mut zum eigenen Vorschlag; Alternativen kommen über Pluralität ins Verfahren (Ressorts, Anhörungen, Verbände), nicht über den Initianten | [S] |
| EU Regulatory Scrutiny Board | Optionen „eine der schwächsten“ Komponenten von Folgenabschätzungen, Spektrum oft auf die Vorzugsoption zugeschnitten | [S] [Jahresbericht 2022](https://commission.europa.eu/system/files/2023-05/RSB_2022_1.pdf) |
| UK Regulatory Policy Committee | „identification of options“ ist eines von drei Kriterien für eine rote Bewertung; Anteil „gut/befriedigend“ bei Rationale & Options fiel von 84 % auf 71 % | [P] gov.uk |
| Forschung | Hahn u. a. (USA 1996–99): 27 % ohne Alternativen; Fritsch, Radaelli u. a. (UK/EU 2005–10): andere Instrumente als Ge- und Verbote nur in rund einem Viertel geprüft | [S] [Hahn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=213854), [Fritsch u. a.](https://aei.pitt.edu/33551/1/WD362_Fritsch_et_al_Regulatory_Quality_in_the_Commission_and_the_UK.pdf) |
| Nationaler Normenkontrollrat | Prüfmandat umfasst, ob es praxistauglichere Alternativen gibt | [P] normenkontrollrat.bund.de |
| Bundeserprobungsgesetz (in Kraft seit 10.10.2026) | Reallabore und Experimentierklauseln; Ergebnisse sollen in die Gesetzgebung zurückfließen | [P] [Bundesregierung](https://www.bundesregierung.de/breg-de/schwerpunkte/wirksam-regieren/bundeserprobungsgesetz-2427510) |

## 3. Wer Optionen heute vergleicht

**Geschlossen, für Regierungen und Verwaltung**

| Angebot | Was es tut | Unterschied |
|---|---|---|
| [CentreAI Policy](https://institute.global/insights/tech-and-digitalisation/why-we-built-centreai-policy) (Tony Blair Institute) | KI-Werkzeug für Regierungszentralen; jede Option bekommt einen „Anwalt“ | offen, für Parlament und Öffentlichkeit |
| [PolicyNova](https://apolitical.co/en/pages/announcement-policy-nova-government-ai-navigator) (Apolitical) | KI-Recherche „wie haben andere es gelöst“ für Verwaltungen | dauerhaft gepflegte, prüfbare Einträge statt Antwort pro Anfrage |
| [Nesta „Policy Atlas“](https://www.nesta.org.uk/project-updates/using-ai-to-generate-policy-blueprints/) (Alpha) | Sprachmodell fasst Studien zusammen und bewertet Evidenz | Menschen bestätigen jeden Befund mit Fundstelle; Scheitern und Positionen sichtbar |
| [Overton](https://www.overton.io/pricing) | Datenbank politischer Dokumente, kostenpflichtig | offen, Optionen statt Dokumente |
| Allgemeine KI-Assistenten (ChatGPT, Gemini, Perplexity), Suchmaschinen | Antworten ohne prüfbare Grundlage; Quellen teils falsch zugeordnet (Olejniczak u. a. 2025, Test zur Instrumenten-Typologie) | belegte, versionierte Daten; Abstention statt Erfindung |

**Offen, aber je Politikfeld oder ohne Vergleich**

| Angebot | Was es tut | Was fehlt |
|---|---|---|
| [EEF Teaching and Learning Toolkit](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/), [YEF Toolkit](https://youthendowmentfund.org.uk/yef-toolkit-what-works-to-prevent-youth-violence/), [What Works Growth](https://whatworksgrowth.org/resources/) | bewerten Ansätze nach Wirkung, Evidenzstärke und Kosten | je ein Politikfeld, redaktionell, kein gemeinsames Schema, keine Gegenpositionen |
| Evidence and Gap Maps (Campbell, 3ie) | Matrix Intervention × Ergebnis | zeigen bewusst nicht, was die Evidenz ergibt (White u. a. 2020) |
| [OECD OPSI Case Study Library](https://oecd-opsi.org/case_type/opsi/) | Fallsammlung zu Verwaltungsinnovation | keine Wirkungsbefunde im Vergleich |
| [European Sufficiency Policy Database](https://energysufficiency.de/en/policy-database-en/) | offene Instrumentendatenbank mit Umsetzungsbeispielen (CSV) | nur Suffizienzpolitik |
| [Data to Policy Navigator](https://www.datatopolicy.org/navigator) (UNDP/BMZ, Digital Public Good) | Leitfaden, wie Politik Daten nutzt | Prozesshilfe, keine Optionen- und Befunddatenbank |
| [Bundestagszusammenfasser](https://bundestagszusammenfasser.de/) | liest den „Exekutiven Fußabdruck“ aus Drucksachen | anderes Pflichtfeld, keine API |
| [de-eli-mcp](https://github.com/matematicsolutions/de-eli-mcp) und andere DIP-Clients | reichen Bundestagsdokumente durch | keine Vorblatt-Felder, keine Optionen |
| [EUPLEX](https://data.euplex.org/) | fortlaufender Datensatz zu Kommissionsvorschlägen, regelbasiert | methodisches Vorbild für den Parser |

Im deutschsprachigen Raum haben wir kein offenes, politikfeldübergreifendes Angebot gefunden, das Optionen, Fälle, Befunde und Gegenpositionen verbindet.

## 4. Fachliche Fundierung des Datenmodells

| Element | Grundlage | Beleg |
|---|---|---|
| Instrumenttyp | OECD-Typologie 2024 (ökonomisch, regulatorisch, staatliche Investition, Information, freiwillig), aufbauend auf Vedung („sticks, carrots, sermons“) und Hood (NATO); mehrere Instrumente je Ansatz | [P] OECD 2024, doi:10.1787/68529f35-en; Vedung 2025, doi:10.56645/jmde.v21i50.1169 |
| Ebenen | Hall: Ziele, Instrumente, Einstellung der Instrumente → Feld „Ausgestaltung“ am Fall | [S] Arbeitspapier 1990 |
| Befund | Wirkrichtung und Evidenzstärke getrennt, angelehnt an GRADE und die Maryland-Skala; Evidence Gap Maps kodieren die Richtung bewusst nicht | [P] White u. a. 2020, doi:10.1002/cl2.1125 |
| Status „gestoppt“ | Zustand am Fall, nicht Befund (Policy-Dismantling-Literatur, McConnell zu Erfolg und Scheitern) | [S] |
| Positionen | Akteur stützt oder lehnt ab, mit Datum und Quelle (Diskursnetzwerkanalyse) | [P] Leifeld 2020, doi:10.17645/pag.v8i2.3249 |
| Abdeckung | „noch nicht geprüft“ ≠ „gesucht, nichts gefunden“; fehlende Evidenz erscheint nie als „wirkt nicht“ | eigene Festlegung, ADR im Repo |

Offene Forschungsfrage: Für Gesetze ohne Vergleichsgruppe gibt es keine etablierte Evidenzskala. Wir weisen die Studienart deshalb aus, statt eine Stufe zu behaupten.

## 5. Eigene Vorarbeit

- Recherche zu Zukunftsfragen Europas: rund 540 geprüfte Aussagen, 590 Quellen zu sechs Fragen (Wirtschaft, Klima und Migration, Alterung, KI und Arbeit, Sozialstaatsfinanzierung, Bildung).
- Prototypen: 17 Ansätze zu KI und Arbeit; Fallakte zu älteren Langzeitarbeitslosen in Österreich (Aktion 20.000, Marienthal, Aktion 55+); Demo des Vergleichsportals.
- Zählungen Deutschland und Österreich, Goldset und Eval-Ratchet, Schema v0 mit Herkunftsangaben (dieses Repository).

## 6. Europäische Perspektive

`[OFFEN: nach Gespräch mit Stefan ergänzen]`
