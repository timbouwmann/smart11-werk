---
name: canva-magic-write-prompter
description: "Schrijft exacte Canva Magic Write instructies per tekstelement van een LinkedIn visual — headline, subline, bullets en CTA. Gebruik na de Visuele Briefing Generator om direct in Canva te kunnen werken zonder zelf te hoeven typen."
allowed-tools: Read Write
metadata:
  author: triplebird
  version: "1.0"
---

# Canva Magic Write Prompter

## Wanneer gebruiken

Gebruik deze skill wanneer je:
- Een visuele briefing hebt (bijv. van de Visuele Briefing Generator) en nu de tekst in Canva wilt laten schrijven
- Niet zelf elke tekstregel wilt typen maar Canva AI wilt gebruiken
- Variaties wilt genereren voor headline, subline of bullets

**NIET gebruiken voor:** het uitdenken van de visual zelf — gebruik eerst de Visuele Briefing Generator.

---

## Kernprincipe

CANVA MAGIC WRITE IS HET STERKST VOOR VARIATIES. GENEREER 3 OPTIES PER ELEMENT EN KIES DE BESTE. DAT GAAT SNELLER DAN ZELF HERSCHRIJVEN.

---

## Fase 1: Input verzamelen

| Input | Vraag | Default |
|-------|-------|---------|
| **Visuele briefing** | "Plak je briefing van de Visuele Briefing Generator." | Geen default — verplicht |
| **Toon** | "Zakelijk, scherp, inspirerend, nuchter?" | Direct en zakelijk |
| **Taal** | "Nederlands of Engels?" | Nederlands |

---

## Fase 2: Magic Write instructies genereren

Lever voor elk tekstelement een exacte Canva Magic Write instructie:

```
## Canva Magic Write Instructies

**Headline**
Canva Magic Write instructie:
"[Exacte instructietekst die je in Magic Write plakt]"
Doel: directe aandacht trekken, max 8 woorden, toon: [toon], taal: [taal]

**Subline**
Canva Magic Write instructie:
"[Exacte instructietekst]"
Doel: ondersteunend, max 15 woorden, contextualiseert de headline

**Bullet 1**
Canva Magic Write instructie:
"[Exacte instructietekst]"
Doel: actief geformuleerd, max 5 woorden, concreet voordeel of punt

**Bullet 2**
Canva Magic Write instructie:
"[Exacte instructietekst]"

**Bullet 3**
Canva Magic Write instructie:
"[Exacte instructietekst]"

**CTA**
Canva Magic Write instructie:
"[Exacte instructietekst]"
Doel: urgentie zonder druk, max 6 woorden
```

---

## Fase 3: Hoe gebruik je dit in Canva

```
## Stappen in Canva

1. Selecteer een tekstblok in je design
2. Klik rechtermuisknop → 'Magic Write'
   Of: Apps (linkermenu) → Magic Write
3. Plak de instructietekst uit dit document
4. Genereer 3 variaties — kies de sterkste
5. Herhaal voor elk tekstblok

Tip: gebruik Magic Write NIET voor de hook/headline als je al een sterke hebt.
Gebruik het voor de elementen waar je twijfelt of vastloopt.
```

---

## Voorbeeld output

**Input:** Briefing = vergelijkings-visual over coaches met vs. zonder videoanalyse, toon = direct en zakelijk, taal = Nederlands.

**Output:**

```
## Canva Magic Write Instructies

**Headline (linkerkant — negatief)**
Canva Magic Write instructie:
"Schrijf een korte, negatieve label voor een LinkedIn vergelijkings-visual over coaches
die geen videoanalyse gebruiken. Max 4 woorden, Nederlands, zakelijk maar scherp,
geen uitroeptekens."

**Headline (rechterkant — positief)**
Canva Magic Write instructie:
"Schrijf een korte, positieve label voor coaches die wél videoanalyse gebruiken.
Max 4 woorden, Nederlands, krachtig en direct."

**Bullet links 1**
Canva Magic Write instructie:
"Schrijf één korte bullet (max 5 woorden, Nederlands) over een nadeel van coachen
zonder data — iets wat coaches herkennen als een dagelijkse frustratie."

**Bullet rechts 1**
Canva Magic Write instructie:
"Schrijf één korte bullet (max 5 woorden, Nederlands) over een voordeel van coachen
met videoanalyse — concreet en meetbaar."

**Ondertitel**
Canva Magic Write instructie:
"Schrijf een samenvattende zin (max 10 woorden, Nederlands) die het contrast tussen
coachen met en zonder videoanalyse benoemt. Zakelijk en direct."

**CTA (voor de caption)**
Canva Magic Write instructie:
"Schrijf een zachte call-to-action voor onder een LinkedIn visual over videoanalyse
voor coaches. Max 6 woorden, Nederlands, geen opdringerige taal, geen uitroeptekens."
```

---

## Anti-patterns

- **Niet doen:** te vage instructies meegeven ("schrijf iets over marketing") — wees specifiek
- **Niet doen:** de Magic Write output direct overnemen zonder te selecteren — kies altijd de beste van 3
- **Niet doen:** Magic Write gebruiken voor de headline als je al een sterke hook hebt
- **Niet doen:** instructies schrijven zonder lengte-limiet — Canva AI neigt naar te lange teksten
- **Niet doen:** de taal weglaten in de instructie — anders schrijft Canva in het Engels
