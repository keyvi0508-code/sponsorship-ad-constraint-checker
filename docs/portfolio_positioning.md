# Creator Content Review Workbench

## Product brief

Creator Content Review Workbench helps a creator-partnership reviewer screen sponsored short-video scripts before publication. It compares a deterministic keyword baseline with an AI-assisted review, shows the text evidence behind each finding, and routes uncertain cases to a human decision-maker.

The current local prototype applies a narrow rule set derived from CHANEL's public [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/). It is independent and does not represent CHANEL or any private campaign policy.

## Intended user and problem

The primary user is a reviewer checking creator-submitted copy across captions, spoken scripts, and planned on-screen text. Literal search can catch explicit phrases but miss context; AI can interpret context but may over-escalate acceptable copy. The workbench makes this trade-off visible and keeps the reviewer accountable for the outcome.

## Product flow

1. Load a saved example or enter script text and review context.
2. Run a free keyword check for explicit signals.
3. Optionally request an AI review after seeing and confirming its estimated cost.
4. Compare verdicts, evidence quotes, rule IDs, and rationales.
5. Record a local human disposition or escalate uncertainty.

The saved example makes no API call. Draft text and reviewer decisions remain in the current session and are not persisted. A live AI review uses two sequential requests.

## Product decisions

- Evidence before verdict: the model first extracts relevant assertions; the second stage applies the decision rubric.
- Abstain on ambiguity: the system can return HUMAN_REVIEW instead of forcing a pass or flag.
- Human accountability: AI findings support review; they do not approve content.
- Cost visibility: a preflight estimate and explicit confirmation gate every live review.
- Bounded scope: the prototype checks text. It does not inspect video visibility, audio, timing, or creator conduct.

## Evaluation snapshot

On a balanced 30-case synthetic extension, the AI reviewer scored 23/30 (76.7%), compared with 20/30 (66.7%) for the keyword baseline. It flagged all 10 clear violations and did not flag any clean cases, while escalating 2 clean and 5 borderline examples for human review. Estimated token cost was approximately US$0.0079 per case.

This is development evidence, not a production claim. The dataset is fictional, the sample is small, and the prompt had been revised after earlier results. The comparison does not establish real-world lift or reviewer efficiency.

## Portfolio relevance

The project demonstrates policy-to-product translation, human-in-the-loop workflow design, baseline comparison, model evaluation, error analysis, and cost-aware API use. It is most directly relevant to creator content review, brand safety, and content-governance product work. It is adjacent experience for LIVE safety roles: this prototype does not handle real-time latency, video/audio understanding, adversarial behavior, or platform-scale operations.

## Interview narrative

> I built a review workbench for sponsored creator scripts because literal keyword search misses context, while an AI reviewer can over-escalate acceptable copy. The interface shows keyword and AI findings side by side, cites evidence, and leaves ambiguous cases and final decisions with a person. On a balanced 30-case synthetic extension, the AI scored 23/30 versus 20/30 for the baseline. I treat that as a development result, not proof of production impact. My next step would be to validate the workflow with reviewers and a permissioned, independently labeled dataset before expanding the rules or claiming operational gains.

## Next product validation

- Interview reviewers and map the existing workflow, time spent, and common disagreements.
- Create a permissioned dataset with independent labels and documented adjudication.
- Test whether evidence-first results and human escalation improve review quality or time without increasing misses on clean content.
- Explore a configurable rule set and persistent audit history only after privacy, access, and retention requirements are understood.
- Evaluate video/audio and real-time requirements separately before positioning this as a LIVE moderation tool.

The local demo has no team accounts, persistent review history, rule editor, or campaign-system integration and has not been deployed or reviewed for multi-user security.
