def generate_feedback(audio_data, eye_score):
    pace = audio_data["pace"]
    fillers = audio_data["filler_count"]

    confidence = 100 - (abs(pace - 130) * 0.2) - (fillers * 2) + (eye_score * 0.3)
    confidence = max(0, min(100, confidence))

    advice = []
    if pace > 150:
        advice.append("You’re speaking a bit fast — try slowing down.")
    elif pace < 100:
        advice.append("Try to increase your pace slightly for better engagement.")
    if fillers > 5:
        advice.append("Reduce filler words like 'um' or 'like'.")
    if eye_score < 50:
        advice.append("Maintain more eye contact with the camera for confidence.")

    return {
        "confidence_score": confidence,
        "advice": "\n".join(advice) or "Excellent delivery! Keep it up!"
    }
