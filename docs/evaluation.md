# Sahay Evaluation Framework

## Evaluation Metrics

1. **Retrieval Precision & Recall**: Percentage of relevant schemes retrieved for specific user scenarios.
2. **Urgency Precision**: Accurate detection of `CRISIS` vs `NORMAL` requests.
3. **Eligibility Reasoning Accuracy**: Match rate between rule-engine evaluations and benchmark ground truth.
4. **Hallucination Rate**: Zero tolerance for fabricated URLs, emergency numbers, or scheme names.
5. **Missing Information Coverage**: Rate at which necessary missing facts (e.g. income threshold) are correctly identified.

## Evaluation Dataset
- Located at `evaluations/datasets/benchmark.json`.
- Contains test scenarios covering disaster relief, unemployment, disability support, student aid, and food security.
