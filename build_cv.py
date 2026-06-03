#!/usr/bin/env python3
"""
build_cv.py — Generic, template-agnostic CV builder.

Fills {{TOKEN}} placeholders in a Word (.docx) template with tailored content.
Works in any language (Hebrew/Arabic RTL included): it edits only the text
inside <w:t> tags and never touches paragraph direction or styling, so your
template's design and RTL layout are preserved exactly.

Robust to Word "run-splitting": Word often breaks a token like {{PROFILE_1}}
across several <w:t> runs. This script matches tokens even when XML tags are
interspersed between their characters.

Usage:
  python build_cv.py --template template.docx --output out.docx --content content.json

content.json format (keys are token names WITHOUT the braces):
  {
    "PROFILE_1": "First profile bullet...",
    "ROLE1_BULLET_1": "...",
    "SKILL_1": "Strategic Thinking",
    "NAME": "Jane Doe"
  }

Any token present in the template but missing from content.json is left as-is
(and reported). Any token set to "" is blanked out.
"""

import argparse
import json
import os
import re
import shutil
import sys
import zipfile


def xml_escape(text: str) -> str:
    """Escape a replacement value for safe embedding inside XML text nodes."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def token_regex(token_name: str) -> re.Pattern:
    """
    Build a regex matching {{token_name}} even when Word has split it across
    multiple <w:t> runs (i.e. XML tags interspersed between any characters).

    We allow optional sequences of XML tags (<...>) between every character of
    the literal '{{token_name}}'.
    """
    literal = "{{" + token_name + "}}"
    gap = r"(?:<[^>]*>)*"  # zero or more XML tags between characters
    pattern = gap.join(re.escape(ch) for ch in literal)
    return re.compile(pattern)


def find_all_tokens(xml: str) -> set:
    """
    Discover every {{TOKEN}} present in the document, tolerating run-splitting.
    Strategy: strip XML tags, then scan the plain text for {{...}}.
    """
    plain = re.sub(r"<[^>]*>", "", xml)
    return set(re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", plain))


def apply_content(template_path: str, output_path: str, content: dict) -> None:
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    shutil.copy2(template_path, output_path)

    with zipfile.ZipFile(output_path, "r") as zin:
        xml = zin.read("word/document.xml").decode("utf-8")

    present = find_all_tokens(xml)
    if not present:
        print(
            "WARNING: No {{TOKEN}} placeholders found in the template. "
            "Did you tokenize template.docx? (e.g. type {{PROFILE_1}} where "
            "the first profile bullet should go.)",
            file=sys.stderr,
        )

    # Replace each provided token. Longest names first so e.g. SKILL_10 is not
    # shadowed by SKILL_1.
    for name in sorted(content.keys(), key=len, reverse=True):
        value = content[name]
        if not isinstance(value, str):
            value = "" if value is None else str(value)
        rx = token_regex(name)
        xml, n = rx.subn(xml_escape(value), xml)
        if n == 0 and name in present:
            print(f"  NOTE: token {{{{{name}}}}} present but replacement matched 0 times.", file=sys.stderr)

    # Report tokens left unfilled
    leftover = find_all_tokens(xml)
    if leftover:
        print(
            "  NOTE: these tokens had no value in content.json and were left in place: "
            + ", ".join("{{" + t + "}}" for t in sorted(leftover)),
            file=sys.stderr,
        )

    tmp_path = output_path + ".tmp.docx"
    with zipfile.ZipFile(output_path, "r") as zin:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "word/document.xml":
                    zout.writestr(item, xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
    os.replace(tmp_path, output_path)
    print(f"OK  CV saved to: {output_path}")


def main():
    ap = argparse.ArgumentParser(description="Fill {{TOKEN}} placeholders in a .docx CV template.")
    ap.add_argument("--template", required=True, help="Path to tokenized template .docx")
    ap.add_argument("--output", required=True, help="Path for the generated .docx")
    ap.add_argument("--content", required=True, help="Path to content.json OR a raw JSON string")
    args = ap.parse_args()

    # --content accepts a file path or an inline JSON string
    raw = args.content
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as f:
            raw = f.read()
    try:
        content = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: --content is not valid JSON (file or string): {e}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.template):
        print(f"ERROR: template not found: {args.template}", file=sys.stderr)
        sys.exit(1)

    apply_content(args.template, args.output, content)


if __name__ == "__main__":
    main()
