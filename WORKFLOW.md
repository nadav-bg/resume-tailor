# Resume Tailoring — Agent Workflow

You are tailoring a **one-page CV** to a specific job posting. The user runs you
inside an AI coding agent (Claude Code, OpenAI Codex, Google Antigravity, Cursor,
etc.). This file is the recipe; the intelligence is you.

**Zero setup for the user.** They drop in their real CV as `resume.docx`. That one
file is the design, the template, AND the only source of information about them.
You read its exact text, decide what to improve for this job, and swap the
original lines for tailored ones — preserving their design, fonts, and direction
(Hebrew/RTL included). You never invent facts.

---

## CRITICAL RULES — READ FIRST

1. **NO HALLUCINATIONS.** Every word must come from the user's `resume.docx`
   (plus anything they explicitly tell you). Never invent roles, employers, dates,
   numbers, or skills. You may rephrase, reorder, and trim — not fabricate.
2. **ONE PAGE.** Keep it to one page. If it's already one page, keep it that way.
3. **MIRROR THE JOB LANGUAGE.** Rephrase the user's real lines to match the
   posting's vocabulary, seniority, and values.
4. **MATCH THE POSTING'S LANGUAGE.** Hebrew posting → Hebrew CV (RTL-correct);
   English → English. Never replace accented/Hebrew characters with ASCII.
5. **PRESERVE THE DESIGN.** You only replace text content. Layout, fonts, colors,
   and direction stay exactly as the user built them.

---

## STEP 0 — Locate inputs

- **CV:** `resume.docx` in this folder. If missing, tell the user to drop their
  Word CV in as `resume.docx` and stop.
- **Job posting:** provided by the user as a URL, a screenshot/image path, or
  pasted text. If nothing was provided, ask:
  *"Give me the job posting — a URL, a screenshot path, or just paste the text."*

## STEP 1 — Read the job posting

Accept any of three forms:
- **URL** → fetch the page (WebFetch / your platform's web tool) and read its text.
  If it's blocked or JS-only/login-walled and returns junk, ask the user to paste
  the text or send a screenshot instead.
- **Screenshot / image path** → read the image directly.
- **Pasted text** → use as-is.

Extract: company name, role title, top 5–8 required skills/keywords, key
responsibilities, tone/values, and the **language** of the posting.

## STEP 2 — Read the CV exactly

Run:

```bash
python cv_tools.py extract --doc resume.docx
```

This prints a JSON array of the CV's paragraphs — the **exact** strings as they
appear in the document (split runs reassembled). These exact strings are what you
must use as `find` values in the next step. Study them: identify the profile/
summary lines, each role's bullets, the skills line(s), contact, education.

## STEP 3 — Tailor

Decide, for each line worth changing, a tailored replacement drawn only from the
user's real content:
- **Profile/summary:** rewrite to foreground what the posting asks for first.
- **Role bullets:** rephrase to mirror the posting's verbs and priorities; keep
  every number truthful. Surface the most relevant bullets.
- **Skills:** reorder/rephrase to surface the posting's keywords. Don't add skills
  the user doesn't have.
- **Contact / name / dates / education:** leave unchanged (don't include them).

Leave any line you don't want to change OUT of your replacements — untouched lines
stay verbatim. If the posting is Hebrew, write replacements in fluent Hebrew.

> On trimming/reordering: this tool replaces text in place; it does not move or
> delete paragraphs. To drop a weak bullet, replace it with a stronger real one,
> or set `"replace": ""` to blank it (leaves an empty line). If a true reorder is
> needed for one-page fit, say so in your report rather than fabricating.

## STEP 4 — Write replacements.json

A JSON array of `{find, replace}` objects. Each `find` MUST be copied **verbatim**
from Step 2's output (exact characters, or it won't match):

```json
[
  {"find": "Strategic Operations Leader with over 20 years...", "replace": "Operations Director with 20+ years..."},
  {"find": "Led company strategy in Marketing, Sales...", "replace": "Owned go-to-market across Marketing & Sales..."}
]
```

## STEP 5 — Build the tailored CV

```bash
python cv_tools.py apply \
  --doc resume.docx \
  --output "output/CV_<Company>_<Role>.docx" \
  --replacements replacements.json
```

Read the output: it reports `N/M replacements applied`. If any `find` "matched 0
times," you didn't copy it verbatim from Step 2 — fix that `find` and re-run.

## STEP 6 — Report

Tell the user:
- Where the file was saved.
- An **ATS match estimate** (0–100): how well the tailored CV covers the posting's
  keywords/requirements, based only on the user's real content.
- **Quick wins:** 2–4 honest suggestions (e.g. "the posting stresses budget
  ownership — I moved your 18M figure into the profile" or "they want SQL; you
  don't list it, so I left it out — add it to your CV if you have it").

Never raise the ATS score by inventing content.
