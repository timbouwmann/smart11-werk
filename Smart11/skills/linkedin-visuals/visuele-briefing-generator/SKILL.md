---
name: visuele-briefing-generator
description: "Genereert een complete visuele briefing voor een LinkedIn visual — hook, hoofdboodschap, layout-type, tekst-hiërarchie, kleurtemperatuur en CTA. Gebruik dit vóór je Canva of Figma opent."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Visuele Briefing Generator

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Een LinkedIn visual wilt maken maar nog geen plan hebt
- Wilt weten welk visueel format het beste past bij je boodschap
- Een Canva-klare briefing nodig hebt voordat je begint te designen

**NIET gebruiken voor:** het bouwen van de visual zelf, het schrijven van een caption, of het maken van een carrousel (gebruik daarvoor de Carrousel Architect skill).

---

## Kernprincipe

CLAUDE DENKT DE VISUAL UIT — JIJ BOUWT WAT CLAUDE BEDACHT HEEFT. NIET ANDERSOM.

---

## Fase 1: Input verzamelen

Vraag de gebruiker om de volgende informatie. Als iets ontbreekt, gebruik de default.

| Input | Vraag | Default |
|-------|-------|---------|
| **Onderwerp** | "Waar gaat de visual over?" | Geen default — verplicht |
| **Doelgroep** | "Wie moet dit zien?" | Ambitieuze professionals op LinkedIn |
| **Kernboodschap** | "Wat moet de kijker onthouden? (1 zin)" | Geen default — verplicht |
| **Post-type** | "Single image, carrousel of quote card?" | Single image |
| **Toon van het merk** | "Zakelijk, scherp, inspirerend, nuchter?" | Zakelijk maar direct |

**STOP: Ga niet verder zonder onderwerp én kernboodschap.**

---

## Fase 2: Briefing genereren

Lever de complete visuele briefing in dit formaat:

```
## Visuele Briefing

**Hook** (max 8 woorden)
[De eerste zin of het eerste element dat iemand doet stoppen]

**Hoofdboodschap** (max 12 woorden)
[Wat de kijker moet onthouden]

**Aanbevolen layout-type**
[Vergelijking / Stappen / Quote / Data / Lijst]
Onderbouwing: [Waarom dit format past bij deze boodschap]

**Tekst-hiërarchie**
- Centraal (groot): [Wat de meeste aandacht krijgt]
- Ondersteunend (klein): [Wat de context geeft]
- Verwijderen: [Wat afleidt van de kernboodschap]

**Kleurtemperatuur**
[Warm / Koel / Hoog contrast / Neutraal]
Onderbouwing: [Waarom deze keuze past bij de emotie van de boodschap]

**Caption CTA**
[Eén concrete call-to-action voor in de caption]
```

---

## Fase 3: Canva-instructie

Sluit altijd af met een concrete Canva-instructie:

```
## In Canva

1. Open Canva → selecteer [aanbevolen formaat, bijv. LinkedIn Post 1080×1080]
2. Gebruik de tekst-hiërarchie uit de briefing als structuur
3. Pas alleen de tekst aan — niet de layout (die is al bepaald)
4. Kleur: gebruik [primaire kleur] voor het centrale element, [secundaire kleur] voor ondersteuning
```

---

## Voorbeeld output

**Input:** Onderwerp = videoanalyse voor coaches, Doelgroep = ambitieuze amateur-coaches, Kernboodschap = coaches verliezen waardevolle inzichten omdat ze video's niet analyseren, Post-type = single image.

**Output:**

```
## Visuele Briefing

**Hook:** "Je verliest de helft na elk duel."

**Hoofdboodschap:** "Coaches die video analyseren winnen meer. Data bewijst het."

**Layout:** Vergelijking (links: zonder analyse / rechts: met analyse)
Onderbouwing: contrast is het krachtigste visuele element op LinkedIn — herkenning + oplossing in één oogopslag.

**Tekst-hiërarchie**
- Centraal: de twee labels ("Zonder analyse" / "Met analyse")
- Ondersteunend: 2-3 bullets per kant met concrete gevolgen
- Verwijderen: percentages en statistieken — te veel details voor een single image

**Kleurtemperatuur:** Hoog contrast — donker links (verlies), licht/oranje rechts (winst)
Onderbouwing: emotioneel contrast versterkt de boodschap visueel

**Caption CTA:** "Comment ANALYSE als je wil weten hoe dit werkt."
```

---

## Anti-patterns

- **Niet doen:** drie kernboodschappen meegeven. Eén boodschap, één visual.
- **Niet doen:** de hook en hoofdboodschap hetzelfde maken. De hook stopt de scroll, de hoofdboodschap geeft de betekenis.
- **Niet doen:** een layout kiezen die niet past bij de boodschap (bijv. een quote card voor stappenplan-content).
- **Niet doen:** beginnen met bouwen zonder goedkeuring van de briefing.
