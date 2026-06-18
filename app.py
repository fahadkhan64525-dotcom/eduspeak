import streamlit as st
import cv2
import tempfile
import numpy as np
import whisper
import time
from utils.audio_analysis import analyze_speech
from utils.video_analysis import analyze_eye_contact
from utils.feedback import generate_feedback

st.set_page_config(page_title="EduSpeak — AI Communication Coach", layout="wide")

st.title("🎤 EduSpeak — AI Communication Coach")
st.write("Analyze your presentation or interview skills with AI feedback in real-time.")

uploaded_video = st.file_uploader("Upload your presentation video", type=["mp4", "mov", "avi"])
record_option = st.button("🎥 Record from Camera")

if uploaded_video or record_option:
    if record_option:
        st.info("OpenCV camera capture mode not supported in Streamlit Cloud; use local run instead.")
    else:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_path = tfile.name

        st.video(video_path)

        with st.spinner("Analyzing video..."):
            model = whisper.load_model("base")
            audio_analysis = analyze_speech(video_path, model)
            eye_contact_score = analyze_eye_contact(video_path)
            feedback = generate_feedback(audio_analysis, eye_contact_score)

        st.subheader("📊 Results Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Speaking Pace (WPM)", f"{audio_analysis['pace']:.1f}")
        col2.metric("Filler Words", str(audio_analysis["filler_count"]))
        col3.metric("Eye Contact (%)", f"{eye_contact_score:.1f}")

        st.progress(feedback["confidence_score"] / 100)
        st.write(f"**Confidence Score:** {feedback['confidence_score']:.1f}%")

        st.subheader("🧠 AI Feedback")
        st.write(feedback["advice"])
