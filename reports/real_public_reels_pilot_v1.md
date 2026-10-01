# Public-content feasibility pilot (caption observations only)

**Status: source-linked external-data feasibility check; not a model accuracy evaluation.** On 2026-10-01, ten original public Instagram Reels were opened and their visible creator, date, caption, and source URL were checked. They represent nine creators. The source inventory is [`real_public_reels_pilot_v1.jsonl`](../data/real_public_reels_pilot_v1.jsonl); run `python scripts/summarize_real_pilot.py` to reproduce the counts below.

## Why this pilot exists

The 60-case evaluation set contains project-authored fictional drafts. This pilot tests whether real, traceable CHANEL-related creator material is available and what evidence a caption-only collection can actually support. It does **not** change, pool with, or validate the synthetic scores. Public finished Reels are also a different input from a brand's unpublished script.

The ten links were the first ten original Reel results shown for the discovery query `site:instagram.com/reel/ "#chanelpartner" "@welovecoco"` on 2026-10-01. Search ranking is a convenience sample, not random selection. Each result was checked on Instagram itself; search excerpts were not treated as source text. No video, image, or full caption was copied into the repository.

## Observed source inventory

| ID | Original Reel | Creator | Public-caption disclosure signal observed |
|---|---|---|---|
| REAL-01 | [Original post](https://www.instagram.com/reel/DWmHcr0DiuH/) | @elnaz_golrokh | `#CHANELpartner` |
| REAL-02 | [Original post](https://www.instagram.com/reel/DcdwI1ngDM7/) | @briannesikorski | `#chanelpartner` |
| REAL-03 | [Original post](https://www.instagram.com/reel/Dd1Qw-ORB5z/) | @alexisbadiyi | `#CHANELpartner` |
| REAL-04 | [Original post](https://www.instagram.com/reel/Dd7gK0wo8uj/) | @katekimshah | `#gifted` plus tags of CHANEL-linked accounts; no brand-specific disclosure phrase in the visible caption |
| REAL-05 | [Original post](https://www.instagram.com/reel/DcekOBIhtk_/) | @elnaz_golrokh | `#chanelpartner` |
| REAL-06 | [Original post](https://www.instagram.com/reel/DcL3dk2OK1j/) | @willowwpreston | `#chanelpartner` |
| REAL-07 | [Original post](https://www.instagram.com/reel/Dbv5qp9NON0/) | @fabiolacolmenaresp | `#CHANELpartner` |
| REAL-08 | [Original post](https://www.instagram.com/reel/DWjsSFMRPuk/) | @tyronmachhausen | `#chanelpartner` |
| REAL-09 | [Original post](https://www.instagram.com/reel/Dd4mANdyrqc/) | @mananamariee | `#CHANELPartner` |
| REAL-10 | [Original post](https://www.instagram.com/reel/DWcIW_nEaiR/) | @wheatatreat | `#CHANELpartner` |

Nine of ten visible captions contained a CHANEL-specific partnership marker. The remaining caption used a generic `#gifted` marker while tagging CHANEL-linked accounts. This is a **caption observation**, not a finding that the Reel breached a rule. In fact, that fourth case appeared under a search query for `#chanelpartner` but the original post's current visible caption did not contain it: a search result can be stale or describe information absent from the current caption.

## What is still unknown

The [CHANEL Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/) accept `#ChanelPartner` as a disclosure wording example and say `#gifted` alone is insufficient. They also require disclosure to be conspicuous, close to the endorsement, and in the video when the endorsement is in video. This pilot did not verify complete video frames, spoken audio, exact on-screen duration, mobile caption fold, private compensation terms, actual product use, or claim substantiation. None of the ten posts has a defensible full `PASS`, `FLAG`, or `HUMAN_REVIEW` gold label in this dataset; `full_policy_verdict` is `null` for every row. A reviewer with the full asset and relevant private facts would have to make those decisions. The post's own tag is evidence of what the creator published, not independent proof of the relationship terms.

Because discovery targeted a partnership hashtag, the sample favors posts that already signal a connection. It cannot measure how often a system catches missing disclosures. Posts may be edited or removed after the access date. An observed caption marker is not equivalent to a complete published-video audit or a pre-publication script review.

## Product implication and next evaluation gate

Real examples are obtainable, but they cannot simply be pasted into the existing text-only scorer and treated as labelled test cases. The workbench needs an intake state that separates **observed caption** from **unverified audio, video overlay, product use, and campaign facts**. Until those fields are checked, its outcome should be “evidence incomplete / human review required,” not `PASS`. The next meaningful performance study needs permissioned draft scripts or a full-media review protocol, an independently adjudicated rule-specific reference set, and a frozen prompt before any accuracy comparison. This pilot establishes source feasibility and exposes a data-collection limitation; it does not establish model quality.
