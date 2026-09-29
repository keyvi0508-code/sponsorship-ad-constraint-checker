# Project scope — CHANEL Creator Guideline Script Checker

## Problem

Reviewers checking sponsored short-form video scripts against creator guidelines may miss meaning and context when they rely on keyword search. An LLM can interpret context but may over-flag acceptable language. This project compares both approaches on a controlled bilingual evaluation while leaving final decisions to a human.

## User and use case

A creator-partnership or brand-content reviewer checks a proposed English or Chinese sponsored-video script before publication against CHANEL's publicly available Social Media Guidelines. This is an academic prototype; it is not affiliated with CHANEL and does not claim to reproduce CHANEL's private campaign approval process.

## Source-grounded MVP rules

Only rules in CHANEL's public guide are in scope:

1. **Disclosure identity and wording:** the script should clearly disclose the creator's material connection. If multiple brands appear and a generic disclosure would not make CHANEL's sponsorship clear, the sponsor should be identified. The guide gives acceptable and insufficient examples.
2. **Disclosure placement in the supplied script fields:** the disclosure should appear with the endorsement and at the beginning/above the fold, rather than only in the profile or behind a “more” action. For video, review disclosure text represented in spoken, on-screen, and caption fields. A text-only prototype cannot verify actual visibility, contrast, duration, or audibility.
3. **Competitor criticism and impartiality:** when a creator connected to CHANEL criticizes a competitor, the script must not imply that the opinion is impartial. A neutral competitor mention alone is not automatically a violation.

The guide also recommends truthful first-hand opinions and verifiable factual statements. The MVP may flag claims that need supporting evidence for human review, but it will not independently certify whether a product claim is true unless an authoritative reference is explicitly supplied.

## Input and output

Input is a structured script with language, platform/format, caption, spoken lines, planned on-screen text, and scene/placement notes. Output is PASS, FLAG, or HUMAN_REVIEW, with a source rule ID, quoted evidence, and a concise rationale. The tool supports reviewer decisions; it does not approve or publish content automatically.

## Evaluation commitment

Primary evaluation: 30 script instances, balanced across 10 compliant, 10 clearly violating, and 10 borderline cases. Each label group contains 5 English and 5 Chinese cases. The 30 instances are organized as 15 paired scenarios with bilingual adaptations; paired-language dependence will be disclosed in the report. Ground-truth labels and rationales are frozen before model evaluation. The keyword baseline and AI system run on the same set.

Any extra development or stress cases are reported separately. Report both error directions, class- and language-specific results, borderline escalation, valid structured-output rate, API model/token use, and cost per script.

## Out of scope

- Private campaign briefs, unpublished product selling points, or an invented CHANEL competitor blacklist.
- Video/audio ingestion or measurement of actual visual prominence, timing, or sound.
- Legal advice, automatic publishing, and final brand approval.
- Claims that the tool is CHANEL-approved or will catch every breach.
