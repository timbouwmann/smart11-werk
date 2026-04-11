---
name: data-visual-briefer
description: "Zet cijfers en statistieken om naar een begrijpelijke LinkedIn data-visual — selecteert de 2-3 sterkste datapunten, kiest het juiste chart-type en levert een Canva-klare briefing. Gebruik bij content met getallen, onderzoeksdata of statistieken."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Data Visual Briefer

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Cijfers of statistieken wilt communiceren op LinkedIn
- Data wilt omzetten naar een visueel begrijpelijk format
- Wilt weten welke datapunten het meest overtuigend zijn voor je doelgroep

**NIET gebruiken voor:** content zonder data, vergelijkings-visuals zonder cijfers, of carrousels met meerdere datapunten per slide.

---

## Kernprincipe

ÉÉN STERK CIJFER WERKT BETER DAN VIJF ZWAKKE. SELECTEER ALTIJD HET MEEST VERRASSENDE DATAPUNT VOOR JE DOELGROEP.

---

## Fase 1: Input verzamelen

| Input | Vraag | Default |
|-------|-------|---------|
| **Data** | "Plak je cijfers, statistieken of databron." | Geen default — verplicht |
| **Kernboodschap** | "Wat wil je aantonen met deze data?" | Geen default — verplicht |
| **Doelgroep** | "Wie moet dit overtuigen?" | LinkedIn-professionals |

---

## Fase 2: Data selecteren en visualiseren

```
## Data Visual Briefing

**Geselecteerde datapunten**
1. [Meest schokkerende/verrassende datapunt] — waarom: [onderbouwing]
2. [Meest herkenbare datapunt] — waarom: [onderbouwing]
3. [Optioneel: derde punt als het de boodschap versterkt]

Geschrapte data: [Welke cijfers weggelaten zijn en waarom]

**Aanbevolen visueel format**
[Kies één]:
- Staafgrafiek — voor vergelijking van categorieën
- Percentage-vergelijking — voor twee contrasterende getallen
- Tijdlijn — voor progressie over tijd
- Scorecards — voor losse kerncijfers naast elkaar
- Procenttaart — voor aandeel van een geheel

Keuze: [Format] + onderbouwing

**Headline** (max 10 woorden)
[Plaatst het cijfer in context — dit is de zin die iemand doet stoppen]

**Subline** (max 15 woorden)
[Legt de implicatie uit — wat betekent dit voor de doelgroep?]

**Canva-instructie**
- Primaire datapunt: text-6xl, kleur [primaire merkkleur]
- Secundaire datapunt: text-4xl, kleur [secundaire kleur]
- Labels: text-sm, kleur grijs (#888888)
- Headline: vet, groot, bovenaan
- Subline: klein, onder de data
- Achtergrond: [Licht of donker] + HEX
```

---

## Fase 3: Canva-tip

```
## In Canva

Voor procentcirkels: gebruik het 'Progress Circle' element in Canva.
Vul het percentage in als waarde — Canva berekent de cirkel automatisch.

Voor scorecards: gebruik een grid van 2×1 of 3×1 blokken.
Elk blok: groot getal centraal, klein label eronder.

Stelregel: als de data op een telefoonscherm niet in 3 seconden te begrijpen is,
is er te veel informatie. Schrap meer.
```

---

## Voorbeeld output

**Input:** Data = "68% van coaches maakt geen gebruik van videoanalyse. Coaches die wél analyseren rapporteren 40% snellere spelersgroei. Gemiddeld duurt een analysesessie 47 minuten zonder tool." Kernboodschap = videoanalyse levert aantoonbaar resultaat maar wordt te weinig gebruikt.

**Output:**

```
## Data Visual Briefing

**Geselecteerde datapunten**
1. 68% gebruikt geen videoanalyse — meest schokkend: groot deel mist een bewezen voordeel
2. 40% snellere spelersgroei — meest overtuigend: direct resultaat dat coaches willen

Geschrapt: 47 minuten per sessie — dit is een bezwaar, geen voordeel. Niet geschikt voor deze visual.

**Aanbevolen format:** Percentage-vergelijking (twee grote cirkels naast elkaar)
Onderbouwing: twee contrasterende getallen, maximaal visueel contrast, snel te scannen op mobile.

**Headline:** "Meer dan de helft coach zonder bewijs."

**Subline:** "Coaches die analyseren zien 40% meer groei bij hun spelers."

**Canva-instructie**
- 68%: text-6xl, kleur #CC2200 (negatief signaal)
- 40%: text-6xl, kleur #E8560A (primaire merkkleur)
- Labels: text-sm, kleur #888888
- Achtergrond: #0D0D0D (donker voor contrast)
- Headline: Inter Bold 36px wit bovenaan
- Subline: Inter Regular 20px oranje onderaan
```

---

## Anti-patterns

- **Niet doen:** meer dan 3 datapunten in één visual — dit versnippert de boodschap
- **Niet doen:** een procenttaart gebruiken voor meer dan 2 segmenten — te complex
- **Niet doen:** de headline herhalen wat al in de data staat — voeg context toe
- **Niet doen:** kleine lettertypes gebruiken voor de kerngetallen — die moeten groot
- **Niet doen:** data presenteren zonder de implicatie te benoemen in de subline
