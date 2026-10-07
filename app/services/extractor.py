import re
from collections import defaultdict
from .models import Entity, Relationship

PATTERNS = {
    "component": r"\b(?:Component|SWC|Software Component)\s*[:\-]\s*([A-Za-z][A-Za-z0-9_.-]+)",
    "interface": r"\b(?:Interface|P-Port Interface|R-Port Interface)\s*[:\-]\s*([A-Za-z][A-Za-z0-9_.-]+)",
    "port": r"\b(?:Port|P-Port|R-Port)\s*[:\-]\s*([A-Za-z][A-Za-z0-9_.-]+)",
    "signal": r"\bSignal\s*[:\-]\s*([A-Za-z][A-Za-z0-9_.-]+)",
}

REL_PATTERNS = [
    (r"\b([A-Za-z][A-Za-z0-9_.-]+)\s+uses\s+interface\s+([A-Za-z][A-Za-z0-9_.-]+)", "uses_interface"),
    (r"\b([A-Za-z][A-Za-z0-9_.-]+)\s+connects\s+to\s+([A-Za-z][A-Za-z0-9_.-]+)", "connects_to"),
    (r"\b([A-Za-z][A-Za-z0-9_.-]+)\s+depends\s+on\s+([A-Za-z][A-Za-z0-9_.-]+)", "depends_on"),
    (r"\b([A-Za-z][A-Za-z0-9_.-]+)\s+provides\s+([A-Za-z][A-Za-z0-9_.-]+)", "provides"),
]

def extract_entities(chunks):
    out, seen = [], set()
    for ch in chunks:
        for typ, pat in PATTERNS.items():
            for m in re.finditer(pat, ch.text, re.I):
                name = m.group(1)
                key = (typ, name.lower(), ch.page)
                if key not in seen:
                    out.append(Entity(name, typ, ch.page, m.group(0)))
                    seen.add(key)
    return out

def extract_relationships(chunks):
    out, seen = [], set()
    for ch in chunks:
        for pat, relation in REL_PATTERNS:
            for m in re.finditer(pat, ch.text, re.I):
                source = m.group(1).rstrip(".,;:")
                target = m.group(2).rstrip(".,;:")
                key = (source.lower(), relation, target.lower(), ch.page)
                if key not in seen:
                    out.append(Relationship(
                        source, relation, target, ch.page, m.group(0)
                    ))
                    seen.add(key)
    return out

def detect_issues(chunks, entities, relationships):
    issues = []
    by_name = defaultdict(set)
    for e in entities:
        by_name[e.name.lower()].add(e.entity_type)
    for name, types in by_name.items():
        if len(types) > 1:
            issues.append({
                "type": "Terminology ambiguity",
                "severity": "Medium",
                "message": f"'{name}' appears as multiple entity types: {', '.join(sorted(types))}.",
                "page": "-"
            })

    interfaces = {e.name.lower() for e in entities if e.entity_type == "interface"}
    for r in relationships:
        if r.relation == "uses_interface" and r.target.lower() not in interfaces:
            issues.append({
                "type": "Potential missing interface",
                "severity": "High",
                "message": f"{r.source} references interface '{r.target}', but no explicit interface definition was found.",
                "page": r.page
            })

    all_text = " ".join(c.text for c in chunks)
    if ("updated from" in all_text.lower() or "updated to" in all_text.lower()) and "interface" in all_text.lower():
        issues.append({
            "type": "Revision terminology change",
            "severity": "Medium",
            "message": "The document contains an explicit interface terminology change; review references for consistency.",
            "page": "-"
        })
    return issues
