# NotebookLM Skill voor Claude Code - Installatie

Query je Google NotebookLM notebooks direct vanuit Claude Code. Krijg source-grounded antwoorden van Gemini, gebaseerd op alleen jouw documenten. Geen hallucinaties, alleen feiten uit je bronnen.

## Wat kan deze skill?

- Notebooks aanmaken en beheren vanuit Claude Code
- Bronnen toevoegen (URLs, bestanden, YouTube videos, Google Drive docs)
- Vragen stellen aan je notebooks en antwoorden krijgen met citaties
- Audio overviews, quizzen, rapporten en meer genereren
- Volledige notebook library management

## Installatie (2 minuten)

### Stap 1: Download alle bestanden

Download deze hele map en zet de inhoud in:

```
~/.claude/skills/notebooklm/
```

Dus de structuur wordt:

```
~/.claude/skills/notebooklm/
  SKILL.md              ← De skill definitie (VERPLICHT)
  requirements.txt      ← Python dependencies
  .gitignore            ← Beschermt je auth data
  scripts/
    __init__.py
    run.py              ← De wrapper die alles automatisch opzet
    ask_question.py     ← Vragen stellen aan notebooks
    auth_manager.py     ← Authenticatie beheer
    browser_session.py  ← Browser sessie management
    browser_utils.py    ← Browser hulpfuncties
    cleanup_manager.py  ← Opruimen van data
    config.py           ← Configuratie
    notebook_manager.py ← Notebook library beheer
    setup_environment.py← Automatische omgeving setup
  references/
    api_reference.md    ← Uitgebreide API documentatie
    troubleshooting.md  ← Veelvoorkomende problemen + oplossingen
    usage_patterns.md   ← Best practices en workflows
```

### Stap 2: Installeer de CLI tool (optioneel maar aanbevolen)

```bash
uv tool install notebooklm-py[browser]
```

### Stap 3: Authenticeer

Open Claude Code en zeg:

```
Check mijn NotebookLM authenticatie status
```

Claude zal je door de setup leiden. Er opent een browser voor Google login.

### Stap 4: Klaar!

Gebruik het door te zeggen:

- "Stel een vraag aan mijn NotebookLM over [onderwerp]"
- "Maak een nieuwe notebook aan met de titel [naam]"
- "Voeg deze URL toe als bron aan mijn notebook"
- "Welke notebooks heb ik?"

## Vereisten

- Claude Code
- Python 3.10+
- Google account met NotebookLM toegang
- `uv` package manager (aanbevolen) of `pip`

## Meer info

Bekijk de bestanden in de `references/` map voor:
- Volledige API documentatie
- Troubleshooting guide
- Workflow voorbeelden en best practices
