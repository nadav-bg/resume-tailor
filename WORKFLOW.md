# Resume Tailoring — Agent Workflow

You are tailoring a **one-page CV** to a specific job posting. The user runs you
inside an AI coding agent (Claude Code, OpenAI Codex, Google Antigravity, Cursor,
etc.). This file is the recipe; the intelligence is you.

This workflow is **generic** — it works for any user, in **Hebrew or English**.
All of the user's real CV content lives in `my_cv.md`. The template they want to
fill lives in `template.docx` with `{{TOKEN}}` placeholders. You never invent
facts — you only re-tailor what is already in `my_cv.md`.

---

## CRITICAL RULES — READ FIRST

1. **NO HALLUCINATIONS.** Every word in the CV must come from `my_cv.md`. Do not
   invent roles, employers, dates, numbers, skills, or achievements.
2. **ONE PAGE ONLY.** If content would overflow, shorten or drop the least
   relevant bullets — never pad.
3. **MIRROR THE JOB LANGUAGE.** Reorder, rephrase, and emphasize the user's real
   content to match the posting's vocabulary, seniority, and values.
4. **MATCH THE POSTING'S LANGUAGE.** If the job posting is in Hebrew, produce the
   CV in Hebrew (and keep it RTL-correct). If English, English. Never substitute
   accented/Hebrew characters with ASCII look-alikes.
5. **PRESERVE THE TEMPLATE.** You only fill tokens; the template's design, fonts,
   and direction stay as the user built them.

---

## STEP 0 — Locate inputs

- **Baseline data:** read `my_cv.md` (the user's real CV — the only source of truth).
- **Template:** `template.docx` in this folder, tokenized with `{{...}}` placeholders.
  If it is missing or has no tokens, tell the user to read `README.md` ("Prepare
  your template") and stop.
- **Job posting:** provided by the user as a screenshot path, a pasted text, or a
  URL. If nothing was provided, ask: *"Paste the job posting text, or give me the
  path to a screenshot of it."*

## STEP 1 — Read the job posting

Extract:
- Company name and role title (for the output filename)
- Top 5–8 required skills / keywords
- Key responsibilities
- Tone and values (startup vs. corporate, mission-driven vs. commercial)
- **Language** of the posting (Hebrew / English)

## STEP 2 — Load the user's baseline

Read `my_cv.md` fully. Note which sections exist (profile, roles, skills,
education, etc.) and which tokens the template exposes (open `template.docx`'s
tokens — they look like `{{PROFILE_1}}`, `{{ROLE1_BULLET_1}}`, `{{SKILL_1}}`,
`{{NAME}}`, …). The token names are the contract between you and the template.

## STEP 3 — Tailor

For each token the template exposes, choose and rewrite the best-matching real
content from `my_cv.md`:
- **Profile:** rewrite to foreground what the posting asks for first.
- **Role bullets:** select the most relevant real bullets; rephrase to mirror the
  posting's verbs and metrics. Keep all numbers truthful.
- **Skills:** reorder/select from the user's real skills to surface the posting's
  keywords. Do not add skills the user doesn't have.
- **Contact / name / education:** copy verbatim from `my_cv.md`.

If the posting is Hebrew, write every tailored value in fluent Hebrew.

## STEP 4 — Write content.json

Produce a `content.json` mapping **every** token in the template to its tailored
string. Example:

```json
{
  "NAME": "Jane Doe",
  "PROFILE_1": "...",
  "PROFILE_2": "...",
  "ROLE1_BULLET_1": "...",
  "ROLE1_BULLET_2": "...",
  "SKILL_1": "Strategic Thinking",
  "SKILL_2": "..."
}
```

Set a token to `""` to blank a slot you intentionally leave empty (e.g. an unused
6th bullet). Keep total content to one page.

## STEP 5 — Build the document

Run:

```bash
python build_cv.py \
  --template template.docx \
  --output "output/CV_<Company>_<Role>.docx" \
  --content content.json
```

The script fills the tokens (run-split-safe, UTF-8/RTL-safe) and writes the
`.docx`. Read its stderr: if it reports tokens "left in place," you missed them
in `content.json` — fix and re-run.

> No `.docx` template, or want to generate from scratch instead of filling one?
> You may instead build the file directly with `python-docx`, taking content
> only from `my_cv.md`. The token-template path is preferred because it preserves
> the user's design.

## STEP 6 — Report

Tell the user:
- Where the file was saved.
- An **ATS match estimate** (0–100): roughly how well the tailored CV covers the
  posting's keywords/requirements, based only on the user's real content.
- **Quick wins:** 2–4 concrete, honest suggestions (e.g. "the posting stresses
  budget ownership — your 18M figure is buried in bullet 4; I moved it up" or
  "they want SQL; you don't list it, so I left it out — add it to `my_cv.md` if
  you have it").

Never raise the ATS score by inventing content.
