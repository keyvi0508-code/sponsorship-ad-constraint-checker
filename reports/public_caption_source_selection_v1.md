# Public-caption source selection, before model review

**Status:** 23 source-linked, English-dominant 2026 Instagram Reels selected and caption-captured on 2026-10-02. No keyword or AI caption-review output was inspected before this selection was locked. The [development data](../data/real_public_reels_caption_development_v1.jsonl) and [SHA-256 manifest](../data/real_public_reels_caption_development_v1_manifest.json) preserve source URLs, selected order, access date, full desktop-visible caption wording, discovery route, and unknown evidence fields.

## Selection method

This is a purposive convenience sample, not a random sample of CHANEL partnerships. The first ten posts came from the previously documented query `site:instagram.com/reel/ "#chanelpartner" "@welovecoco"`; their original captions were rechecked on Instagram. To reduce reliance on that one partnership hashtag, additional candidates came from three Google discovery queries, each opened at its original Instagram Reel URL before inclusion:

| Discovery route | Query used | Selected |
|---|---|---:|
| Partnership marker | `site:instagram.com/reel/ "#chanelpartner" "@welovecoco"` | 10 |
| Gift-related wording | `site:instagram.com/reel/ "chanel" "gifted"` | 6 |
| Brand/product mention | `site:instagram.com/reel/ "@chanel.beauty" "#chanelbeauty" -"#chanelpartner" -"#gifted"` | 3 |
| First-hand experience wording | `site:instagram.com/reel/ "chanel" "i tried" makeup` | 4 |

The search exclusions in the third query did not reliably exclude every tagged post. Inclusion was based on the **original Reel**, not its search snippet: the post had to be publicly accessible, posted in 2026, English-dominant, and visibly about a CHANEL product or creator interaction. Older posts, a production-credit post without a creator endorsement, unavailable captions, duplicate URLs, and clearly off-scope material were left out. This selection enriches disclosure and experience wording intentionally; it cannot estimate their natural frequency. One creator appears twice. The exact text was read from the visible original-post caption DOM; no video audio, overlays, mobile fold, product use, or private contract terms were verified. The Reel itself could later change.

## What the locked inventory says, before a model run

There are 23 posts from 22 creators. A creator-authored partnership marker appears in 11 captured captions, gift wording in seven, and neither signal is established in five. These are **publication signals**, not independent verification of a paid relationship. The deterministic intake gate finds one of its listed acceptable disclosure examples in 11 captions, one of its listed insufficient examples in four, and no listed marker in eight. Its literal patterns do not treat the plain word “Gifted” as `#gifted`, which is an observable baseline limitation. A missing listed marker is not proof of a disclosure breach; video disclosures and compensation facts were not checked.

The [intake protocol](../docs/public_content_intake_protocol.md) explains why full-video status is `UNKNOWN` for all 23. The intake counts are **not** AI predictions, reference labels, or accuracy results. After the source lock, a separately versioned [keyword and AI caption-only review](public_caption_ai_pilot_v1.md) was run, preserving raw suggestions separately from the evidence-gated full-review status. The selection and checksum above remain the **pre-run** record rather than being rewritten after seeing outputs.

This development file contains creator-authored caption text to make the private analysis inspectable. Review that text and its publication rights before making a portfolio repository public; links and short evidence excerpts may be more suitable for a public edition.
