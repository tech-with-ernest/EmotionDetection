"""Unit tests for Watson response formatting and the Flask route."""

import unittest
from unittest.mock import patch

from EmotionDetection import emotion_detector
from server import app


class TestEmotionDetector(unittest.TestCase):
    """Check the Watson wrapper with representative mocked HTTP responses."""

    def test_emotion_scores_and_dominant_emotion(self):
        """The returned result has the required keys and highest score."""
        cases = [
            ("I am glad this happened", "joy"),
            ("I am furious", "anger"),
            ("This is disgusting", "disgust"),
            ("I am afraid", "fear"),
            ("I feel so sad", "sadness"),
        ]
        for statement, expected in cases:
            with self.subTest(expected=expected):
                values = {key: 0.1 for key in
                          ("anger", "disgust", "fear", "joy", "sadness")}
                values[expected] = 0.9
                with patch("EmotionDetection.emotion_detection.requests.post") as post:
                    post.return_value.status_code = 200
                    post.return_value.json.return_value = {
                        "emotionPredictions": [{"emotion": values}]
                    }
                    result = emotion_detector(statement)
                    self.assertEqual(result, {**values, "dominant_emotion": expected})
                    self.assertEqual(post.call_args.kwargs["json"],
                                     {"raw_document": {"text": statement}})

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_bad_request(self, post):
        """A 400 response returns six None fields."""
        post.return_value.status_code = 400
        self.assertEqual(emotion_detector(""), {
            "anger": None, "disgust": None, "fear": None,
            "joy": None, "sadness": None, "dominant_emotion": None,
        })

    def test_blank_input_in_browser(self):
        """Whitespace is rejected before calling Watson."""
        with app.test_client() as client:
            self.assertEqual(client.get("/emotionDetector?textToAnalyze=%20").data,
                             b"Invalid text! Please try again!")


if __name__ == "__main__":
    unittest.main()
