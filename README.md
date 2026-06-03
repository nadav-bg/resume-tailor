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

2. **Prepare your template.** Take your existing CV `.docx` (or design one in
   Word), and **type tokens where tailored content should go**. Tokens look like
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

Point your agent at a job posting and ask it to tailor your CV. Examples:

- Claude Code: `/resume-tailor path/to/job.png`
- Codex / Antigravity / Cursor: *"Tailor my CV to this posting"* and paste the
  text or give a screenshot path / URL.

The output `.docx` lands in `output/`, with an ATS estimate and quick-win notes.

## Privacy

`my_cv.md`, `template.docx`, and everything in `output/` contain your personal
data. If you push this repo, keep it **private** or rely on the provided
`.gitignore` (it ignores `output/`, `*.docx`, and your filled `my_cv.md` is yours
to keep local). Never commit API keys — this tool doesn't need any; your agent
platform supplies the model.
