# Project plan and instructor-feedback checklist

## Why this project

Review a creator's sponsored-video script against a brand brief. Ordinary keyword search can catch literal words, but may miss slang, metaphor, paraphrase, or implied references. An AI reviewer may catch meaning-based cases, but can also invent issues or flag acceptable copy. The project measures that trade-off rather than assuming AI is better.

## Deliverable stages

1. Confirm the audience, script language, and rule scope.
2. Finalize a concise problem statement and product boundary.
3. Define rules and a case schema. Write ground-truth verdicts before model evaluation.
4. Build a reproducible keyword-search baseline and AI-assisted review prototype.
5. Evaluate both methods on the same fixed primary set of 30 balanced cases: 10 compliant, 10 violating, and 10 borderline.
6. Report both error directions, borderline handling, valid structured-output rate, API cost per script, limitations, and representative failures.
7. Prepare the final written submission and recorded demo.

## Feedback checklist

- [ ] At least 30 balanced primary cases; do not mix later stress cases into the primary result.
- [ ] Ground-truth labels and short rationales authored before running the model.
- [ ] Include clean scripts and score false positives and false negatives correctly.
- [ ] Run keyword search on the actual same test cases; do not report an unmeasured baseline.
- [ ] Include API cost per script (and disclose model, token assumptions, and measurement date).
- [ ] Document course concepts in the final report, including API cost (Class 5).

## Measurement definitions (draft)

- **False positive:** compliant script incorrectly flagged as violating.
- **False negative:** violating script incorrectly passed as safe.
- **Borderline escalation:** borderline case routed to a human reviewer rather than guessed as safe/unsafe.
- **Primary metrics:** violation precision/recall, compliant-script false-positive rate, false-negative count/rate, borderline escalation rate, structured-output validity, and cost per script.

The final metric formulas and treatment of borderline cases will be frozen before running the evaluation.

## Decisions to confirm

- Primary reviewer/user
- English-only or bilingual (English + Chinese)
- In-scope brand constraints
- Whether the prototype is a command-line evaluator or reviewer-facing UI
