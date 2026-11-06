"""Write research/results.json from the deposited table. No constants are typed here."""

import json
from pathlib import Path

from eorscreen.study import run


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = run(root / "data" / "EOR_36Case_Processed_Analytical_Dataset_v1.csv")
    destination = root / "research" / "results.json"
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    destination.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
