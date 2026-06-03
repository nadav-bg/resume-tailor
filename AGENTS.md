# AGENTS.md — Resume Tailor

This repository is a **resume-tailoring tool** driven by an AI coding agent
(OpenAI Codex, Google Antigravity, Cursor, Claude Code, etc.).

When the user asks you to **tailor / customize / generate a CV or resume** for a
job posting, follow the complete recipe in **`WORKFLOW.md`** in this folder.

Inputs:
- **Job posting** — the user gives a screenshot path, pasted text, or URL. If they
  haven't, ask for it.
- **`my_cv.md`** — the user's real CV content. This is the ONLY source of truth.
  Never invent roles, dates, numbers, or skills.
- **`template.docx`** — the Word template, tokenized with `{{...}}` placeholders.

Build step:
```bash
python build_cv.py --template template.docx --output "output/CV_<Company>_<Role>.docx" --content content.json
```

Rules: one page only; mirror the posting's keywords using only real content;
produce the CV in the posting's language (Hebrew or English) with correct RTL and
no ASCII substitution of accented/Hebrew characters. See `WORKFLOW.md` for the
full step-by-step, including the ATS estimate and quick-win report.

First-time setup (template tokenizing, `my_cv.md`) is described in `README.md`.
