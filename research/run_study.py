"""Write results.json and refresh every marked count from that same run."""

import json
from pathlib import Path

from eorscreen.report import abstract_text, fill_marked, manuscript_text, measured_block
from eorscreen.study import run


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = run(root / "data" / "EOR_36Case_Processed_Analytical_Dataset_v1.csv")
    results = root / "research" / "results.json"
    results.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    block = measured_block(payload)
    for relative in (
        "README.md",
        "docs/JOURNAL_FIT.md",
        "docs/TRL.md",
        "docs/ACHIEVEMENTS.md",
    ):
        fill_marked(root / relative, block)
    fill_marked(root / "article" / "abstract.md", abstract_text(payload))
    manuscript = root / "article" / "manuscript.txt"
    manuscript.parent.mkdir(parents=True, exist_ok=True)
    manuscript.write_text(manuscript_text(payload), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
