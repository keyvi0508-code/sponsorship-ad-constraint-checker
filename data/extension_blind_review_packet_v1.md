# Blind review packet — 30 additional cases (v1)

## Instructions

Independently assign each fictional English short-video script one verdict: `PASS`, `FLAG`, or `HUMAN_REVIEW`. Record applicable project rule IDs and a brief rationale tied to exact script evidence. Do not infer facts not supplied. These cases are synthetic academic examples, not actual CHANEL campaigns. The project is not affiliated with CHANEL.

## Source-grounded project rules

- `CH-DISC-01`: Clearly disclose the material connection. When multiple brands appear, identify CHANEL as sponsor. The guide lists `#ad`, `#sponsored`, `#paid`, `#ChanelPartner`, and `#GiftFromChanel` as examples; bare thanks, `#partner`, `#ambassador`, abbreviations such as `#spon`, and `#gifted`/`#hosted` are insufficient alone.
- `CH-DISC-02`: Put disclosure near the endorsement and at the beginning. Caption line 2 is within this project’s first-two-lines window. Disclosure should match the medium: spoken for spoken endorsement, on-screen for visual endorsement. A script cannot prove final visibility, legibility, duration, or audibility.
- `CH-CONTEXT-01`: A CHANEL-connected creator must not imply that criticism of a CHANEL competitor is impartial. Negative or neutral competitor mentions alone are not automatically violations. Clearly personal preference may pass; explicit claims of impartiality may flag; genuinely unclear comparison framing should go to human review.
- `CH-CLAIM-01`: Product opinions/reviews require actual first-hand use. Objective factual claims should be truthful, supportable, and verifiable. Unknown use or missing substantiation warrants human review; do not infer that an unsupported claim is false.

