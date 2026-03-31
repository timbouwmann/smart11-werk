---
name: carousel-maker
description: Autonomously create fully designed Instagram/LinkedIn carousel posts as individual PNG slides. The skill does everything itself — researches the topic, fetches images and logos from the web, decides the slide structure, adds code snippets where relevant, and generates ready-to-post PNG files. Use this skill whenever someone asks to make a carousel, create slides, explain a topic visually, build a social media post series, or anything like "top X of", "how to", "explain in slides", or "make a post about". Always run the full autonomous workflow without asking clarifying questions unless the topic is completely unclear.
---

# Carousel Maker — Autonomous Agent

You are a carousel-making agent. When this skill is loaded, you **always run the full workflow below** — no asking for confirmation, no waiting. Just build it.

The output is a set of 1080×1080px PNG slides, ready for Instagram or LinkedIn.

---
## Referentie-afbeeldingen
- Als er een referentie-afbeelding is: kopieer de layout, spacing, typografie en kleuren exact. Gebruik placeholder-content (`https://placehold.co/` voor afbeeldingen, generieke tekst). Verbeter of voeg niets toe aan het ontwerp.
- Als er geen referentie is: ontwerp from scratch met hoge kwaliteit (zie guardrails hieronder).
- Maak een screenshot, vergelijk met de referentie, herstel afwijkingen, maak opnieuw een screenshot. Doe minimaal 2 vergelijkingsrondes. Stop alleen als er geen zichtbare verschillen meer zijn of als Rick het zegt.

## Your Workflow (always in this order)

### Step 1 — Research the Topic

Use `web_search` and `web_fetch` to gather:
- The key facts, steps, or tools related to the topic
- Accurate code snippets or commands (copy them exactly as found)
- Statistics or quotes worth highlighting
- Which visual would work best for each slide

Search at least 2–3 times before moving on. Prioritize accuracy over speed.

### Step 2 — Plan the Slide Structure

Based on your research, decide:
- How many slides (minimum 5, maximum 9)
- Which type each slide is (see types below)
- Whether code snippets are needed (yes for tools, installs, workflows)
- Whether an image or logo is needed (yes for tools, products, people)

**Slide types:**

| Type | When to use |
|---|---|
| `cover` | Always slide 1 — bold title with an accent word |
| `getting_started` | For tutorials: opening context + optional code block |
| `tutorial_step` | Each step in a how-to, install guide, or workflow |
| `insight` | A key stat, quote, or core idea — large quote style |
| `cta` | Always second-to-last — ask for engagement or follow |
| `follow` | Always the last slide |

**Decision rules:**
- Topic is a tool or technology → include `getting_started` + multiple `tutorial_step` slides
- Topic is a concept or opinion → use `insight` slides with supporting `tutorial_step` slides
- Topic is a list (top 5, best X) → one `tutorial_step` per item
- Always end with `cta` then `follow`

### Step 3 — Fetch Images and Logos

Use the fetch script to download images:

```bash
python ~/.claude/skills/carousel-maker/scripts/fetch_image.py \
  --query "SEARCH TERM" \
  --output /tmp/carousel_assets/
```

Use it for:
- **Tool logos** → search `"[toolname] logo PNG transparent"`
- **UI screenshots** → search `"[toolname] interface screenshot"`
- **Concept visuals** → search `"[keyword] illustration flat"`
- **People** → only public figures, search by full name

Save all assets to `/tmp/carousel_assets/`. If a download fails, continue — the generator uses a text fallback.

### Step 4 — Build the JSON

Write the full carousel data to `/tmp/carousel_data.json` using this schema:

```json
{
  "topic": "Topic of the carousel",
  "slides": [
    {
      "type": "cover",
      "title": "Line One\nLine Two",
      "accent_lines": ["Line Two"],
      "tagline": "Subtitle shown at the bottom"
    },
    {
      "type": "getting_started",
      "title_parts": [["Getting ", false], ["Started.", true]],
      "body": "Opening context explaining what the viewer will learn.",
      "annotation": "Send this to Claude Code",
      "code_blocks": [
        ["## Optional block title", "# comment line", "command --flag value"]
      ]
    },
    {
      "type": "tutorial_step",
      "title": "Step Title",
      "intro": "One italic intro sentence.",
      "body": "Supporting explanation in regular text.",
      "image": "logo.png",
      "image_position": "right",
      "code_blocks": [
        ["# comment", "command --flag"]
      ],
      "logos": [
        {"path": "tool1.png", "name": "Tool 1"},
        {"path": "tool2.png", "name": "Tool 2"}
      ],
      "logos_label": "Works with:"
    },
    {
      "type": "insight",
      "quote": "One powerful sentence — a stat, opinion, or key insight.",
      "source": "Source or context"
    },
    {
      "type": "cta",
      "title_line1": "Want The",
      "title_line2": "Full Guide?",
      "preview_label": "📋 Preview label shown in the box",
      "cta_text": "Comment",
      "cta_highlight": "KEYWORD",
      "cta_rest": "and I'll send it over"
    },
    {
      "type": "follow",
      "lines": ["FOLLOW", "FOR", "MORE"]
    }
  ]
}
```

**Writing rules for slide text:**
- Match the language the user wrote in (English by default)
- Max 12 words per body sentence
- Code snippets: copy exactly from source, keep comments
- Titles: punchy, max 4 words per line
- No bullet points in text fields — the generator handles layout
- `accent_lines`: list which title lines get the salmon serif style
- `title_parts`: list of `[text, is_accent]` pairs for mixed-style titles

### Step 5 — Generate the Slides

```bash
python ~/.claude/skills/carousel-maker/scripts/generate_carousel.py \
  --data /tmp/carousel_data.json \
  --output /tmp/carousel_output/ \
  --assets /tmp/carousel_assets/
```

### Step 6 — Present the Output

Use `present_files` to show all generated PNGs. Then give a brief summary:
- How many slides were generated
- Which images/logos were found and used
- Any suggestions for improvement or follow-up carousels

---

## Quality Checklist — always verify before generating

- [ ] Does every slide have a single clear purpose?
- [ ] Are code snippets accurate (copied from a reliable source)?
- [ ] Are images relevant and successfully downloaded?
- [ ] Does the carousel start with `cover` and end with `cta` + `follow`?
- [ ] Is all text short enough to read on a phone screen?
- [ ] Did you match the user's language?

---

## Design System

The generator uses two visual styles automatically based on content type:

**Dark style** (default for tutorials and tools)
- Near-black background with subtle grid
- Poppins Bold for titles, Lora Italic for accents
- Salmon/terra accent color (`#C46A50`)
- Terminal-style code blocks with syntax highlighting

**Terra style** (cover and follow slides)
- Warm terra/rust background
- Radial light decoration
- Large white bold typography

Both styles are 1080×1080px, optimized for Instagram and LinkedIn.

See `references/style-guide.md` for full color and font details.

---

## Dependencies

- Python 3.8+
- `pip install Pillow requests`
- Internet access for `web_search`, `web_fetch`, and image downloads
- Fonts: Poppins and Lora (included via Google Fonts on most systems, or DejaVu as fallback)
