#!/usr/bin/env python3
"""Split ref/ markdown files into per-section files under ref-v2/.

For each .md file in ref/:
  - Detect the H1 title → topic subdirectory slug
  - Split content at ## boundaries
  - Write each section to ref-v2/<topic-slug>/<N>-<section-slug>.md

Also writes ref-v2/README.md as a master index.

Usage:
    python3 scripts/split_ref.py [--ref-dir ref] [--out-dir ref-v2]
"""

import argparse
import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    """Convert a heading to a lowercase hyphen-separated slug."""
    text = text.strip()
    # Remove markdown formatting (bold, code, etc.)
    text = re.sub(r"[`*_]", "", text)
    # Remove leading numbering like "1.", "Part 1:", etc.
    text = re.sub(r"^[\d]+[.:]\s*", "", text)
    text = re.sub(r"^Part\s+\d+[.:]\s*", "", text, flags=re.IGNORECASE)
    text = text.lower()
    # Replace non-alphanumeric chars with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def topic_slug(filename: str) -> str:
    """Convert a ref filename to a topic directory slug."""
    name = Path(filename).stem  # e.g. "Networking Reference"
    return slugify(name)


def split_markdown(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (preamble, [(heading, body), ...]) split at ## boundaries.

    Falls back to splitting on # boundaries (skipping the first H1 title)
    when no ## sections are present.
    """
    preamble, sections = _split_at(content, "## ")
    if not sections:
        # Fall back: treat additional # headings (after the first title) as sections
        preamble, sections = _split_at_h1(content)
    return preamble, sections


def _split_at(content: str, prefix: str) -> tuple[str, list[tuple[str, str]]]:  # type: ignore[return]
    """Split content at lines starting with *prefix*, returning (preamble, sections)."""
    lines = content.splitlines(keepends=True)
    preamble_lines: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_body: list[str] = []

    for line in lines:
        if line.startswith(prefix):
            if current_heading is not None:
                sections.append((current_heading, "".join(current_body)))
            elif current_body:
                preamble_lines = current_body[:]
            current_heading = line.rstrip("\n")
            current_body = []
        else:
            current_body.append(line)

    if current_heading is not None:
        sections.append((current_heading, "".join(current_body)))
    else:
        preamble_lines = current_body[:]

    preamble = "".join(preamble_lines).strip()
    return preamble, sections


def _split_at_h1(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Split on H1 headings, treating the first as the document title (preamble)."""
    lines = content.splitlines(keepends=True)
    preamble_lines: list[str] = []
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_body: list[str] = []
    first_h1_seen = False

    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            if not first_h1_seen:
                # This is the document title; add to preamble
                preamble_lines.append(line)
                first_h1_seen = True
            else:
                if current_heading is not None:
                    sections.append((current_heading, "".join(current_body)))
                elif current_body:
                    preamble_lines.extend(current_body)
                # Re-emit as ## heading so section files are consistent
                current_heading = "## " + line[2:].rstrip("\n")
                current_body = []
        else:
            current_body.append(line)

    if current_heading is not None:
        sections.append((current_heading, "".join(current_body)))
    else:
        preamble_lines.extend(current_body)

    preamble = "".join(preamble_lines).strip()
    return preamble, sections


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ref-dir",
        default="ref",
        help="Source directory containing the large .md files (default: ref)",
    )
    parser.add_argument(
        "--out-dir",
        default="ref-v2",
        help="Output directory for split files (default: ref-v2)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    ref_dir = repo_root / args.ref_dir
    out_dir = repo_root / args.out_dir

    if not ref_dir.is_dir():
        print(f"Error: source directory '{ref_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(ref_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in '{ref_dir}'.", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    # index: list of (topic_name, topic_slug, [(section_heading, rel_path), ...])
    index: list[tuple[str, str, list[tuple[str, str]]]] = []

    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Extract H1 title (first non-blank line starting with "# ")
        h1_title = md_file.stem  # fallback
        for line in lines:
            if line.startswith("# "):
                h1_title = line[2:].strip()
                break

        t_slug = topic_slug(md_file.name)
        topic_dir = out_dir / t_slug
        topic_dir.mkdir(parents=True, exist_ok=True)

        preamble, sections = split_markdown(content)

        topic_sections: list[tuple[str, str]] = []

        for idx, (heading, body) in enumerate(sections, start=1):
            heading_text = heading[3:].strip()  # strip leading "## "
            s_slug = slugify(heading_text)
            filename = f"{idx:02d}-{s_slug}.md"
            file_path = topic_dir / filename

            # Build section file
            section_content = (
                f"# {h1_title}\n\n"
                f"[← Back to index](../README.md)\n\n"
                f"---\n\n"
                f"{heading}\n"
                f"{body.rstrip()}\n"
            )
            file_path.write_text(section_content, encoding="utf-8")

            rel_path = f"{t_slug}/{filename}"
            topic_sections.append((heading_text, rel_path))

        # Write per-topic README
        topic_readme_lines = [f"# {h1_title}\n", "\n", "[← Back to index](../README.md)\n", "\n"]
        if preamble:
            topic_readme_lines += [preamble, "\n\n"]
        topic_readme_lines.append("## Sections\n\n")
        for heading_text, rel_path in topic_sections:
            section_filename = Path(rel_path).name
            topic_readme_lines.append(f"- [{heading_text}]({section_filename})\n")
        (topic_dir / "README.md").write_text("".join(topic_readme_lines), encoding="utf-8")

        index.append((h1_title, t_slug, topic_sections))
        print(f"  {md_file.name} → {t_slug}/ ({len(sections)} sections)")

    # Write master README.md
    readme_lines = [
        "# Kubernetes Reference — v2\n",
        "\n",
        "Split from [`ref/`](../ref/) for easier navigation. "
        "Each `##` section is its own file.\n",
        "\n",
        "---\n",
        "\n",
    ]

    for h1_title, t_slug, topic_sections in index:
        readme_lines.append(f"## [{h1_title}]({t_slug}/README.md)\n\n")
        for heading_text, rel_path in topic_sections:
            readme_lines.append(f"- [{heading_text}]({rel_path})\n")
        readme_lines.append("\n")

    (out_dir / "README.md").write_text("".join(readme_lines), encoding="utf-8")
    print(f"\nDone. Master index written to {out_dir / 'README.md'}")


if __name__ == "__main__":
    main()
