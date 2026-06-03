---
name: resume-tailor
description: Tailor a one-page CV to a specific job posting. Provide the posting as a URL, a screenshot path, or pasted text. Reads the user's real resume.docx as-is (zero setup, no hallucinations), rewrites the wording to match the job, and outputs a tailored .docx that keeps the original design, plus an ATS match estimate. Works in Hebrew and English. Triggers when the user wants to tailor/customize/generate a resume or CV for a job.
argument-hint: <job-posting URL | screenshot path | pasted text>
allowed-tools: Read, Bash, Write, Edit, WebFetch
---

# Resume Tailor (Claude Code entry point)

Follow the full recipe in **`WORKFLOW.md`** in this folder, start to finish.

- The job posting is in `$ARGUMENTS` (a URL, a screenshot path, or pasted text).
  If empty, ask the user for it.
- The user's CV is `resume.docx` in this folder — read its exact text with
  `python cv_tools.py extract --doc resume.docx`. It's the only source of truth.
- Tailor the wording, write `replacements.json`, then build the output with
  `python cv_tools.py apply ...` per WORKFLOW.md Step 5.

Do not invent any content. Match the posting's language (Hebrew or English) and
preserve the CV's original design.
