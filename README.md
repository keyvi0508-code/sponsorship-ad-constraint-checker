# CHANEL Sponsorship Script Brand-Rule Checker

An English-only course-project prototype that helps a human reviewer check a proposed sponsored-video script against CHANEL's publicly available creator guidelines. It compares an actually measured keyword-search baseline with an AI-assisted reviewer and routes ambiguous cases to a person.

## Scope

The MVP focuses on disclosure wording and sponsor identity, placement represented in structured script fields, and contextual competitor criticism. It does not claim to know CHANEL's private campaign brief or required selling points. See [scope](scope.md), [decisions](decisions.md), [evaluation plan](plan.md), and [brand-source assessment](docs/brand_source_research.md).

## Evaluation

The planned primary set has 30 English-language instances: 10 compliant, 10 violating, and 10 borderline. Labels and rationales will be written and frozen before running either system. The keyword baseline and AI reviewer will run on the same cases. No results are claimed until both have actually been run.

## Planned course deliverables

- Problem statement and scope
- Business/technical trade-off analysis
- Reproducible code and labeled evaluation data
- Measured results, including false positives, false negatives, borderline handling, structured-output validity, and API cost per script
- Recorded demo
- Self-appraisal/cover page if required by the course instructions

## Source and use limits

The source is CHANEL's official [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/), accessed 2026-09-29. The prototype is an independent academic project, not affiliated with or approved by CHANEL. It reviews text fields supplied by the user; it cannot verify actual screen visibility, spoken audibility, or video timing. It supports human review and is not legal advice.
