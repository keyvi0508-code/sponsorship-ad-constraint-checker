# Project scope (draft in progress)

## User problem

A brand or creator-partnership reviewer needs to check a sponsored-video script against brand rules. A literal Ctrl+F check can miss paraphrases, implications, and context; a language model can interpret meaning but can also over-flag compliant text. This project will compare the two methods and keep final decisions with a human reviewer.

## Confirmed direction

- Use real brand rules that are publicly available from an authoritative brand source.
- Evaluate scripts in both English and Chinese.
- Cite and distinguish the source text from the project team's operational interpretation of each rule.
- Do not represent a constructed test brief as a brand's private campaign brief.

## Pending

- Select the brand and primary official source.
- Choose a narrow set of rules that can be operationalized and evaluated fairly in both languages.
- Confirm whether the prototype is CLI-only or includes a simple reviewer interface.

## Evaluation commitment

The primary set is planned as 30 balanced cases (10 compliant, 10 violating, 10 borderline), with labels and rationales frozen before model runs. The keyword baseline and AI-assisted system will be run on exactly the same set. Any extra tuning or stress cases will be reported separately.

## Product boundary

The tool will support a human review decision. It will not approve or publish sponsored content automatically, and it is not legal advice.
