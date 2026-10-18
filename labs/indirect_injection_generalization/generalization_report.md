# Indirect Prompt Injection — Generalization Evaluation

## Objective
Evaluate an existing rule-based prompt-injection detector against a separate set of 10 hand-written test cases.

## Initial Results
- Test cases: 10
- True Positives (TP): 0
- True Negatives (TN): 5
- False Positives (FP): 1
- False Negatives (FN): 4
- Accuracy: 50%
- Precision: 0%
- Recall: 0%
- F1-score: 0%

## Findings
The detector missed four injected instructions because their wording differed from the phrases in its existing indicator list. It also incorrectly flagged one educational discussion as an injection.

## Limitations
The dataset is small and manually authored. The labels reflect the intended classification for this experiment. These results do not establish performance against all prompt-injection attacks.

The evaluation tests the rule-based detector, not the security of the local language model itself.

## Conclusion
The initial evaluation shows limited generalization beyond the detector's existing indicators. Further evaluation should use a larger, independently designed dataset and carefully labeled contextual examples.
