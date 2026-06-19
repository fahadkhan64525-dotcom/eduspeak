import whisper
import numpy as np
import re
import os
import tempfile
import subprocess

def extract_audio(video_path):
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    subprocess.run([
        "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", temp_audio.name, "-y"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return temp_audio.name

def analyze_speech(video_path, model):
    audio_path = extract_audio(video_path)
    result = model.transcribe(audio_path)
    text = result["text"]

    words = text.split()
    duration = result["segments"][-1]["end"] if result["segments"] else 1
    wpm = len(words) / (duration / 60)

    filler_words = ["um", "uh", "like", "you know", "so"]
    filler_count = sum(text.lower().count(f) for f in filler_words)

    return {"pace": wpm, "filler_count": filler_count, "text": text}
