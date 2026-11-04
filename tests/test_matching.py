import unittest
from app import similarity_score

class MatchingTests(unittest.TestCase):
    def test_similar_descriptions_have_positive_score(self):
        score = similarity_score(
            "black leather wallet lost near the library",
            "black leather wallet found by library entrance"
        )
        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_unrelated_descriptions_have_low_score(self):
        score = similarity_score("blue water bottle", "mathematics notebook")
        self.assertEqual(score, 0.0)

    def test_empty_text_is_safe(self):
        self.assertEqual(similarity_score("", ""), 0.0)

if __name__ == "__main__":
    unittest.main()
