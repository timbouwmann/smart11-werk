---
name: figma-briefing-schrijver
description: "Schrijft een volledige technische Figma-briefing voor een LinkedIn visual — frame-structuur, typografie, kleurgebruik, spacing en Auto Layout regels. Gebruik wanneer je een designer of Figma Auto Layout wilt briefen zonder eindeloos heen-en-weer."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Figma Briefing Schrijver

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Een designer wilt briefen voor een LinkedIn visual in Figma
- Zelf werkt in Figma en exacte specs nodig hebt
- Herbruikbare Figma-componenten wilt bouwen voor consistente LinkedIn content

**NIET gebruiken voor:** Canva-designs (gebruik daarvoor de Canva Magic Write Prompter), of als je nog geen visuele briefing hebt (gebruik eerst de Visuele Briefing Generator).

---

## Kernprincipe

ÉÉN CLAUDE OUTPUT = COMPLETE BRIEFING. GEEN HEEN-EN-WEER. GEEN AANNAMES. ALLES WAT EEN DESIGNER NODIG HEEFT STAAT ER IN.

---

## Fase 1: Input verzamelen

| Input | Vraag | Default |
|-------|-------|---------|
| **Visuele briefing** | "Plak je briefing van de Visuele Briefing Generator." | Geen default — verplicht |
| **Kleurenpalet** | "Wat zijn je merkkleuren? (HEX-codes)" | #0D0D0D, #E8560A, #FFFFFF |
| **Beschikbare fonts** | "Welke fonts gebruik je?" | Inter voor body, geen header-font opgegeven |
| **Platform** | "Voor welk platform?" | LinkedIn feed post (1080×1080px) |

---

## Fase 2: Figma-briefing genereren

Lever de volledige technische spec in dit formaat:

```
## Figma Briefing — LinkedIn Visual

**Frame**
Afmeting: [breedte]×[hoogte]px
Achtergrond: [HEX]
Platform: LinkedIn feed post

**Layer-structuur**
Layer 1 — [Naam element]:
  Type: [Text / Rectangle / Image / Icon]
  Inhoud: [Tekst of beschrijving]
  Font: [Familienaam] [Weight], [size]px
  Kleur: [HEX]
  Line-height: [waarde]
  Letter-spacing: [waarde]em

Layer 2 — [Naam element]:
  [zelfde structuur]

[Herhaal voor alle layers]

**Spacing**
Padding frame (alle kanten): [n]px
Gap tussen lagen: [n]px
Interne padding tekstblokken: [n]px

**Auto Layout**
Richting: [Vertical / Horizontal]
Sizing: [Fill container / Hug contents / Fixed]
Uitlijning: [Left / Center / Right]
Wrap: [Aan / Uit]

**Component-instructie**
[Optioneel: hoe dit frame als component opslaan voor hergebruik]
```

---

## Fase 3: Figma-tip

```
## In Figma

1. Maak één master frame aan op basis van deze specs
2. Gebruik 'Publish as component' (rechtermuisknop → Create component)
3. Dupliceer vanuit de component library voor elke nieuwe visual
4. Gebruik Auto Layout zodat de structuur automatisch meeschaalt bij tekstwijzigingen
5. Sla kleurstijlen op als Local Styles zodat je merkkleur altijd consistent is
```

---

## Voorbeeld output

**Input:** Briefing = vergelijkings-visual coaches met/zonder videoanalyse, kleuren = #0D0D0D + #E8560A + #FFFFFF, fonts = Inter, platform = LinkedIn.

**Output:**

```
## Figma Briefing — LinkedIn Visual

**Frame**
Afmeting: 1080×1080px
Achtergrond: #0D0D0D
Platform: LinkedIn feed post

**Layer-structuur**

Layer 1 — Headline:
  Type: Text
  Inhoud: "Blind coachen vs. Slim coachen"
  Font: Inter Bold, 52px
  Kleur: #FFFFFF
  Line-height: 1.1
  Letter-spacing: -0.02em

Layer 2 — Linker blok (negatief):
  Type: Rectangle
  Afmeting: 492×600px
  Achtergrond: #1A1A1A
  Padding: 32px alle kanten

  Layer 2a — Label links:
    Type: Text
    Inhoud: "Blind coachen"
    Font: Inter Bold, 36px
    Kleur: #CC2200

  Layer 2b — Bullets links:
    Type: Text (elk bullet apart als Text Layer)
    Font: Inter Regular, 20px
    Kleur: #AAAAAA
    Line-height: 1.6

Layer 3 — Rechter blok (positief):
  Type: Rectangle
  Afmeting: 492×600px
  Achtergrond: #E8560A
  Padding: 32px alle kanten

  Layer 3a — Label rechts:
    Type: Text
    Inhoud: "Slim coachen"
    Font: Inter Bold, 36px
    Kleur: #FFFFFF

  Layer 3b — Bullets rechts:
    Font: Inter Regular, 20px
    Kleur: #FFFFFF
    Line-height: 1.6

Layer 4 — Ondertitel:
  Type: Text
  Inhoud: "Dit is het verschil tussen goed en beter."
  Font: Inter Regular, 22px
  Kleur: #888888
  Positie: Onderaan, volledig breedte, gecentreerd

**Spacing**
Padding frame: 64px alle kanten
Gap tussen linker en rechter blok: 0px (aansluitend)
Gap tussen label en bullets in blok: 16px

**Auto Layout**
Frame: Vertical, fill container
Blokken: Horizontal, fixed width 492px
Bullets: Vertical, hug contents, gap 8px

**Component-instructie**
Sla op als component 'LinkedIn-VergelijkingVisual'. Maak twee varianten:
- Variant A: donkere achtergrond links, oranje rechts
- Variant B: omgedraaid (voor toekomstige variaties)
```

---

## Anti-patterns

- **Niet doen:** layer-namen weglaten of generiek houden ("Rectangle 1") — benoem wat het is
- **Niet doen:** pixel-waarden raden — gebruik exact de waarden uit de briefing
- **Niet doen:** Auto Layout weglaten als het frame hergebruikt moet worden
- **Niet doen:** de component-instructie overslaan als het merk vaker LinkedIn-content maakt
- **Niet doen:** verschillende font-weights door elkaar gebruiken zonder hiërarchie
