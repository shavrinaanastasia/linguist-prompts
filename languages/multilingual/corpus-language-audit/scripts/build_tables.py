"""Turn the raw per-code audit (data/raw_audit.json) into the CSV tables of this folder.

Usage: python scripts/build_tables.py   (run from the corpus-language-audit folder)
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data"

# Languages that are mostly the language of description (grammars, dictionaries,
# summaries); the summary-based check says nothing about them.
METALANGUAGES = {"eng", "fra", "spa", "por", "rus", "deu", "zho", "cmn", "ita", "nld", "lat", "ara"}
SPECIAL = {"und", "mis", "mul", "zxx"}
ISO_639_2B = {"alb", "arm", "baq", "bur", "chi", "cze", "dut", "fre", "geo", "ger", "gre",
              "ice", "mac", "mao", "may", "per", "rum", "slo", "tib", "wel"}
COLLECTIVE = set("""aav afa alg alv apa aqa aql art ath auf aus awd azc bad bai bat ber bih bnt btk
cai cau cba ccn ccs cdc cdd cel cmc cpe cpf cpp crp csu cus day dmn dra egx esx euq fiu fox gem gme
gmq gmw grk hmx hok hyx iir ijo inc ine ira iro itc jpx kar kdo khi kro map mkh mno mun myn nah nai
ngf nic nub omq omv oto paa phi plf poz pqe pqw pra qwe roa sai sal sdv sem sgn sio sit sla smi son
sqj ssa syd tai tbq trk tup tut tuw urj wak wen xgn xnd ypk zhx zle zls zlw znd""".split())


def code_kind(code):
    if code in SPECIAL:
        return "special"
    if "qaa" <= code <= "qtz":
        return "private-use"
    if code in ISO_639_2B:
        return "iso639-2/B"
    if code in COLLECTIVE:
        return "collective"
    return "iso639-3"


def main():
    rows = json.load(open(DATA / "raw_audit.json", encoding="utf-8"))["rows"]
    out = []
    for r in rows:
        r = dict(r)
        if r["code"] in METALANGUAGES:
            r["verdict"] = "n/a-metalanguage"
            r["suggested"] = r["suggested_name"] = ""
        r["code_kind"] = code_kind(r["code"])
        name = (r.get("suggested_name") or "").lower()
        r["prefix_signature"] = int(
            r["verdict"] in ("mislabel", "partial")
            and bool(r["suggested"])
            and r["suggested"] != r["code"]
            and "".join(ch for ch in name if ch.isalpha()).startswith(r["code"])
        )
        r["confidence"] = "low" if r["sample"] < 5 else ("medium" if r["sample"] < 30 else "high")
        out.append(r)
    out.sort(key=lambda r: -r["total"])

    cols = ["code", "ref_name", "code_kind", "total", "sample", "confidence", "verdict",
            "suggested", "suggested_name", "prefix_signature", "primary_pct", "match_pct",
            "other_pct", "meta_only_pct", "none_pct", "other_langs", "primary_was",
            "formats", "sources", "examples"]
    with open(DATA / "written_language_audit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(out)

    flagged = [r for r in out if r["verdict"] in ("mislabel", "partial")]
    with open(DATA / "suspected_mislabels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(flagged)

    # summary numbers for the README
    by = defaultdict(lambda: [0, 0])
    for r in out:
        by[r["verdict"]][0] += 1
        by[r["verdict"]][1] += r["total"]
    stats = {
        "codes": len(out),
        "label_doc_pairs": sum(r["total"] for r in out),
        "by_verdict": {k: {"codes": v[0], "docs": v[1]} for k, v in by.items()},
        "by_code_kind": dict(Counter(r["code_kind"] for r in out)),
        "prefix_signature_codes": sum(r["prefix_signature"] for r in out),
        "mislabel_high_conf": sum(1 for r in out if r["verdict"] == "mislabel" and r["confidence"] != "low"),
        "secondary_label_share_pct": round(
            100 * sum(r["total"] * (100 - r["primary_pct"]) / 100 for r in out)
            / sum(r["total"] for r in out), 1),
    }
    json.dump(stats, open(DATA / "summary_stats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