Project rule IDs are local identifiers mapped to numbered sections of CHANEL’s public [Social Media Guidelines](https://www.chanel.com/us/makeup/social-media-guidelines/) (accessed 2026-09-30); they are not official CHANEL identifiers. These operational summaries incorporate the project’s v2 rubric clarification.

## Cases

### BLIND-84

```json
{
  "case_id": "BLIND-84",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "A look at a soft rose shade.",
    "#sponsored · CHANEL sent this lipstick for me to try."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "CHANEL sent this lipstick for me to try. Here is the shade in daylight."
      ],
      "on_screen_text": [
        "Gift from CHANEL · #ad"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-61

```json
{
  "case_id": "BLIND-61",
  "language": "en",
  "format": "short_video",
  "multiple_brands": true,
  "caption": [
    "#ad",
    "Two brands, one evening routine."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "Here is my routine with CHANEL and another brand."
      ],
      "on_screen_text": [
        "#ad"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-91

```json
{
  "case_id": "BLIND-91",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "I love how this foundation feels on my skin."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "I love how this foundation feels on my skin."
      ],
      "on_screen_text": [
        "CHANEL foundation"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-94

```json
{
  "case_id": "BLIND-94",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "My side-by-side wear test: the rival brand faded sooner."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "Sponsored by CHANEL. In my side-by-side wear test, the rival brand faded sooner."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-45

```json
{
  "case_id": "BLIND-45",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A sponsored product close-up."
  ],
  "scenes": [
    {
      "verbal_endorsement": false,
      "visual_endorsement": true,
      "spoken_text": [],
      "on_screen_text": [
        "#ad · CHANEL (planned overlay; duration and final placement not yet confirmed)"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-96

```json
{
  "case_id": "BLIND-96",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A wear test of CHANEL and a rival lipstick."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "This is a CHANEL-sponsored wear test. The rival lipstick seemed to fade sooner to me."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-66

```json
{
  "case_id": "BLIND-66",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "Watch this blush blend."
  ],
  "scenes": [
    {
      "verbal_endorsement": false,
      "visual_endorsement": true,
      "spoken_text": [],
      "on_screen_text": [
        "CHANEL blush · shade 03"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-43

```json
{
  "case_id": "BLIND-43",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#sponsored",
    "A guide to applying this face powder."
  ],
  "scenes": [
    {
      "verbal_endorsement": false,
      "visual_endorsement": true,
      "spoken_text": [],
      "on_screen_text": [
        "#sponsored"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-56

```json
{
  "case_id": "BLIND-56",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "My own test suggests this rival fragrance lasts longer."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "This video is sponsored by CHANEL. My own test suggests the rival fragrance lasts longer."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-41

```json
{
  "case_id": "BLIND-41",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "Thanks CHANEL for the beautiful box!",
    "My unboxing and first impression."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "Thanks, CHANEL, for sending this. I love the packaging."
      ],
      "on_screen_text": [
        "CHANEL unboxing"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-73

```json
{
  "case_id": "BLIND-73",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#CHANELPartner",
    "A neutral comparison of packaging shapes."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "This video is a paid partnership with CHANEL. The rival brand uses a square bottle; CHANEL uses a round one."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-58

```json
{
  "case_id": "BLIND-58",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A quick tip for keeping lipstick in place."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "CHANEL lipstick lasts 24 hours on everyone."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-69

```json
{
  "case_id": "BLIND-69",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A personal color note: this shade looked warmer on me than I expected."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "Sponsored by CHANEL. This shade looked warmer on me in daylight."
      ],
      "on_screen_text": [
        "Paid partnership with CHANEL"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-88

```json
{
  "case_id": "BLIND-88",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "For my dry skin, this balm felt comfortable during a windy walk."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "This video is sponsored by CHANEL. For my dry skin, this balm felt comfortable."
      ],
      "on_screen_text": [
        "#ad · CHANEL"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-75

```json
{
  "case_id": "BLIND-75",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#paid · CHANEL",
    "A close-up of the compact in natural light."
  ],
  "scenes": [
    {
      "verbal_endorsement": false,
      "visual_endorsement": true,
      "spoken_text": [],
      "on_screen_text": [
        "Paid partnership with CHANEL"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-47

```json
{
  "case_id": "BLIND-47",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "My review: I tested this cream for a week and it never caused irritation."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "Sponsored by CHANEL. I tested this cream for a week and it never caused irritation."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-53

```json
{
  "case_id": "BLIND-53",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A quick look at this mascara."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "CHANEL mascara is clinically proven to double lash length in seven days."
      ],
      "on_screen_text": [
        "Clinically proven: 2x lash length"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-80

```json
{
  "case_id": "BLIND-80",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#partner",
    "My review of CHANEL Rouge Allure."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "I recommend this lipstick."
      ],
      "on_screen_text": [
        "CHANEL Rouge Allure"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-98

```json
{
  "case_id": "BLIND-98",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · Paid partnership with CHANEL",
    "I wore this lipstick through dinner; the color stayed comfortable for me."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "This video is sponsored by CHANEL. I wore this shade through dinner and liked how it felt."
      ],
      "on_screen_text": [
        "#ad · CHANEL"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-51

```json
{
  "case_id": "BLIND-51",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "A quick review of CHANEL skincare.",
    "The cream felt light on my skin.",
    "#ad"
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "I recommend this cream for sensitive skin."
      ],
      "on_screen_text": [
        "CHANEL skincare"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-87

```json
{
  "case_id": "BLIND-87",
  "language": "en",
  "format": "short_video",
  "multiple_brands": true,
  "caption": [
    "#ad",
    "Today's edit features CHANEL and another makeup label."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "Paid partnership with CHANEL. Here are the two looks."
      ],
      "on_screen_text": [
        "CHANEL partner · #ad"
      ]
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-63

```json
{
  "case_id": "BLIND-63",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "My review: I tried this serum and recommend it."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "I have never tried this serum, but my review is that it works beautifully."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": false,
  "claim_reference_sources": []
}
```

### BLIND-76

```json
{
  "case_id": "BLIND-76",
  "language": "en",
  "format": "short_video",
  "multiple_brands": true,
  "caption": [
    "#paid",
    "My routine with CHANEL and another luxury house."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": true,
      "spoken_text": [
        "This routine is sponsored."
      ],
      "on_screen_text": [
        "#paid"
      ]
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-67

```json
{
  "case_id": "BLIND-67",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#GiftFromCHANEL",
    "A quiet morning routine."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "I partnered with CHANEL for this video. I used this hand cream every morning this week."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-74

```json
{
  "case_id": "BLIND-74",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "This lipstick is the best choice for every skin tone."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "This lipstick is guaranteed to suit every skin tone."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": [
    "A CHANEL product page is named, but no supporting passage is supplied."
  ]
}
```

### BLIND-78

```json
{
  "case_id": "BLIND-78",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "An unbiased review: the competitor's formula is objectively inferior."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "Sponsored by CHANEL. This is a completely impartial review; the competitor's formula is objectively inferior."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-50

```json
{
  "case_id": "BLIND-50",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#spon",
    "First impressions of a new CHANEL lip color."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "#spon—this shade is lovely."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-64

```json
{
  "case_id": "BLIND-64",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad",
    "A comparison of two foundations."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "Sponsored by CHANEL. The rival foundation is poorly made, and this is an impartial assessment."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```

### BLIND-46

```json
{
  "case_id": "BLIND-46",
  "language": "en",
  "format": "short_video",
  "multiple_brands": true,
  "caption": [
    "#CHANELPartner · Paid partnership with CHANEL",
    "Comparing two evening looks."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "This segment is sponsored by CHANEL. I will show a CHANEL look alongside another brand."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": null,
  "claim_reference_sources": []
}
```

### BLIND-42

```json
{
  "case_id": "BLIND-42",
  "language": "en",
  "format": "short_video",
  "multiple_brands": false,
  "caption": [
    "#ad · CHANEL",
    "A short wear test with another luxury house's lipstick."
  ],
  "scenes": [
    {
      "verbal_endorsement": true,
      "visual_endorsement": false,
      "spoken_text": [
        "Sponsored by CHANEL. In a short wear test, the other lipstick transferred more."
      ],
      "on_screen_text": []
    }
  ],
  "creator_used_product": true,
  "claim_reference_sources": []
}
```
