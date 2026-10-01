"""Verify deterministic keyword decisions on disclosure and context examples."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.baseline import extract_level1_assertions, review_with_keyword_baseline


class KeywordBaselineTests(unittest.TestCase):
    def base_case(self):
        return {
            "case_id": "TEST-01",
            "language": "en",
            "format": "short_video",
            "multiple_brands": False,
            "caption": ["#ChanelPartner #ad"],
            "scenes": [{
                "verbal_endorsement": True,
                "visual_endorsement": True,
                "spoken_text": ["Paid partnership with Chanel."],
                "on_screen_text": ["Paid partnership with Chanel"],
            }],
        }

    def test_clear_early_disclosure_passes(self):
        result = review_with_keyword_baseline(self.base_case())
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["findings"], [])

    def test_missing_caption_disclosure_is_flagged(self):
        case = self.base_case()
        case["caption"] = ["A new look for tonight."]
        case["scenes"][0]["spoken_text"] = []
        case["scenes"][0]["on_screen_text"] = []
        result = review_with_keyword_baseline(case)
        self.assertEqual(result["verdict"], "FLAG")
        self.assertIn("CH-DISC-01", {x["rule_id"] for x in result["findings"]})

    def test_generic_tag_is_not_enough_when_multiple_brands_appear(self):
        case = self.base_case()
        case["multiple_brands"] = True
        case["caption"] = ["#ad"]
        case["scenes"][0]["spoken_text"] = []
        case["scenes"][0]["on_screen_text"] = []
        result = review_with_keyword_baseline(case)
        self.assertEqual(result["verdict"], "FLAG")

    def test_level1_assertions_do_not_make_the_level2_verdict(self):
        case = self.base_case()
        assertions = extract_level1_assertions(case)
        self.assertIn("disclosure_mentions", assertions)
        self.assertNotIn("verdict", assertions)

    def test_competitor_criticism_with_impartiality_claim_is_flagged(self):
        case = self.base_case()
        case["caption"] = ["#ChanelPartner #ad"]
        case["scenes"][0]["spoken_text"] = [
            "This is an unbiased review: the competitor's product is overpriced and poor quality."
        ]
        result = review_with_keyword_baseline(case)
        self.assertIn("CH-CONTEXT-01", {x["rule_id"] for x in result["findings"]})

    def test_ambiguous_competitor_criticism_routes_to_human(self):
        case = self.base_case()
        case["scenes"][0]["spoken_text"] = [
            "The competitor's product feels overpriced, but this is only my view."
        ]
        result = review_with_keyword_baseline(case)
        self.assertEqual(result["verdict"], "HUMAN_REVIEW")

    def test_neutral_competitor_mention_is_not_flagged(self):
        case = self.base_case()
        case["scenes"][0]["spoken_text"] = [
            "Paid partnership with Chanel. The competitor also launched a new fragrance this season."
        ]
        result = review_with_keyword_baseline(case)
        self.assertEqual(result["verdict"], "PASS")

    def test_unverified_first_hand_claim_routes_to_human(self):
        case = self.base_case()
        case["creator_used_product"] = None
        case["scenes"][0]["spoken_text"] = [
            "Paid partnership with Chanel. I love the moisturizer."
        ]
        result = review_with_keyword_baseline(case)
        self.assertEqual(result["verdict"], "HUMAN_REVIEW")


if __name__ == "__main__":
    unittest.main()




