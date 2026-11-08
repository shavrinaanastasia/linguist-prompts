"""Render ERROR_TYPES.md: the narrative template plus one table per error type.

Usage (from the corpus-language-audit folder):
    python scripts/build_error_types.py
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(HERE / "data" / "proposed_corrections_by_code.csv", encoding="utf-8")))
inflated = list(csv.DictReader(open(HERE / "data" / "inflated_counts.csv", encoding="utf-8")))
template = (HERE / "scripts" / "error_types_template.md").read_text(encoding="utf-8")

CONF_RU = {"verified": "проверено вручную", "high": "высокая", "medium": "средняя"}


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def table(etype):
    sel = [r for r in rows if r["error_type"] == etype and r["confidence"] in CONF_RU]
    order = {"verified": 0, "high": 1, "medium": 2}
    sel.sort(key=lambda r: (order[r["confidence"]], -int(r["docs_in_catalogue"] or 0)))
    out = ["| Метка в корпусе | Документов | На самом деле | Доля в проверке | Уверенность | Пример документа |",
           "|---|---:|---|---:|---|---|"]
    for r in sel:
        share = r["proposed_share_pct"] or ""
        share = f"{share}%" if share else "—"
        ex = esc(r["example"] or r["manual_note"])[:90]
        out.append(f"| `{r['label_code']}` {esc(r['label_name'])} | {r['docs_in_catalogue']} | "
                   f"`{r['proposed_code']}` {esc(r['proposed_name'])} | {share} | {CONF_RU[r['confidence']]} | {ex} |")
    return "\n".join(out), len(sel)


def inflated_table(n=30):
    out = ["| Код | Язык | Документов в счётчике | Язык основной | Оценка «настоящих» | Основной язык у остальных |",
           "|---|---|---:|---:|---:|---|"]
    for r in inflated[:n]:
        out.append(f"| `{r['code']}` | {esc(r['ref_name'])} | {r['documents_listed']} | {r['primary_pct_in_sample']}% | "
                   f"{r['est_primary_docs']} | {esc(r['first_language_when_not_primary'])} |")
    return "\n".join(out)


text = template
for et in ["code_from_name", "wrong_language", "related_or_neighbour_language", "historical_stage"]:
    t, n = table(et)
    text = text.replace("{{table:" + et + "}}", t).replace("{{count:" + et + "}}", str(n))
text = text.replace("{{table:inflated}}", inflated_table())
(HERE / "ERROR_TYPES.md").write_text(text, encoding="utf-8")
print("ok")
