
import csv
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
LABS_DIR = PROJECT_DIR.parent
OLD_LAB_DIR = LABS_DIR / "indirect_injection"

sys.path.insert(0, str(OLD_LAB_DIR))

from evaluate_test_cases import classify_document  # noqa: E402
from improved_detector import detect_injection  # noqa: E402

CASES_FILE = PROJECT_DIR / "unseen_test_cases.json"
RESULTS_FILE = BASE_DIR / "comparison_results.csv"


def calculate_metrics(expected_values, predicted_values):
    tp = sum(e and p for e, p in zip(expected_values, predicted_values))
    tn = sum(not e and not p for e, p in zip(expected_values, predicted_values))
    fp = sum(not e and p for e, p in zip(expected_values, predicted_values))
    fn = sum(e and not p for e, p in zip(expected_values, predicted_values))

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    accuracy = (tp + tn) / len(expected_values) if expected_values else 0.0

    return tp, tn, fp, fn, accuracy, precision, recall, f1


def main():
    with CASES_FILE.open(encoding="utf-8") as file:
        cases = json.load(file)

    rows = []
    expected_values = []
    baseline_values = []
    improved_values = []

    for case in cases:
        document = case["document"]
        expected = case["expected_injection"]

        baseline, _, baseline_reason = classify_document(document)
        improved_result = detect_injection(document)
        improved = improved_result["predicted_injection"]

        expected_values.append(expected)
        baseline_values.append(baseline)
        improved_values.append(improved)

        rows.append({
            "test_id": case["id"],
            "category": case["category"],
            "expected": expected,
            "baseline_prediction": baseline,
            "baseline_reason": baseline_reason,
            "improved_prediction": improved,
            "improved_reason": improved_result["reason"],
            "baseline_correct": baseline == expected,
            "improved_correct": improved == expected,
        })

    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"{row['test_id']}: expected={row['expected']}, "
            f"baseline={row['baseline_prediction']} "
            f"(correct={row['baseline_correct']}), "
            f"improved={row['improved_prediction']} "
            f"(correct={row['improved_correct']})"
        )

    for name, predictions in [
        ("Baseline", baseline_values),
        ("Improved", improved_values),
    ]:
        metrics = calculate_metrics(expected_values, predictions)
        tp, tn, fp, fn, accuracy, precision, recall, f1 = metrics

        print(f"\n=== {name} Metrics ===")
        print(f"TP={tp}, TN={tn}, FP={fp}, FN={fn}")
        print(f"Accuracy:  {accuracy:.1%}")
        print(f"Precision: {precision:.1%}")
        print(f"Recall:    {recall:.1%}")
        print(f"F1-score:  {f1:.1%}")

    print(f"\nComparison saved to: {RESULTS_FILE}")
    print("Results describe only this small hand-written dataset.")


if __name__ == "__main__":
    main()
