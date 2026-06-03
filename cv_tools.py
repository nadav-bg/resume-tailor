#!/usr/bin/env python3
"""
cv_tools.py — Tailor a Word (.docx) CV in place, with zero manual prep.

No tokens, no template editing. The user drops in their real resume.docx; the
agent reads its exact text and supplies tailored replacements; this script swaps
the original strings for the tailored ones, preserving all design, fonts and
direction (Hebrew/RTL included — only text inside <w:t> nodes is touched).

Two subcommands:

  extract --doc resume.docx
      Print the document's paragraphs (exact text, JSON array). The agent reads
      these so it knows the precise strings to replace. Copy "find" values from
      here VERBATIM.

  apply --doc resume.docx --output out.docx --replacements pairs.json
      pairs.json is a list of {"find": "...", "replace": "..."} objects.
      Each "find" is matched against the document even when Word has split it
      across multiple runs. "replace" goes in; set it to "" to blank a line.
      Replacements are applied longest-find-first so short strings don't clobber
      longer ones that contain them.

All standard-library; no install needed. UTF-8 throughout.
"""

import argparse
import json
import os
import re
import shutil
import sys
import zipfile

DOC_PART = "word/document.xml"


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def read_doc_xml(path: str) -> str:
    with zipfile.ZipFile(path, "r") as z:
        return z.read(DOC_PART).decode("utf-8")


def paragraphs(xml: str):
    """Yield the concatenated visible text of each <w:p> paragraph, in order."""
    for p in re.findall(r"<w:p\b.*?</w:p>", xml, flags=re.DOTALL):
        texts = re.findall(r"<w:t\b[^>]*>(.*?)</w:t>", p, flags=re.DOTALL)
        if texts:
            joined = "".join(texts)
            # Unescape the few XML entities so the agent sees real characters.
            joined = (
                joined.replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&quot;", '"')
            )
            if joined.strip():
                yield joined


def split_safe_regex(find: str) -> re.Pattern:
    """
    Regex matching `find` even when Word split it across runs, i.e. with optional
    XML tags interspersed between characters. We escape find for XML first so we
    match the on-disk (escaped) form, then allow tags between each character.
    """
    escaped = xml_escape(find)
    gap = r"(?:<[^>]*>)*"
    return re.compile(gap.join(re.escape(ch) for ch in escaped), flags=re.DOTALL)


def cmd_extract(args):
    xml = read_doc_xml(args.doc)
    paras = list(paragraphs(xml))
    json.dump(paras, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    print(f"# {len(paras)} paragraphs", file=sys.stderr)


def cmd_apply(args):
    raw = args.replacements
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as f:
            raw = f.read()
    try:
        pairs = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: --replacements is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(pairs, list):
        print("ERROR: replacements must be a JSON array of {find, replace}.", file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    shutil.copy2(args.doc, args.output)
    xml = read_doc_xml(args.output)

    # Longest find first so a short line that is a substring of a longer one
    # doesn't consume it.
    pairs = [p for p in pairs if isinstance(p, dict) and "find" in p]
    pairs.sort(key=lambda p: len(p.get("find", "")), reverse=True)

    misses = []
    for pair in pairs:
        find = pair.get("find", "")
        repl = pair.get("replace", "")
        if repl is None:
            repl = ""
        if not find:
            continue
        rx = split_safe_regex(find)
        xml, n = rx.subn(xml_escape(str(repl)), xml, count=1)
        if n == 0:
            misses.append(find)

    tmp = args.output + ".tmp.docx"
    with zipfile.ZipFile(args.output, "r") as zin:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == DOC_PART:
                    zout.writestr(item, xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
    os.replace(tmp, args.output)

    print(f"OK  saved: {args.output}  ({len(pairs) - len(misses)}/{len(pairs)} replacements applied)")
    if misses:
        print(
            "  NOTE: these 'find' strings matched 0 times (copy them verbatim from "
            "`extract`, exactly as written):",
            file=sys.stderr,
        )
        for m in misses:
            print(f"    - {m[:80]!r}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Tailor a .docx CV in place (no tokens).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="Dump paragraph text (exact strings) as JSON.")
    pe.add_argument("--doc", required=True)
    pe.set_defaults(func=cmd_extract)

    pa = sub.add_parser("apply", help="Apply {find,replace} pairs to the doc.")
    pa.add_argument("--doc", required=True, help="Source resume .docx")
    pa.add_argument("--output", required=True, help="Output .docx path")
    pa.add_argument("--replacements", required=True, help="pairs.json path or inline JSON")
    pa.set_defaults(func=cmd_apply)

    args = ap.parse_args()
    if not os.path.exists(args.doc):
        print(f"ERROR: doc not found: {args.doc}", file=sys.stderr)
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
