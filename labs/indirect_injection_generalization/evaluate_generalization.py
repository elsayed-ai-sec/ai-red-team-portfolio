
import csv
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LABS_DIR = BASE_DIR.parent
OLD_LAB_DIR = LABS_DIR / "indirect_injection"

sys.path.insert(0, str(OLD_LAB_DIR))

from evaluate_test_cases import (  # noqa: E402
    classify_document,
    calculate_metrics,
)

CASES_FILE = BASE_DIR / "unseen_test_cases.json"
RESULTS_FILE = BASE_DIR / "generalization_results.csv"


def main():
    with CASES_FILE.open(encoding="utf-8") as file:
        cases = json.load(file)

    results = []

    for case in cases:
        predicted, matches, reason = classify_document(
            case["document"]
        )
        expected = case["expected_injection"]

        results.append({
            "test_id": case["id"],
            "category": case["category"],
            "expected_injection": expected,
            "predicted_injection": predicted,
            "matched_phrases": "; ".join(matches),
            "classification_reason": reason,
            "correct": predicted == expected,
        })

        print(
            f"{case['id']}: expected={expected}, "
            f"predicted={predicted}, reason={reason}, "
            f"correct={predicted == expected}"
        )

    fields = [
        "test_id",
        "category",
        "expected_injection",
        "predicted_injection",
        "matched_phrases",
        "classification_reason",
        "correct",
    ]

    with RESULTS_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    metric_rows = [
        {
            "expected_injection": row["expected_injection"],
            "input_indicator_found": row["predicted_injection"],
        }
        for row in results
    ]

    metrics = calculate_metrics(metric_rows)

    print("\n=== Unseen Test Metrics ===")
    print(
        f"TP={metrics['TP']}, TN={metrics['TN']}, "
        f"FP={metrics['FP']}, FN={metrics['FN']}"
    )
    print(f"Accuracy:  {metrics['accuracy']:.1%}")
    print(f"Precision: {metrics['precision']:.1%}")
    print(f"Recall:    {metrics['recall']:.1%}")
    print(f"F1-score:  {metrics['f1']:.1%}")
    print(f"\nResults saved to: {RESULTS_FILE}")
    print("Metrics apply only to this small test set.")


if __name__ == "__main__":
    main()
