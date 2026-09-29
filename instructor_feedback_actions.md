# Instructor feedback translated into project actions

This document records the actionable feedback received on the proposal. It is a project checklist, not an additional course instruction.

| Feedback | Project response |
|---|---|
| The core Ctrl+F argument is strong: literal search misses slang, metaphor, and implicit references. | Compare an actually run keyword-search baseline with a meaning-aware method on the same fixed scripts. Include paraphrase and implicit-reference examples. |
| Keep Level 1 JSON assertions separate from Level 2 judgement. | Make rule extraction/checking and judgement distinct stages, and validate machine-readable output separately from semantic accuracy. |
| Ten scripts are too few and the author writes both prompt and scripts. | Use a larger balanced primary evaluation set (30 is the working plan), with labels and rationales fixed before model runs. Disclose that examples are synthetic and authored for the project. |
| Test both non-compliant and clean scripts. | Report false positives and false negatives with the correct labels; do not evaluate only on intentionally failing cases. |
| A claimed keyword baseline must be measured. | Implement and run it on the same primary test set as the AI-assisted system. |
| Include Class 5 API cost because an external API is rented. | Record model/provider, token usage, price source/date, and cost per script. |

## Reporting discipline

- Keep the primary 30-case results separate from any development or stress-test data.
- Do not tune prompts against the final primary set after looking at its results. If iteration is needed, create a separate development set and document the change.
- Report limitations and failure examples, not only aggregate accuracy.
