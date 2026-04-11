---
name: vergelijking-visual-designer
description: "Ontwerpt een kant-en-klare vergelijkings-visual voor LinkedIn — labels, bullets, kleuren en Canva-instructies voor het meest gedeelde format op LinkedIn. Gebruik bij contrast-content (oud vs. nieuw, fout vs. goed)."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Vergelijking Visual Designer

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Een "voor vs. na" of "fout vs. goed" visual wilt maken
- Herkenning én oplossing in één oogopslag wilt tonen
- Een visual nodig hebt die stopt met scrollen door contrast

**NIET gebruiken voor:** carrousels met meerdere slides, quote cards, of data-visuals met grafieken.

---

## Kernprincipe

CONTRAST IS HET KRACHTIGSTE VISUELE ELEMENT OP LINKEDIN. TWEE KANTEN. TWEE EMOTIES. ÉÉN BOODSCHAP.

---

## Fase 1: Input verzamelen

| Input | Vraag | Default |
|-------|-------|---------|
| **Kernboodschap** | "Wat wil je aantonen met dit contrast?" | Geen default — verplicht |
| **Linkerkant (oud/fout)** | "Wat is de slechte/oude situatie?" | Geen default — verplicht |
| **Rechterkant (nieuw/goed)** | "Wat is de betere/nieuwe situatie?" | Geen default — verplicht |
| **Doelgroep** | "Wie herkent dit contrast?" | LinkedIn-professionals |
| **Merkkleur** | "Wat is je primaire merkkleur?" | Oranje #E8560A |

**STOP: Ga niet verder zonder beide kanten van het contrast.**

---

## Fase 2: Visual uitwerken

Lever de complete vergelijkings-visual in dit formaat:

```
## Vergelijkings-Visual

**Links — [OUD/FOUT]**
Label (max 4 woorden): [Label]
Achtergrondkleur: [Negatieve kleur, bijv. #CC2200 of donkergrijs #1A1A1A]
Bullets (max 5 woorden per bullet):
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**Rechts — [NIEUW/GOED]**
Label (max 4 woorden): [Label]
Achtergrondkleur: [Positieve kleur, bijv. primaire merkkleur]
Bullets (max 5 woorden per bullet):
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**Ondertitel** (max 10 woorden)
[Zin die de boodschap samenvat]
```

---

## Fase 3: Canva-instructie

```
## In Canva

Formaat: Presentatie 1:1 (1080×1080px) — optimaal voor LinkedIn feed
Layout: 50/50 split — NOOIT een 40/60 verdeling
- Links blok: achtergrond [negatieve kleur], tekst wit
- Rechts blok: achtergrond [positieve kleur], tekst wit of donker
- Labels: text-5xl, vet, gecentreerd boven de bullets
- Bullets: text-sm, regelafstand 1.6
- Padding per blok: 24px aan alle kanten
- Ondertitel: volledig onderaan, over de volledige breedte, kleinere tekst
```

---

## Voorbeeld output

**Input:** Kernboodschap = coaches missen inzichten zonder videoanalyse, Links = zonder analyse, Rechts = met Smart11, Doelgroep = ambitieuze amateur-coaches.

**Output:**

```
## Vergelijkings-Visual

**Links — ZONDER ANALYSE**
Label: "Blind coachen"
Achtergrondkleur: #1A1A1A
Bullets:
- Gevoel stuurt beslissingen
- Dezelfde fouten herhalen
- Progressie onzichtbaar

**Rechts — MET SMART11**
Label: "Slim coachen"
Achtergrondkleur: #E8560A
Bullets:
- Data stuurt beslissingen
- Fouten snel gecorrigeerd
- Groei meetbaar per speler

**Ondertitel:** "Dit is het verschil tussen goed en beter."
```

---

## Anti-patterns

- **Niet doen:** meer dan 3 bullets per kant — te veel = te weinig contrast
- **Niet doen:** een 40/60 split in Canva — altijd gelijke blokken
- **Niet doen:** beide kanten dezelfde kleurtemperatuur geven
- **Niet doen:** de ondertitel herhalen wat al in de labels staat
- **Niet doen:** bullets schrijven die langer zijn dan 5 woorden
