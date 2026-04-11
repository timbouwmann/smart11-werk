---
name: quote-card-creator
description: "Destilleert de krachtigste quote uit een tekst of idee en maakt er een kant-en-klare LinkedIn quote card van — inclusief visueel concept, typografie en Canva-instructie. Quote cards worden 3x vaker gedeeld dan informatieve posts."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Quote Card Creator

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Een sterke uitspraak visueel wilt maken voor LinkedIn
- Een blogpost, speech of idee wilt destilleren naar één krachtige zin
- Content wilt maken die mensen delen omdat het zegt wat zij voelden maar nooit verwoordden

**NIET gebruiken voor:** informatieve posts met meerdere punten, stappen-content, of vergelijkings-visuals.

---

## Kernprincipe

EEN QUOTE CARD WERKT ALS DE LEZER DENKT: "DAT IS PRECIES WAT IK VOELDE, MAAR IK HAD HET NOOIT ZO KUNNEN ZEGGEN."

---

## Fase 1: Input verzamelen

| Input | Vraag | Default |
|-------|-------|---------|
| **Ruwe tekst of idee** | "Plak je tekst of beschrijf je gedachte." | Geen default — verplicht |
| **Toon** | "Hoe wil je klinken? Scherp, inspirerend, nuchter, provocatief?" | Direct en eerlijk |
| **Doelgroep** | "Wie moet dit raken?" | LinkedIn-professionals |

---

## Fase 2: Quote uitwerken

Lever altijd twee versies én het visuele concept:

```
## Quote Card

**Quote — volledige versie** (max 15 woorden)
[Herschreven voor maximale impact. Geen vakjargon. Directe taal.]

**Quote — korte versie** (max 8 woorden)
[Voor bold typografie. De essentie in zo min mogelijk woorden.]

**Contextzin** (max 20 woorden)
[De zin die de quote ondersteunt en de implicatie uitlegt. Staat klein onder de quote.]

**Visueel concept**
- Achtergrond: [Donker (#0D0D0D) of licht (#F5F5F5)] + onderbouwing
- Quote: [Kleur + lettertype-instructie]
- Contextzin: [Kleur + grootte]
- Grafisch element: [Diagonale lijn / accent kleur / geen]

**Canva-instructie**
- Formaat: 1080×1080px
- Quote (lange versie): [Font] Bold, [grootte]px, kleur [HEX]
- Quote (korte versie): [Font] Bold Condensed, [grootte]px
- Contextzin: [Font] Regular, [grootte]px, kleur [HEX]
- Uitlijning: Links of gecentreerd
```

---

## Fase 3: Canva-tip

```
## In Canva

Gebruik een condensed font (bijv. Bebas Neue of Anton) voor de korte versie — dit geeft
de bold typografie die nodig is voor scroll-stop effect.

Tekst op donkere achtergrond converteert beter op mobile — gebruik dit als default
tenzij je merkstijl expliciet licht is.

Stap: maak eerst de korte versie af (bold, groot). Voeg dan de lange versie toe als
tweede optie op dezelfde slide — zo heb je twee posts klaar in één keer.
```

---

## Voorbeeld output

**Input:** "Coaches denken dat ze weten wat er in de wedstrijd gebeurde. Maar het menselijk geheugen is slecht. Videoanalyse laat zien wat echt was."

**Output:**

```
## Quote Card

**Quote — volledige versie**
"Je herinnert je de wedstrijd niet. Je herinnert je wat je voelde."

**Quote — korte versie**
"Je herinnert je wat je voelde."

**Contextzin**
"Videoanalyse laat zien wat er écht was. Niet wat je denkt dat er was."

**Visueel concept**
- Achtergrond: Donker (#0D0D0D) — creëert focus en werkt goed op mobile
- Quote: Wit (#FFFFFF), bold, groot centraal
- Contextzin: Oranje (#E8560A), small, onderaan
- Grafisch element: Subtiele diagonale lijn links als accentkleur

**Canva-instructie**
- Formaat: 1080×1080px
- Quote lang: Inter Bold, 52px, kleur #FFFFFF, line-height 1.2
- Quote kort: Bebas Neue, 96px, kleur #FFFFFF
- Contextzin: Inter Regular, 22px, kleur #E8560A
- Uitlijning: Links uitgelijnd, 64px padding
```

---

## Anti-patterns

- **Niet doen:** een quote langer maken dan 15 woorden — elke extra zin verzwakt de impact
- **Niet doen:** vakjargon of merknamen in de quote — het moet universeel aanvoelen
- **Niet doen:** de contextzin weglaten — zonder context mist de quote haar betekenis
- **Niet doen:** lichte achtergrond gebruiken als de quote provocatief is — donker versterkt de toon
- **Niet doen:** meer dan één grafisch accent gebruiken — eenvoud wint
