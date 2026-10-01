# Brand policy packs

## Product boundary today

The current Creator Content Review Workbench supports one policy pack: a narrow, project-defined interpretation of CHANEL's public [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/). The implementation, rule IDs, examples, labels, and reported evaluation results are CHANEL-specific. They do not establish behavior for another brand.

If a reviewer submits work for a brand that has no approved policy pack, the product should stop and say that the brand is not configured. It must not reuse CHANEL's rules, imply coverage, or return `PASS` by default.

## Product direction

Keep one review workflow and load a separate policy pack for each brand. The workflow can still accept captions, spoken copy, on-screen text, and context; collect evidence; apply rule-specific decisions; and route uncertainty to a human. The selected pack supplies the requirements and their scope.

| Shared review workflow | Brand-specific policy pack |
|---|---|
| Input validation and text-field handling | Brand identity and approved source documents |
| Evidence extraction and quoted spans | Source-grounded rule IDs and exact excerpts |
| `PASS`, `FLAG`, and `HUMAN_REVIEW` workflow | Applicability conditions and decision thresholds |
| Human disposition and audit event shape | Brand-specific examples and boundary cases |
| Cost controls and technical observability | Effective date, version, reviewer/owner approval |

Shared output labels do not make the underlying rules interchangeable. A result should identify the selected brand, policy-pack version, and rule IDs that support it.

Campaign-specific mandatory selling points belong to a separately supplied, approved campaign brief, not the public brand guideline pack. The current workbench has no such brief; it displays `Not provided / mandatory selling points not evaluated` and includes that status in the exported review record. A public-guideline `PASS` must not be interpreted as campaign approval. A future brief workflow would require the brand owner to provide the exact requirements, effective campaign, and approval/version information before those checks can run.

## Minimum policy-pack record

Before a brand can be enabled, its pack should record:

- stable `brand_id`, display name, jurisdiction/market, and supported language;
- authoritative source URLs or approved documents, access date, and source version/effective date where available;
- rule IDs namespaced by brand, exact source excerpt, plain-language interpretation, and applicability conditions;
- what counts as `FLAG`, `HUMAN_REVIEW`, or `PASS`, including facts the system must not infer;
- calibration examples and known limits, each traceable to the source rule;
- policy owner/reviewer approval and a content hash so a changed source produces a new pack version.

Do not invent private campaign requirements or treat a general industry convention as a brand rule. If a source is missing, conflicting, or too vague to operationalize, keep that rule disabled or route cases to human review.

## Review routing

1. The reviewer selects the brand and campaign context.
2. The app confirms an approved, active policy pack exists for that brand and language.
3. Each applicable rule is assessed separately with exact evidence and its source reference.
4. The overall verdict is `FLAG` if any rule clearly flags; otherwise `HUMAN_REVIEW` if any applicable rule is unresolved; otherwise `PASS`.
5. The audit record stores the policy-pack ID/version with the rule-level results. A later policy update does not rewrite historical decisions.

If multiple brands appear in one script, apply only the selected sponsor's pack unless the reviewer explicitly requests a separate review under another configured pack. Keep each brand's result distinct; do not merge conflicting rules into a single unlabeled verdict.

## Evaluation when adding a brand

Every new policy pack needs its own source review, operational guide, independently labeled cases, and keyword/AI evaluation. Do not transfer CHANEL accuracy, labels, or examples as evidence of performance for another brand. Freeze the new pack and evaluation set before measuring; after any policy or prompt revision, report the new run separately.

## Current implementation status

This is a product architecture direction, not a claim that multi-brand support is implemented. The local prototype has no policy selector, policy editor, tenant isolation, or multi-brand evaluation. Current evidence covers only the CHANEL pack.
