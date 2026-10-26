#!/usr/bin/env python3
"""Build the static website's page data from the canonical Markdown routes."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "en"
OUT = ROOT / "data" / "pages.json"


def display_title(value: str) -> str:
    """Keep route IDs in filenames and URLs, but not learner-facing web labels."""
    return re.sub(r"^[0-9]+[A-Z] - ", "", value)


def routes() -> list[dict[str, str]]:
    raw = (EN / "pathways.yml").read_text()
    groups = []
    current = None
    option = None
    for line in raw.splitlines():
        if line.startswith("  - id: "):
            current = {"id": line.partition(": ")[2], "title": "", "options": []}
            groups.append(current)
        elif current is not None and line.startswith("    title: "):
            current["title"] = line.partition(": ")[2]
        elif line.startswith("      - id: "):
            option = {"id": line.partition(": ")[2]}
            current["options"].append(option)
        elif option is not None and line.startswith("        file: "):
            option["file"] = line.partition(": ")[2]
        elif option is not None and line.startswith("        title: "):
            option["title"] = line.partition(": ")[2]
        elif option is not None and line.startswith("        description: "):
            option["description"] = line.partition(": ")[2]
    return groups


def inline(value: str, ids: dict[str, str]) -> str:
    tokens = []

    def hold(markup: str) -> str:
        tokens.append(markup)
        return f"\x01{len(tokens) - 1}\x02"

    def image(match: re.Match[str]) -> str:
        alt, target = match.groups()
        url = "en/" + target if not target.startswith("http") else target
        return hold(f'<a class="image-link" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener"><img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy"></a>')

    def link(match: re.Match[str]) -> str:
        label, target = match.groups()
        filename = unquote(target.split("#", 1)[0])
        if filename in ids:
            href = "#step/" + ids[filename]
            extra = " data-prereq"
        elif filename == "landing.md":
            href = "#hub"
            extra = " data-prereq"
        elif target.startswith(("http://", "https://")):
            href = target
            extra = ' target="_blank" rel="noopener"'
        elif target.endswith(".md"):
            href = "en/" + target
            extra = ""
        else:
            href = "en/" + target
            extra = ""
        if filename in ids:
            label = display_title(label)
        return hold(f'<a href="{html.escape(href, quote=True)}"{extra}>{html.escape(label)}</a>')

    value = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image, value)
    value = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", link, value)
    value = re.sub(r"`([^`]+)`", lambda m: hold("<code>" + html.escape(m.group(1)) + "</code>"), value)
    value = html.escape(value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", value)
    for index, markup in enumerate(tokens):
        value = value.replace(f"\x01{index}\x02", markup)
    return value


def blocks(source: str, ids: dict[str, str]) -> str:
    lines = source.splitlines()
    output = []
    at = 0
    first_heading = True
    while at < len(lines):
        line = lines[at]
        if not line.strip():
            at += 1
            continue
        if line == "<details>":
            at += 1
            summary = re.fullmatch(r"<summary>(.+)</summary>", lines[at])
            assert summary, "A details block needs a summary"
            at += 1
            content = []
            while at < len(lines) and lines[at] != "</details>":
                content.append(lines[at])
                at += 1
            assert at < len(lines), "Unclosed details block"
            at += 1
            output.append(f'<details class="worked-example"><summary>{inline(summary.group(1), ids)}</summary>{blocks(chr(10).join(content), ids)}</details>')
            continue
        if line.startswith(">"):
            quoted = []
            while at < len(lines) and lines[at].startswith(">"):
                quoted.append(re.sub(r"^> ?", "", lines[at]))
                at += 1
            kind = "note"
            if quoted and re.fullmatch(r"\[!(CAUTION|TIP|TASK)\]", quoted[0]):
                kind = quoted.pop(0)[2:-1].lower()
            inner = blocks("\n".join(quoted), ids)
            label = {"caution": "Before you test", "tip": "Tip", "task": "Try this", "note": "Note"}[kind]
            output.append(f'<aside class="callout {kind}"><span class="callout-label">{label}</span>{inner}</aside>')
            continue
        if line.startswith("```"):
            language = line[3:].strip()
            at += 1
            code = []
            while at < len(lines) and not lines[at].startswith("```"):
                code.append(lines[at])
                at += 1
            at += 1
            output.append(f'<div class="code-wrap"><div class="code-head"><span>{html.escape(language or "Code")}</span><button class="copy-code" type="button">Copy code</button></div><pre tabindex="0" aria-label="Code to try"><code>{html.escape(chr(10).join(code))}</code></pre></div>')
            continue
        if line.startswith("## "):
            tag = "h1" if first_heading else "h2"
            first_heading = False
            output.append(f"<{tag}>{inline(line[3:], ids)}</{tag}>")
            at += 1
            continue
        if line.startswith("### "):
            output.append(f"<h3>{inline(line[4:], ids)}</h3>")
            at += 1
            continue
        if line.startswith("- "):
            items = []
            while at < len(lines) and lines[at].startswith("- "):
                items.append("<li>" + inline(lines[at][2:], ids) + "</li>")
                at += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue
        paragraph = [line]
        at += 1
        while at < len(lines) and lines[at].strip() and not re.match(r"^(>|```|## |### |- )", lines[at]):
            paragraph.append(lines[at])
            at += 1
        output.append("<p>" + inline(" ".join(paragraph), ids) + "</p>")
    return "\n".join(output)


def build() -> str:
    groups = routes()
    presentation = json.loads((ROOT / "data/presentation.json").read_text())
    options = [option for group in groups for option in group["options"]]
    ids = {option["file"]: option["id"] for option in options}
    pages = {}
    for option in options:
        page = EN / option["file"]
        body = page.read_text()
        body = re.sub(r"^## [0-9]+[A-Z] - ", "## ", body, count=1)
        # Only unquoted level-two headings divide a lesson. Wiring, code and
        # worked examples remain verbatim inside their original section.
        chunks = re.split(r"^## (.+)\n", body, flags=re.M)
        sections = [
            {"title": chunks[index],
             "key": re.sub(r"[^a-z0-9]+", "-", chunks[index].lower()).strip("-"),
             "html": blocks(chunks[index + 1], ids)}
            for index in range(3, len(chunks), 2)
        ]
        pages[option["id"]] = {
            "title": display_title(option["title"]), "html": blocks(body, ids),
            "intro": blocks(chunks[2], ids), "sections": sections,
        }
    result = {"landing": blocks((EN / "landing.md").read_text(), ids),
              "groups": [{"title": group["title"], **presentation["groups"][group["id"]],
                          "options": [{"id": o["id"], "title": display_title(o["title"]),
                                       **presentation["options"].get(o["id"], {}),
                                       **({"description": o["description"]} if o.get("description") else {})}
                                      for o in group["options"]]} for group in groups],
              "pages": pages}
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = build()
    if args.check:
        assert OUT.read_text() == output, "Web pages are out of sync with Markdown"
        print("Checked web pages against Markdown")
    else:
        OUT.write_text(output)
        print("Built web pages from Markdown")


if __name__ == "__main__":
    main()
