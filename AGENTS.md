# AGENTS.md — Resume Tailor

This repository is a **resume-tailoring tool** driven by an AI coding agent
(OpenAI Codex, Google Antigravity, Cursor, Claude Code, etc.).

When the user asks you to **tailor / customize / generate a CV or resume** for a
job posting, follow the complete recipe in **`WORKFLOW.md`** in this folder.

Inputs:
- **Job posting** — the user gives a URL, a screenshot/image path, or pasted text.
  If they haven't, ask for it. For a URL, fetch and read the page; if it's blocked
  or JS-only, ask for a paste or screenshot.
- **`resume.docx`** — the user's real CV, as-is. It is the ONLY source of truth
  AND the design/template. Never invent roles, dates, numbers, or skills.

Steps (see `WORKFLOW.md` for detail):
1. `python cv_tools.py extract --doc resume.docx` → exact paragraph strings.
2. Decide tailored replacements drawn only from the user's real content.
3. Write `replacements.json` — a list of `{"find": "...", "replace": "..."}` where
   each `find` is copied **verbatim** from step 1.
4. Build:
   ```bash
   python cv_tools.py apply --doc resume.docx --output "output/CV_<Company>_<Role>.docx" --replacements replacements.json
   ```

Rules: one page; mirror the posting's keywords using only real content; produce
the CV in the posting's language (Hebrew or English) with correct RTL and no ASCII
substitution; preserve the original design (only text is replaced). Finish with an
ATS match estimate and honest quick-win suggestions.
