#!/usr/bin/env python3
"""Check local site references and generated article pages using the stdlib."""

import ast
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
URL_RE = re.compile(r"(?<![\w-])url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((self.getpos()[0], value))


def local_target(page, reference):
    """Return (target, exists), or None for external/fragment-only references."""
    reference = reference.strip()
    if not reference or reference.startswith("#"):
        return None
    try:
        parsed = urlsplit(reference)
    except ValueError:
        return page, False
    if parsed.scheme or parsed.netloc:  # Includes http(s), mailto, data, javascript, //...
        return None
    path = unquote(parsed.path)
    if not path:
        return None

    base = ROOT if path.startswith("/") else page.parent
    target = (base / path.lstrip("/")).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return target, False
    if target.is_file():
        return target, True
    return target, (target / "index.html").is_file()


def check_references(pages):
    problems = []
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        parser = ReferenceParser()
        parser.feed(text)
        references = parser.references
        references.extend(
            (text.count("\n", 0, match.start()) + 1, match.group(2))
            for match in URL_RE.finditer(text)
        )
        for line, reference in references:
            result = local_target(page, reference)
            if result is None:
                continue
            checked += 1
            target, exists = result
            if not exists:
                problems.append(
                    f"{page.relative_to(ROOT)}:{line}: broken local reference "
                    f"{reference!r} (resolved to {target})"
                )
    return problems, checked


def configured_post_ids():
    tree = ast.parse((ROOT / "generate-static-articles.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "posts" for target in node.targets
        ):
            return [post[0] for post in ast.literal_eval(node.value)]
    raise ValueError("Could not find the posts list in generate-static-articles.py")


def main():
    pages = [ROOT / "index.html", *sorted(ROOT.glob("post-*/index.html"))]
    problems, checked = check_references(pages)
    post_ids = configured_post_ids()
    for post_id in post_ids:
        if not (ROOT / post_id / "index.html").is_file():
            problems.append(f"Missing generated page for {post_id}: {post_id}/index.html")

    print(f"Checked {checked} local references in {len(pages)} HTML files.")
    print(f"Checked generated pages for {len(post_ids)} configured posts.")
    if problems:
        print("\n".join(f"ERROR: {problem}" for problem in problems))
        print(f"Site check failed with {len(problems)} problem(s).")
        return 1
    print("Site check passed: no broken local references or missing generated pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
