---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through document-only responses. Can also CREATE new notebooks and add sources (URLs, files, YouTube) via the notebooklm CLI.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Wants to **create a new notebook** with sources
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"
- Says "maak een notebook", "create notebook", "nieuwe notebook"

## 🆕 Create Notebooks via CLI (notebooklm-py)

The `notebooklm` CLI tool (installed via `uv tool install notebooklm-py[browser]`) can create notebooks and add sources programmatically. Auth state lives at `~/.notebooklm/storage_state.json`.

### Create a New Notebook

```bash
# Check auth status first
notebooklm status

# If not logged in:
notebooklm login

# List existing notebooks
notebooklm list

# Create a new notebook
notebooklm create "My Notebook Title"

# Set it as active
notebooklm use NOTEBOOK_ID
```

### Add Sources to a Notebook

Source type is auto-detected (URLs, files, YouTube, inline text):

```bash
# Add a URL as source
notebooklm source add "https://example.com/article"

# Add a local file (.txt, .md)
notebooklm source add "./path/to/document.md"

# Add a YouTube video
notebooklm source add "https://youtube.com/watch?v=..."

# Add inline text with title
notebooklm source add "My notes content here" --title "Research Notes"

# Add Google Drive document
notebooklm source add-drive DRIVE_FILE_ID

# Search web and add results as sources
notebooklm source add-research "search query"

# Specify notebook explicitly (if not using active)
notebooklm source add "./file.md" -n NOTEBOOK_ID

# Wait for source to finish processing
notebooklm source wait SOURCE_ID
```

### Manage Sources

```bash
# List sources in active notebook
notebooklm source list

# Get source details
notebooklm source get SOURCE_ID

# Get full indexed text of a source
notebooklm source fulltext SOURCE_ID

# Get AI-generated summary of a source
notebooklm source guide SOURCE_ID

# Rename a source
notebooklm source rename SOURCE_ID "New Title"

# Delete a source
notebooklm source delete SOURCE_ID

# Refresh a URL/Drive source
notebooklm source refresh SOURCE_ID
```

### Generate Artifacts

```bash
# Generate various artifacts from notebook content
notebooklm generate audio          # Audio overview (podcast-style)
notebooklm generate quiz           # Quiz from content
notebooklm generate flashcards     # Flashcards
notebooklm generate report         # Written report
notebooklm generate mind-map       # Mind map
notebooklm generate slide-deck     # Presentation slides
notebooklm generate infographic    # Infographic
notebooklm generate data-table     # Data table

# Download generated artifacts
notebooklm download audio
notebooklm download report
```

### Notes Management

```bash
# Create a note in the notebook
notebooklm note create "Note content here" --title "My Note"

# List notes
notebooklm note list

# Save conversation history as a note
notebooklm history --save
```

### Full Workflow Example: Research Notebook

```bash
# 1. Create notebook
notebooklm create "AI Agents Research - March 2026"

# 2. Set as active
notebooklm use NOTEBOOK_ID

# 3. Add multiple sources
notebooklm source add "https://docs.anthropic.com/claude-code"
notebooklm source add "./research/agent-patterns.md"
notebooklm source add "https://youtube.com/watch?v=XXXXX"

# 4. Wait for processing
notebooklm source wait SOURCE_ID

# 5. Query the notebook
notebooklm ask "What are the main patterns for building AI agents?"

# 6. Generate a report
notebooklm generate report
notebooklm download report
```

### CLI vs Browser Scripts

| Feature | CLI (`notebooklm`) | Browser Scripts (`run.py`) |
|---------|--------------------|-----------------------------|
| Create notebooks | ✅ `notebooklm create` | ❌ Not supported |
| Add sources | ✅ `source add` | ❌ Not supported |
| Ask questions | ✅ `notebooklm ask` | ✅ `ask_question.py` |
| Generate artifacts | ✅ `generate audio/report/...` | ❌ Not supported |
| Library management | ❌ Use notebook_manager.py | ✅ `notebook_manager.py` |
| Auth | `notebooklm login` | `auth_manager.py setup` |

**Recommendation:** Use CLI for notebook creation and source management. Use browser scripts for querying (more reliable response extraction). After creating via CLI, register in local library with `notebook_manager.py add`.

---

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details missing, use Smart Add to discover them.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## Core Workflow

### Step 1: Check Authentication Status
```bash
python scripts/run.py auth_manager.py status
```

If not authenticated, proceed to setup.

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```

**Important:**
- Browser is VISIBLE for authentication
- Browser window opens automatically
- User must manually log in to Google
- Tell user: "A browser window will open for Google login"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# BEFORE ADDING: Ask user for metadata if unknown!
# "What does this notebook contain?"
# "What topics should I tag it with?"

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \  # REQUIRED - ASK USER IF UNKNOWN!
  --topics "topic1,topic2,topic3"  # REQUIRED - ASK USER IF UNKNOWN!

# Search notebooks by topic
python scripts/run.py notebook_manager.py search --query "keyword"

# Set active notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Quick Workflow
1. Check library: `python scripts/run.py notebook_manager.py list`
2. Ask question: `python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook if set)
python scripts/run.py ask_question.py --question "Your question here"

