# Resume Tailor

Tailor a **one-page CV to any job posting** using your own AI coding agent —
Claude Code, OpenAI Codex, Google Antigravity, or Cursor. You bring the model;
this repo brings the recipe.

It pulls **only from your real CV** (no hallucinated experience), mirrors the
posting's language and keywords, fills your designed Word template, and gives you
an ATS match estimate. Works in **Hebrew and English** (RTL-safe).

## How it works

- **`WORKFLOW.md`** — the actual logic ("the magic"), written for any agent.
- **`SKILL.md`** — entry point for Claude Code (a native Skill).
- **`AGENTS.md`** — entry point for Codex / Antigravity / Cursor.
- **`my_cv.md`** — *you* fill this with your real career data (source of truth).
- **`template.docx`** — *you* provide this: your Word CV with `{{TOKEN}}` slots.
- **`build_cv.py`** — fills the template's tokens, language/RTL-safe.

The agent reads the posting, tailors your content, writes `content.json`, and runs
`build_cv.py` to produce the final `.docx`.

## One-time setup

1. **Add your data.** Open `my_cv.md` and replace the placeholders with your real
   profile, roles, bullets, skills, and education. Be thorough — the agent picks
   the most relevant parts per job.

2. **Prepare your template — your own design.** Use *your* existing CV `.docx`
   (any layout, fonts, colors, Hebrew/RTL or English/LTR — all preserved) or design
   a fresh one in Word. **Type tokens where tailored content should go.** Tokens
   look like
   `{{NAME}}`, `{{PROFILE_1}}`, `{{ROLE1_BULLET_1}}`, `{{SKILL_1}}`. Save it as
   `template.docx` in this folder.
   - Tip: type each token in one go so Word keeps it intact (the builder also
     handles tokens Word splits internally, but clean tokens are safest).
   - Use any token names you like — just make sure the agent fills the same ones.
   - For a Hebrew CV, build the template in Hebrew/RTL as usual; the tool only
     replaces token text and leaves your direction and styling untouched.

3. **Install the entry point for your platform:**
   - **Claude Code:** copy this folder into `~/.claude/skills/resume-tailor/`
     (it'll be available as the `resume-tailor` skill), or keep it as a project
     folder and let Claude read `SKILL.md`.
   - **Codex / Antigravity / Cursor:** keep this folder as your working directory;
     those tools auto-read `AGENTS.md`.

4. **Python:** ensure Python 3 is available (`build_cv.py` uses only the standard
   library — no install needed). The optional "generate from scratch" path in
   WORKFLOW.md uses `python-docx` (`pip install python-docx`).

## Use it

Point your agent at a job posting and ask it to tailor your CV. The posting can be
a **URL**, a **screenshot/image**, or **pasted text** — whichever is easiest:

- Claude Code: `/resume-tailor https://company.com/careers/123`
  or `/resume-tailor path/to/job.png`
- Codex / Antigravity / Cursor: *"Tailor my CV to this posting: <url>"*, or paste
  the description text, or give a screenshot path.

The output `.docx` lands in `output/`, with an ATS estimate and quick-win notes.

## Privacy

`my_cv.md`, `template.docx`, and everything in `output/` contain your personal
data. If you push this repo, keep it **private** or rely on the provided
`.gitignore` (it ignores `output/`, `*.docx`, and your filled `my_cv.md` is yours
to keep local). Never commit API keys — this tool doesn't need any; your agent
platform supplies the model.
