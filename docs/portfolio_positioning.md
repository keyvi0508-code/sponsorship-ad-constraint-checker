# Portfolio positioning: Creator Content Review Workbench

## Product statement

I built a local prototype that helps a creator-partnership reviewer screen sponsored short-video scripts against a small, source-grounded rule set. It compares a deterministic keyword baseline with an AI-assisted reviewer, shows evidence and uncertainty, and keeps the final disposition with a person.

## Product workflow

1. A reviewer loads a saved example or enters caption, spoken copy, on-screen copy, brand context, and first-hand-use metadata.
2. The keyword baseline returns a free, explainable first pass.
3. The reviewer may request an AI review after seeing an estimate and confirming that two API calls may incur a charge.
4. The interface compares verdicts and shows quoted evidence, rule IDs, and rationales.
5. A human selects a disposition. This demo does not persist the decision.

The saved example and dashboard use 30 fictional extension cases. On that set, the AI scored 23/30 (76.7%) and the keyword baseline scored 20/30 (66.7%). The AI flagged all 10 clear violations and made no `FLAG` decisions on clean cases, while sending 2 clean cases and 5 borderline cases to `HUMAN_REVIEW`. These are descriptive development results on synthetic data, not a production performance claim.

## Why the project is relevant to content-governance product work

Recent TikTok career listings describe LIVE safety and content-ecosystem product work in terms of AI-assisted review, safety or quality metrics, cross-functional policy/operations/engineering collaboration, creator experience, and model evaluation. This project gives me a small, demonstrable example of policy-to-product translation, baseline comparison, error analysis, human escalation, and cost-aware use of an external model. It does not establish that I have shipped a production moderation system.

- [TikTok Product Manager — LIVE Safety, Singapore](https://lifeattiktok.com/search/7584722257312057653) emphasizes product strategy, safety and operational metrics, creator ecosystems, and AI/ML-supported detection.
- [TikTok AI Product Manager Graduate — Content Ecosystem](https://lifeattiktok.com/search/7667472978298767621) emphasizes content understanding/classification, precision and recall, annotation/data tools, and collaboration with Policy, Trust & Safety, Engineering, Data Science, and Operations.
- [TikTok AI Product Manager Project Intern — LIVE Ecosystem Governance](https://lifeattiktok.com/search/7598849238706735365) describes governance tools, moderation mechanisms, ecosystem analysis, and cross-team product iteration.

The closest fit is creator/content policy review and brand safety. The prototype is a pre-publication text review tool. It does not evaluate live video, latency, multimodal signals, adversarial evasion, or platform-scale operations, so I should describe it as adjacent experience when applying to LIVE safety roles.

## Interview narrative

> I started from a reviewer problem: literal search can locate explicit phrases but struggles with meaning and context, while a language model can over-escalate acceptable content. I built a small review workbench that puts both methods beside each other, cites the text evidence, and sends ambiguous cases to a human. I evaluated both methods on the same balanced 30-case extension: the AI was correct on 23 cases versus 20 for the keyword baseline, but this was synthetic development evidence rather than proof of real-world lift. The interface makes the trade-offs visible, including clean-case escalation, borderline handling, and estimated API cost. My next validation step would be a permissioned, independently labeled set and reviewer workflow study before making any production claim.

## Current portfolio gaps

- I have not interviewed working reviewers or measured their current review time and workload.
- The cases are fictional and the reviewer provenance for the blind-label return was not provided.
- The dashboard reports small-sample outcomes and the extension prompt had been revised after earlier outputs.
- The local interface does not save review history, support team accounts, provide a configurable ruleset editor, or integrate with a campaign platform.
- The prototype has not been deployed publicly or security-reviewed for multi-user use.
- It reviews structured text only; it does not inspect video, audio, or real-time LIVE content.

I will keep those gaps visible in the demo and treat them as the next discovery and validation questions, not as implemented features.
