from datetime import datetime

def build_report(filename, entities, relationships, issues):
    counts = {}
    for e in entities:
        counts[e.entity_type] = counts.get(e.entity_type, 0) + 1
    out = [
        "# AutoHLD-AI Analysis Report", "",
        f"**Document:** {filename}",
        f"**Generated:** {datetime.now().isoformat(timespec='seconds')}", "",
        "## Summary", "",
        f"- Components: {counts.get('component', 0)}",
        f"- Interfaces: {counts.get('interface', 0)}",
        f"- Ports: {counts.get('port', 0)}",
        f"- Signals: {counts.get('signal', 0)}",
        f"- Relationships: {len(relationships)}",
        f"- Potential issues: {len(issues)}", "",
        "## Entities", "",
        "| Type | Name | Page |", "|---|---|---:|"
    ]
    out += [f"| {e.entity_type} | {e.name} | {e.page} |" for e in entities]
    out += ["", "## Relationships", "", "| Source | Relation | Target | Page |", "|---|---|---|---:|"]
    out += [f"| {r.source} | {r.relation} | {r.target} | {r.page} |" for r in relationships]
    out += ["", "## Issues", ""]
    if issues:
        out += [f"- **{i['severity']} — {i['type']}**: {i['message']} (Page {i['page']})" for i in issues]
    else:
        out.append("No rule-based issues detected.")
    out += ["", "> Human review is required before consequential engineering use."]
    return "\n".join(out)
