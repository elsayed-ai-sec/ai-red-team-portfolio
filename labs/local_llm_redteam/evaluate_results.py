import csv
from pathlib import Path

RESULTS_FILE = Path(__file__).resolve().parent / "test_results.csv"


def main():
    with RESULTS_FILE.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("No test results found.")
        return

    passed = sum(row["result"].strip().lower() == "pass" for row in rows)
    failed = sum(row["result"].strip().lower() == "fail" for row in rows)
    total = len(rows)

    print("AI Red Teaming Test Summary")
    print("---------------------------")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success rate: {passed / total * 100:.1f}%")
    print(f"Failure rate: {failed / total * 100:.1f}%")


if __name__ == "__main__":
    main()
