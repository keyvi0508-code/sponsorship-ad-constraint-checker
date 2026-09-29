# Project scope — CHANEL Creator Guideline Script Checker

## Problem

Reviewers checking sponsored short-form video scripts against creator guidelines may miss meaning and context when relying on keyword search. An LLM can interpret context but may over-flag acceptable language. This project compares both approaches on a controlled English-only evaluation while leaving final decisions to a human.

## User and use case

A creator-partnership or brand-content reviewer checks a proposed English sponsored-video script before publication against CHANEL's publicly available Social Media Guidelines. This is an academic prototype, not affiliated with CHANEL and not a reproduction of its private campaign approval process.

## Source-grounded MVP rules

1. **Disclosure identity and wording:** disclose the creator's material connection clearly. If multiple brands appear and a generic disclosure would not make CHANEL's sponsorship clear, identify the sponsor. The guide gives acceptable and insufficient examples.
2. **Disclosure placement in supplied script fields:** disclosure should appear with the endorsement and at the beginning/above the fold, not only in the profile or behind a “more” action. For video, evaluate disclosure text represented in spoken, on-screen, and caption fields. A text-only prototype cannot verify actual visibility, contrast, duration, or audibility.
3. **Competitor criticism and impartiality:** when a creator connected to CHANEL criticizes a competitor, the script must not imply that the opinion is impartial. A neutral competitor mention alone is not automatically a violation.

The guide also recommends truthful first-hand opinions and verifiable factual statements. The prototype may route claims lacking an authoritative reference to HUMAN_REVIEW; it will not independently certify a claim as true or false without evidence.

## Input and output

Input is a structured English script with platform/format, caption, spoken lines, planned on-screen text, and scene/placement notes. Output is PASS, FLAG, or HUMAN_REVIEW, with a source rule ID, quoted evidence, and concise rationale. The tool supports reviewer decisions; it does not approve or publish content.

## Evaluation commitment

Primary evaluation: 30 English-language script instances, balanced across 10 compliant, 10 clearly violating, and 10 borderline cases. Ground-truth labels and rationales are written and frozen before model evaluation. The keyword baseline and AI system run on the same set. Any additional development or stress cases are reported separately.

Report false positives, false negatives, class-specific results, borderline escalation, valid structured-output rate, API model/token use, and cost per script.

## Out of scope

- Non-English scripts and translation comparisons.
- Private campaign briefs, unpublished product selling points, or an invented CHANEL competitor blacklist.
- Video/audio ingestion and verification of actual screen prominence or sound.
- Legal advice, automatic publishing, and final brand approval.
- Claims that the tool is CHANEL-approved or catches every breach.
