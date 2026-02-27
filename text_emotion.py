def predict_emotion(text):

    text = text.lower()

    happy_words = ["happy", "joy", "great", "good", "excited", "awesome",
                   "santhosham", "baagundi", "chala happy", "super"]

    sad_words = ["sad", "depressed", "cry", "bad", "upset",
                 "baadha", "edustunna", "lopala baadha"]

    angry_words = ["angry", "mad", "furious",
                   "kopam", "chala kopam"]

    stress_words = ["stress", "tension", "worried",
                    "tension ga undi", "bhayam", "anxiety"]

    for word in happy_words:
        if word in text:
            return "Happy", "😊"

    for word in sad_words:
        if word in text:
            return "Sad", "😢"

    for word in angry_words:
        if word in text:
            return "Angry", "😡"

    for word in stress_words:
        if word in text:
            return "Stressed", "😰"

    return "Neutral", "😐"


def give_suggestion(emotion):

    suggestions = {
        "Happy": "Keep up the positive energy! Continue studying with focus.",
        "Sad": "Take a short break, listen to calm music and restart.",
        "Angry": "Practice deep breathing for 2 minutes before studying.",
        "Stressed": "Break your tasks into small goals. You can do it!",
        "Neutral": "Maintain steady focus and consistency."
    }

    return suggestions.get(emotion, "Stay motivated!")