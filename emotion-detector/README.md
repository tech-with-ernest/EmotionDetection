# Emotion Detector — IBM Watson NLP and Flask

Final project for the IBM AI application development course. The app analyzes
English text using Watson NLP's EmotionPredict endpoint and reports anger,
disgust, fear, joy, sadness, and the dominant emotion.

## Run

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v test_emotion_detection.py
pylint server.py EmotionDetection test_emotion_detection.py
python server.py
```

Visit http://localhost:5000. The IBM Skills Network endpoint needs network
access and may only be reachable from the course environment. You can set
`WATSON_EMOTION_URL` to another compatible Watson NLP endpoint.

Tests mock the external service, so they check request and response behavior
without depending on network access. See `evidence/` for captured local output.
