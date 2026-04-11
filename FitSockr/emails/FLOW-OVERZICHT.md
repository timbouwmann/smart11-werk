# FitSockr — Welkomstflow Overzicht

## Flow trigger
Iemand vult zijn e-mailadres in (opt-in) + selecteert zijn sport.

---

## E-mails in de flow

| # | Bestand | Onderwerp | Verzendtijd |
|---|---------|-----------|-------------|
| 1 | `email-1-welkom-korting.html` | Je 15% korting staat klaar 👊 | Direct na opt-in |
| 2 | `email-2-verhaal.html` | Dit is waarom FitSockr bestaat | Dag 2 |
| 3 | `email-3-social-proof.html` | Martijn Kaars. Marco Bizot. En jij? | Dag 3 |
| 4 | `email-4-sport-benefits.html` | [Sport-specifiek — zie hieronder] | Dag 4 |
| 5 | `email-5-multibundle.html` | Slim gesport: haal meer uit je FitSockr | Dag 5 |
| 6 | `email-6-faq.html` | Twijfels? Dit zijn de antwoorden 👇 | Dag 7 |
| 7 | `email-7-urgentie.html` | ⏳ Je korting verloopt over 24 uur | Dag 8 |

---

## Sport-specifieke onderwerpregels (email 4)

| Sport | Onderwerp | Preheader |
|-------|-----------|-----------|
| Voetbal | Geen speling meer in je schoen op het veld | Dit is wat profs weten. |
| Padel | Snelheid zonder controle is geen voordeel | Stop met glijden in je schoen. |
| Fitness/HYROX | Elke beweging begint bij je voeten | Waarom serieuze trainers gripsokken dragen. |
| Pilates | Grip en stabiliteit op elke reformer | Minder nadenken. Meer voelen. |

---

## Klaviyo variabelen

| Variabele | Gebruik |
|-----------|---------|
| `{{ first_name }}` | Voornaam ontvanger (niet gebruikt in huidige tekst — optioneel toe te voegen) |
| `{{ discount_code }}` | De unieke kortingscode per profiel |
| `{{ unsubscribe_url }}` | Uitschrijflink (verplicht door Klaviyo) |
| `sport` | Profieleigenschap — waarden: `voetbal`, `padel`, `fitness`, `hyrox`, `pilates` |

---

## Klaviyo conditional logica (sport-blokken)

In emails 1, 4 en 5 staan sport-specifieke blokken. Gebruik Klaviyo's template taal:

```
{% if sport == 'voetbal' %}
  ...voetbal inhoud...
{% endif %}

{% if sport == 'padel' %}
  ...padel inhoud...
{% endif %}

{% if sport == 'fitness' or sport == 'hyrox' %}
  ...fitness inhoud...
{% endif %}

{% if sport == 'pilates' %}
  ...pilates inhoud...
{% endif %}
```

---

## Conversie-verbeteringen t.o.v. origineel concept

1. **Kortingscode visueel prominenter** — grote monospace weergave in een opvallend kader
2. **Sterkere subjectlines** — specifiek, niet generiek ("Martijn Kaars. Marco Bizot. En jij?")
3. **Preheaders toegevoegd** — verhogen open rate (ontbrak in origineel)
4. **Besparingen zichtbaar** — doorgestreepte prijzen in bundle-email tonen echte waarde
5. **"Meest gekozen" badge** — op 3-paar deal stuurt richting hogere orderwaarde
6. **Urgentie email** — kortingscode duidelijk herhaald + CTA groter
7. **Consistente discount reminder** — code terug in footer van elk e-mail
8. **Één CTA per mail** — nooit twee verschillende knoppen
