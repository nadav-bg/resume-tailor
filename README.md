# Resume Tailor

Tailor a **one-page CV to any job posting** using your own AI coding agent —
Claude Code, OpenAI Codex, Google Antigravity, or Cursor. You bring the model;
this repo brings the recipe.

**No setup, no tokens, no template prep.** You drop in your real CV as
`resume.docx` and point your agent at a job posting. It reads your CV exactly as
it is, improves the wording to match the job — using only your real experience
(no invented facts) — and saves a tailored `.docx` that keeps your original
design. Works in **Hebrew and English** (RTL-safe).

## How it works

- **`WORKFLOW.md`** — the actual logic ("the magic"), written for any agent.
- **`SKILL.md`** — entry point for Claude Code (a native Skill).
- **`AGENTS.md`** — entry point for Codex / Antigravity / Cursor.
- **`cv_tools.py`** — reads your CV's exact text (`extract`) and applies the
  agent's tailored edits in place (`apply`). Standard library only; UTF-8/RTL-safe;
  handles Word's internal text-splitting automatically.

Your `resume.docx` is the design, the template, and the source of information —
all at once. The agent reads it, decides the improvements, and swaps the affected
lines. Untouched lines stay exactly as they were.

## Use it

1. Put your CV in this folder as **`resume.docx`** (your own design — any layout,
   fonts, language, RTL or LTR; it's preserved).
2. Ask your agent to tailor it, giving the posting as a **URL**, a
   **screenshot/image**, or **pasted text** — whichever is easiest:
   - Claude Code: `/resume-tailor https://company.com/careers/123`
     or `/resume-tailor path/to/job.png`
   - Codex / Antigravity / Cursor: *"Tailor my CV to this posting: <url>"*, or
     paste the description, or give a screenshot path.

The tailored `.docx` lands in `output/`, with an ATS match estimate and honest
quick-win notes.

> Note on URLs: some job boards (LinkedIn, certain ATS pages) block automated
> fetching or load via JavaScript. If a URL won't read cleanly, just paste the
> text or send a screenshot — both work the same.

## Try it first (no need for your own CV yet)

The `examples/` folder has a sample CV and a sample posting so you can see the
whole loop before using your own:

- `examples/sample_resume.docx` — a fictional one-page CV
- `examples/sample_job_posting.txt` — a matching job description

Ask your agent: *"Tailor examples/sample_resume.docx to the posting in
examples/sample_job_posting.txt."* You'll get a tailored `.docx` in `output/`,
an ATS estimate, and quick-win notes. Then swap in your own `resume.docx`.

## Install the entry point for your platform

- **Claude Code:** copy this folder to `~/.claude/skills/resume-tailor/` (available
  as the `resume-tailor` skill), or keep it as a project folder and let Claude read
  `SKILL.md`.
- **Codex / Antigravity / Cursor:** keep this folder as your working directory;
  those tools auto-read `AGENTS.md`.
- **Python 3** must be available (`cv_tools.py` uses only the standard library).

## Privacy

`resume.docx` and everything in `output/` are your personal data. The provided
`.gitignore` keeps `*.docx`, `output/`, and `replacements.json` out of git. If you
fork this repo, you can keep it public — it ships no personal data. This tool needs
no API keys; your agent platform supplies the model.
