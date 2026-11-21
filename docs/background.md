# Open Policy Navigator: Hintergrund und Stand der Forschung

Stand: 20.11.2026. Diese Seite ordnet das Projekt in Forschung und bestehende Angebote ein. Kennzeichnung: [P] Primärquelle gelesen, [S] Sekundärquelle oder nur Abstract.

## 1. Das Problem in Zahlen

- Die Begründung eines Gesetzentwurfs muss darlegen, „ob andere Lösungsmöglichkeiten bestehen … gegebenenfalls welche Erwägungen zu ihrer Ablehnung geführt haben“ (§ 43 Abs. 1 Nr. 3 GGO); das Vorblatt fasst das unter „C. Alternativen“ zusammen (§ 42 Abs. 1 mit Anlage 3). [P] Text Stand 2009, [vzbv-PDF](https://www.vzbv.de/sites/default/files/downloads/gemeinsame_geschaeftsordnung_bundesministerien.pdf)
- Eigene Zählung über die DIP-API, Wahlperioden 20 und 21: Hochgerechnet haben rund 602 Regierungsentwürfe einen Abschnitt C. Bei 326 steht nur das Wort „Keine“ (rund 54 %), bei rund 466 beginnt er damit (rund 77 %). Nach der Kodierregel, die eine verworfene konkrete Alternative als „Alternativen benannt“ zählt, ergibt sich vorläufig: nur „Keine“ ohne Begründung rund 56 %, „Keine“ mit Begründung ohne konkrete Alternative rund 23 %, nur der Status quo erörtert rund 5 %, eine konkrete Alternative genannt und abgewogen rund 17 % (Spanne rund 14–20 %). In etwa vier von fünf Regierungsentwürfen nennt der Abschnitt also keine konkrete Alternative. Vorbehalt: Die Einordnung sind Vorschläge eines Sprachmodells nach ADR 0005; eine menschliche Prüfung von rund 50 Fällen steht aus (eval/codebook_b). Auffällig: Von den übersehenen langen Abschnitten nennen 11 von 16 eine Alternative, von den gefundenen nur rund 10 %. Das erste Suchmuster erkannte rund 88 % der Abschnitte; es übersah Abschnitte über 700 Zeichen (im Goldset 16 von 20 unerkannten Fällen). Haushaltsgesetze haben kein Vorblatt-C. 87 von 619 Regierungsentwürfen erkennt das Muster noch nicht; ein Teil davon hat keinen Abschnitt C (z. B. Haushaltsgesetze). Spanne über alle 619: 68 % bis 82 %. Das Muster erfasst nur Abschnitte bis rund 700 Zeichen; lange Abschnitte diskutieren eher Alternativen, die Quote ist also eher zu hoch. Robust ist: 326 von 532 nur „Keine“ (61 %). Eine bereinigte Quote ohne Fälle, in denen „Keine“ plausibel ist (EU-Umsetzung, Vertragsgesetze, Haushalt), folgt. Manche Entwürfe verweisen vom Vorblatt in die Begründung (z. B. JStG 2026, BR-Drs. 447/26). Skripte und Daten: `zaehlung/` bzw. Paket `open_policy_navigator`.
- Österreich: 470 Regierungsvorlagen (XXVII./XXVIII. GP) mit Vorblatt und Folgenabschätzung; 286 haben eine vereinfachte Folgenabschätzung ohne Feld für Alternativen; von 184 vollen nennen 2 eine echte Alternative (von Hand geprüft).

Grenze: Gezählt wird, was öffentlich im Vorblatt steht, nicht, was Ministerien intern geprüft haben. Alternativen kommen oft über Ressorts, Verbände und Anhörungen ins Verfahren (Rossi). Die Zahl zeigt also eine Lücke in der öffentlichen Nachvollziehbarkeit, keinen Beleg für fehlendes Nachdenken.

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

## 4a. Prüfschleife: Maschine sortiert vor, Mensch entscheidet

Der Ablauf folgt dem Stand der Evidenzsynthese. Cochrane, Campbell, JBI und CEE verlangen seit 2025 gemeinsam, dass KI in Evidenzsynthesen „with human oversight“ eingesetzt und jede Beteiligung dokumentiert wird [P] (doi:10.1186/s13750-025-00374-5). Ausführlich: ADR 0005 in diesem Repository.

| Stufe | Was passiert | Beleg für das Muster |
|---|---|---|
| 1. Automatisch erfasst | Parser und Importer lesen Entwürfe und offene Datenbanken ein; Regeln statt Handlabeling | Weak Supervision (Ratner u. a. 2017, doi:10.14778/3157794.3157797) |
| 2. Maschinell vorgeprüft | Schema, Zitat wörtlich im archivierten Quelltext, Konsistenz, Dubletten; Sprachmodelle nur als dokumentierte Vorschläge | Cochrane-RCT-Klassifikator, auf 99 % Recall kalibriert, 40–70 % weniger Handsichtung in Pilotabläufen (Thomas u. a. 2021, doi:10.1016/j.jclinepi.2020.11.003) |
| 3. Menschlich geprüft | unsichere Fälle zuerst; Prüffrage je Fakt: Folgt die Aussage aus dem Zitat? | Abgabe unsicherer Fälle (Geifman & El-Yaniv 2017, arXiv:1705.08500); automatische Deckungsprüfer nur rund 75–80 % (AttributionBench, LLM-AggreFact) |
| 4. Im Audit bestätigt | Zufallsstichprobe auch der automatisch übernommenen Einträge; Fehlerquote mit Konfidenzintervall veröffentlicht | Automation Bias lässt sich nicht wegschulen (Parasuraman & Manzey 2010, doi:10.1177/0018720810376055); Prediction-powered Inference (Angelopoulos u. a. 2023, doi:10.1126/science.adi6000) |

Goldstandard: doppelt kodiert, Krippendorff-α je Kategorie mit Konfidenzintervall, Ziel ≥ 0,800 (Krippendorff 2004, doi:10.1093/hcr/30.3.411); ein Eval-Ratchet in der CI verhindert Rückschritte (Muster des ML Test Score, Breck u. a. 2017).

Grenze: Alle Kennzahlen stammen aus Medizin, Psychologie oder englischen Benchmarks. Für Policy-Dokumente gibt es noch keine veröffentlichten Fehlerquoten; das Projekt will die ersten liefern.

## 5. Eigene Vorarbeit

- Recherche zu Zukunftsfragen Europas: rund 540 geprüfte Aussagen, 590 Quellen zu sechs Fragen (Wirtschaft, Klima und Migration, Alterung, KI und Arbeit, Sozialstaatsfinanzierung, Bildung).
- Prototypen: 17 Ansätze zu KI und Arbeit; Fallakte zu älteren Langzeitarbeitslosen in Österreich (Aktion 20.000, Marienthal, Aktion 55+); Demo des Vergleichsportals.
- Zählungen Deutschland und Österreich, Goldset und Eval-Ratchet, Schema v0 mit Herkunftsangaben (dieses Repository).

## 6. Europäische Perspektive: ein lernendes Europa

**Grundsatzziel:** Nicht nur Deutschland vergleicht sich mit anderen. Jedes Land soll seine Vorhaben mit den Ansätzen der anderen vergleichen können: Wer in Lissabon eine Mietregulierung plant, sieht die Erfahrungen aus Wien und Berlin, und umgekehrt. Gegenseitiges Lernen statt nationaler Insellösungen.

**Förderzeitraum klein, Skalierung mitgedacht:**

| Stufe | Inhalt | Technische Vorsorge schon jetzt |
|---|---|---|
| Prototype Fund (6 Monate) | Deutschland und Österreich, Fälle aus ganz Europa als Vergleich | Länder als austauschbare Adapter; Schema mehrsprachig angelegt; stabile Kennungen (DIP, ELI, DOI) |
| Second Stage und Anschluss | Folgenabschätzungen der EU-Kommission als nächste Quelle: Sie müssen Optionen vergleichen, das Regulatory Scrutiny Board bewertet sie öffentlich | Adapter-Anleitung, Beitragsregeln, Partner in weiteren Ländern |
| Perspektive | weitere Parlamente, Übersetzungen, gemeinsamer Betrieb mit europäischen Partnern | offenes Schema als möglicher gemeinsamer Standard |

**Anschluss an die Better-Regulation-Agenda (zu prüfen und zu belegen, bevor es im Antrag steht):**

- EU-Leitlinien und Toolbox für bessere Rechtsetzung: verlangen in Folgenabschätzungen den Vergleich von Optionen; der Navigator macht diese Vergleiche auffindbar und vergleichbar.
- Regulatory Scrutiny Board: öffentliche Bewertungen der Folgenabschätzungen; Datenquelle für Qualität der Optionenprüfung.
- „Have your say“-Portal der Kommission: Stellungnahmen von Verbänden und Zivilgesellschaft als Quelle für Positionen.
- Schlussfolgerungen des Rates zu Reallaboren und Experimentierklauseln (2020) und das Bundeserprobungsgesetz: Ergebnisse aus Erprobungen brauchen einen öffentlichen Ort.
- Interoperable Europe Act (2024): Interoperabilität öffentlicher Daten und Dienste; offenes Schema und ELI-Kennungen passen dazu.
- OECD-Empfehlung zu Regulatory Policy and Governance (2012) und OECD Regulatory Policy Outlook: internationaler Bezugsrahmen für Folgenabschätzung.

**Anschlussfinanzierung (zu prüfen):** europäische Programme wie CERV (Bürger, Gleichstellung, Rechte und Werte) oder Horizon Europe (Cluster 2, Demokratie und Governance), dazu Stiftungen in Deutschland und Österreich.