# Query specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required Claude Behavior:**
1. **STOP** - Do not immediately respond to user
2. **ANALYZE** - Compare answer to user's original request
3. **IDENTIFY GAPS** - Determine if more information needed
4. **ASK FOLLOW-UP** - If gaps exist, immediately ask:
   ```bash
   python scripts/run.py ask_question.py --question "Follow-up with context..."
   ```
5. **REPEAT** - Continue until information is complete
6. **SYNTHESIZE** - Combine all answers before responding to user

## Script Reference

### Authentication Management (`auth_manager.py`)
```bash
python scripts/run.py auth_manager.py setup    # Initial setup (browser visible)
python scripts/run.py auth_manager.py status   # Check authentication
python scripts/run.py auth_manager.py reauth   # Re-authenticate (browser visible)
python scripts/run.py auth_manager.py clear    # Clear authentication
```

### Notebook Management (`notebook_manager.py`)
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### Question Interface (`ask_question.py`)
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Data Cleanup (`cleanup_manager.py`)
```bash
python scripts/run.py cleanup_manager.py                    # Preview cleanup
python scripts/run.py cleanup_manager.py --confirm          # Execute cleanup
python scripts/run.py cleanup_manager.py --preserve-library # Keep notebooks
```

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Chromium browser installs automatically
- Everything isolated in skill directory

Manual setup (only if automatic fails):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Data Storage

All data stored in `~/.claude/skills/notebooklm/data/`:
- `library.json` - Notebook metadata
- `auth_info.json` - Authentication status
- `browser_state/` - Browser cookies and session

**Security:** Protected by `.gitignore`, never commit to git.

## Configuration

Optional `.env` file in skill directory:
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Decision Flow

```
User mentions NotebookLM
    ↓
What does user want?
    ├── CREATE notebook → Use CLI: notebooklm create "Title"
    │       ↓
    │   Add sources → notebooklm source add "..."
    │       ↓
    │   Register in library → python scripts/run.py notebook_manager.py add ...
    │
    ├── QUERY notebook → Check auth (browser scripts)
    │       ↓
    │   python scripts/run.py auth_manager.py status
    │       ↓
    │   If not authenticated → python scripts/run.py auth_manager.py setup
    │       ↓
    │   Check/Add notebook → python scripts/run.py notebook_manager.py list/add
    │       ↓
    │   Ask question → python scripts/run.py ask_question.py --question "..."
    │       ↓
    │   See "Is that ALL you need?" → Ask follow-ups until complete
    │       ↓
    │   Synthesize and respond to user
    │
    └── MANAGE notebooks → python scripts/run.py notebook_manager.py list/search/stats
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Authentication fails | Browser must be visible for setup! --show-browser |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook not found | Check with `notebook_manager.py list` |

## MANDATORY: Retry Until Success Policy

**NOOIT opgeven bij NotebookLM fouten. ALTIJD blijven proberen totdat het lukt.**

Wanneer `notebooklm ask`, `source add-research`, of andere commando's falen:

1. **Wacht 5-10 seconden** en probeer exact hetzelfde commando opnieuw
2. **Als het 3x faalt met dezelfde fout:** probeer een alternatieve aanpak:
   - `notebooklm ask` faalt? Probeer met `--show-browser` flag of via browser scripts
   - `source add-research` faalt? Probeer `source add` met individuele URLs
   - API fout? Probeer `notebooklm login` opnieuw en dan weer de vraag
3. **Als CLI faalt:** fallback naar browser scripts (`python3 scripts/run.py ask_question.py`)
4. **Als browser scripts falen:** probeer met `--show-browser` voor debugging
5. **Maximaal 10 pogingen** per vraag voordat je meldt dat het niet lukt
6. **NOOIT omzeilen met websearch/webfetch** als alternatief. NotebookLM is de bron.
7. **NOOIT stoppen na 1 mislukte poging.** Blijf doorgaan.

```bash
# Retry pattern voorbeeld:
notebooklm ask "vraag" || sleep 5 && notebooklm ask "vraag"
# Of via browser scripts als fallback:
cd /Users/bartboonstra/.claude/skills/notebooklm && python3 scripts/run.py ask_question.py --question "vraag"
```

## Best Practices

1. **Always use run.py** - Handles environment automatically
2. **Check auth first** - Before any operations
3. **Follow-up questions** - Don't stop at first answer
4. **Browser visible for auth** - Required for manual login
5. **Include context** - Each question is independent
6. **Synthesize answers** - Combine multiple responses
7. **Never give up** - Retry until NotebookLM responds (see Retry Policy above)

## Limitations

- No session persistence (each question = new browser, for browser scripts)
- Rate limits on free Google accounts (50 queries/day)
- Browser overhead (few seconds per question)
- CLI and browser scripts have separate auth (both need to be set up independently)

## Resources (Skill Structure)

**Important directories and files:**

- `scripts/` - All automation scripts (ask_question.py, notebook_manager.py, etc.)
- `data/` - Local storage for authentication and notebook library
- `references/` - Extended documentation:
  - `api_reference.md` - Detailed API documentation for all scripts
  - `troubleshooting.md` - Common issues and solutions
  - `usage_patterns.md` - Best practices and workflow examples
- `.venv/` - Isolated Python environment (auto-created on first run)
- `.gitignore` - Protects sensitive data from being committed
