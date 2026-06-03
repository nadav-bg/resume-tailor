---
name: resume-tailor
description: Tailor a one-page CV to a specific job posting. Provide the posting as a screenshot path, pasted text, or URL. Pulls all content strictly from the user's own my_cv.md (zero hallucinations), fills a tokenized template.docx, and outputs a .docx plus an ATS match estimate. Works in Hebrew and English. Triggers when the user wants to tailor/customize/generate a resume or CV for a job.
argument-hint: <job-posting screenshot path | pasted text | URL>
allowed-tools: Read, Bash, Write, Edit, WebFetch
---

# Resume Tailor (Claude Code entry point)

Follow the full recipe in **`WORKFLOW.md`** in this folder, start to finish.

- The job posting is in `$ARGUMENTS` (a screenshot path, pasted text, or URL). If
  empty, ask the user for it.
- The user's real CV baseline is `my_cv.md` — the only source of truth.
- The template to fill is `template.docx` (tokenized with `{{...}}`).
- Build the output with `build_cv.py` per WORKFLOW.md Step 5.

Do not invent any content. Match the posting's language (Hebrew or English).
