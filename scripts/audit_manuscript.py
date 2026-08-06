#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

from publication_manifest import PublicationSection, load_publication_manifest


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
FORMULA_OPEN = re.compile(r"^\\\[\s*$")
FORMULA_CLOSE = re.compile(r"^\\\]\s*$")
IMAGE = re.compile(r"!\[([^\]]+)\]\(([^)]+)\)")
FOOTNOTE = re.compile(r"^\[\^[^\]]+\]:", re.MULTILINE)
CITATION = re.compile(r"\[\[(\d+)\]\([^)]*#ref-(\d+)\)\]")


REQUIRED_PHRASES = {
    "Part 0": "# Part 0: The System in Action",
    "Agent lifecycle": "Agent-427",
    "The Gap": "The Gap",
    "RLHF": "RLHF as a Belief Update",
    "offline RL": "Offline RL",
    "memory reality": "The Messy Reality of Memory",
    "memory interference": "Interference",
    "memory consolidation": "Consolidation",
    "forgetting": "Forgetting as a Virtue",
    "responsive environment": "The Responsive Environment",
    "strategic sensing": "Strategic Sensing",
    "sensor poisoning": "Sensor Poisoning",
    "latency": "Latency as a First-Class Citizen",
    "timeout action": "Timeout as Action",
    "scalable oversight": "Scalable Oversight",
    "collusion": "Emergent Collusion",
    "trust": "Trust Delegation",
    "verdict": "The Verdict",
}


def text_of(section: PublicationSection) -> str:
    return section.path.read_text(encoding="utf-8")


def display_formula_checks(section: PublicationSection, text: str) -> tuple[int, list[str]]:
    lines = text.splitlines()
    formula_count = 0
    issues: list[str] = []
    inside = False
    for index, line in enumerate(lines):
        if FORMULA_OPEN.match(line):
            if inside:
                issues.append(f"{section.source}:{index + 1}: nested display formula")
            inside = True
            formula_count += 1
        elif FORMULA_CLOSE.match(line):
            if not inside:
                issues.append(f"{section.source}:{index + 1}: display formula closes without opening")
            inside = False
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            if next_index >= len(lines) or not lines[next_index].startswith("> **Try this with numbers.**"):
                issues.append(f"{section.source}:{index + 1}: display formula lacks immediate Try this with numbers box")
    if inside:
        issues.append(f"{section.source}: unclosed display formula")
    return formula_count, issues


def chapter_groups(sections: tuple[PublicationSection, ...]) -> list[list[PublicationSection]]:
    groups: list[list[PublicationSection]] = []
    current: list[PublicationSection] | None = None
    for section in sections:
        if section.kind == "chapter":
            current = [section]
            groups.append(current)
        elif section.kind == "topic" and current is not None:
            current.append(section)
    return groups


def exercise_body(text: str) -> str:
    match = re.search(r"^## Exercise[^\n]*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def audit() -> tuple[list[str], dict[str, int]]:
    sections = load_publication_manifest(BOOK_DIR)
    issues: list[str] = []
    counts: Counter[str] = Counter()
    all_text = "\n".join(text_of(section) for section in sections)

    for label, phrase in REQUIRED_PHRASES.items():
        if phrase not in all_text:
            issues.append(f"missing mandatory manuscript element: {label} ({phrase!r})")

    for section in sections:
        text = text_of(section)
        formulas, formula_issues = display_formula_checks(section, text)
        counts["formulas"] += formulas
        issues.extend(formula_issues)

        for alt, target in IMAGE.findall(text):
            counts["images"] += 1
            if not alt.strip():
                issues.append(f"{section.source}: diagram has empty alt text")
            if target.startswith(("http://", "https://", "data:")):
                continue
            asset = (section.path.parent / target).resolve()
            if not asset.is_file():
                issues.append(f"{section.source}: missing diagram asset {target}")

        for shown, linked in CITATION.findall(text):
            counts["citations"] += 1
            if shown != linked:
                issues.append(f"{section.source}: citation label {shown} targets ref-{linked}")

        if section.kind == "topic":
            for heading in ("## The Assumption", "## The Violation", "## When It Fails"):
                if heading not in text:
                    issues.append(f"{section.source}: missing {heading}")
            body = exercise_body(text)
            if not body:
                issues.append(f"{section.source}: missing ## Exercise")
            elif not re.search(r"\b(?:implement|write|build|code)\b", body, re.IGNORECASE) or not re.search(r"\b(?:tests?|asserts?|verif(?:y|ies))\b", body, re.IGNORECASE):
                issues.append(f"{section.source}: exercise must require code and tests")

    referenced_pngs = {
        target
        for section in sections
        for _alt, target in IMAGE.findall(text_of(section))
        if target.endswith(".png") and "/diagrams/" in target
    }
    counts["unique_diagrams"] = len(referenced_pngs)
    if len(referenced_pngs) < 10:
        issues.append(f"only {len(referenced_pngs)} unique publication diagrams are placed; need at least 10")

    for group in chapter_groups(sections):
        chapter_text = "\n".join(text_of(section) for section in group)
        chapter_name = group[0].source
        footnotes = len(FOOTNOTE.findall(chapter_text))
        counts["footnotes"] += footnotes
        if footnotes < 3:
            issues.append(f"{chapter_name}: has {footnotes} footnotes; need at least 3")
        if "**Skeptical Engineer:**" not in chapter_text:
            issues.append(f"{chapter_name}: missing Skeptical Engineer exchange")
        if "Agent-427" not in chapter_text:
            issues.append(f"{chapter_name}: Agent-427 lifecycle thread is absent")

    if "legacy-v2" not in all_text or "YAML" not in all_text or "TOML" not in all_text or "self-cit" not in all_text.lower():
        issues.append("memory chapter lacks the complete legacy-v2 YAML/TOML self-citing contamination trace")
    if "Kalman" not in all_text or "queue depth" not in all_text.lower():
        issues.append("embodiment chapter lacks the queue-depth Kalman example")
    if "Byzantine" not in all_text or not re.search(r"(?:lie|lying|inconsistent).{0,100}Router|Router.{0,100}(?:lie|lying|inconsistent)", all_text, re.IGNORECASE | re.DOTALL):
        issues.append("society chapter lacks a Byzantine agent lying to the Router")

    reference_text = (BOOK_DIR / "references.md").read_text(encoding="utf-8")
    anchors = set(re.findall(r"\{#ref-(\d+)\}", reference_text))
    for shown, _linked in CITATION.findall(all_text):
        if shown not in anchors:
            issues.append(f"citation ref-{shown} has no bibliography anchor")

    return issues, dict(counts)


def main() -> None:
    issues, counts = audit()
    print(
        "Manuscript contract: "
        f"{counts.get('formulas', 0)} formulas, "
        f"{counts.get('unique_diagrams', 0)} unique diagrams, "
        f"{counts.get('footnotes', 0)} chapter footnotes, "
        f"{counts.get('citations', 0)} citations"
    )
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        raise SystemExit(1)
    print("PASS: all editor-mandated manuscript invariants are present")


if __name__ == "__main__":
    main()
