import streamlit as st
import pickle
import os
import random
import time
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from utils.text_emotion import predict_emotion, give_suggestion

st.set_page_config(page_title="Emotion Aware Study Companion", layout="wide")

# ================= UI STYLE ================= #
st.markdown("""
<style>
.stApp { background-color: #cfefff; }

.block-container {
    background: white;
    padding: 2rem;
    border-radius: 15px;
}

/* Headings */
h1, h2, h3 { color: #003366 !important; }

/* Normal text */
p, label, div, span {
    color: #111111 !important;
    font-size: 16px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #bde0fe;
}
section[data-testid="stSidebar"] * {
    color: #002244 !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #0077b6;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= STORAGE ================= #
def load_users():
    if os.path.exists("users.pkl"):
        with open("users.pkl", "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open("users.pkl", "wb") as f:
        pickle.dump(users, f)

def load_emotions():
    if os.path.exists("emotion_history.pkl"):
        with open("emotion_history.pkl", "rb") as f:
            return pickle.load(f)
    return {}

def save_emotions(data):
    with open("emotion_history.pkl", "wb") as f:
        pickle.dump(data, f)

# ================= SESSION ================= #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ================= LOGIN ================= #
if not st.session_state.logged_in:
    st.title("Emotion Aware Study Companion 💙")
    menu = st.radio("Select Option", ["Login", "Signup"], horizontal=True)
    users = load_users()

    if menu == "Signup":
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        if st.button("Signup"):
            if new_user in users:
                st.error("Username exists")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Account created!")

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()

# ================= SIDEBAR ================= #
st.sidebar.title("Dashboard")
st.sidebar.write(f"User: {st.session_state.username}")

page = st.sidebar.radio(
    "Navigation",
    ["Emotion Analyzer", "Mood History", "Break Games", "About"]
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ================= EMOTION ANALYZER ================= #
if page == "Emotion Analyzer":

    st.title("Emotion Analyzer 😊")

    st.write("AI-Powered Emotion Detection system..")
    st.info("This system analyzes your emotional state and provides personalized study suggestion.....!")

    text = st.text_area("How is your mood?")

    if st.button("Analyze Emotion"):
        if text.strip() == "":
            st.warning("Enter some text")
        else:
            emotion, emoji = predict_emotion(text)
            suggestion = give_suggestion(emotion)

            st.success(f"Detected Emotion: {emotion} {emoji}")
            st.info(f"Suggestion: {suggestion}")

            st.markdown("### 💡 Motivation For You")
            quotes = [
                "You are stronger than you think 💪",
                "Every day is a fresh start 🌅",
                "Keep going 🚀",
                "Believe in yourself 🌟"
            ]
            st.warning(random.choice(quotes))

            data = load_emotions()
            user = st.session_state.username
            if user not in data:
                data[user] = []
            data[user].append({
                "emotion": emotion,
                "time": datetime.now().strftime("%Y-%m-%d")
            })
            save_emotions(data)

# ================= MOOD HISTORY ================= #
elif page == "Mood History":

    st.title("Mood History 📊")
    data = load_emotions()
    user = st.session_state.username

    if user in data and data[user]:

        emotions = data[user]
        emotion_list = [x["emotion"] for x in emotions]
        overall = Counter(emotion_list)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Overall Mood Distribution")
            st.bar_chart(overall, height=300)

        with col2:
            st.subheader("Weekly Report")
            today = datetime.now()
            week_data = defaultdict(list)

            for item in emotions:
                date_obj = datetime.strptime(item["time"], "%Y-%m-%d")
                if today - timedelta(days=7) <= date_obj <= today:
                    day = date_obj.strftime("%A")
                    week_data[day].append(item["emotion"])

            ordered = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            weekly = {}
            for day in ordered:
                weekly[day] = len(week_data[day]) if week_data[day] else 0

            st.bar_chart(weekly, height=300)

    else:
        st.info("No mood history yet.")



# ================= BREAK GAMES ================= #

elif page == "Break Games":

    st.title("Smart Break Zone 🎮")

    import random
    import time

    # ---------------- SESSION STATE ----------------
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    if "current_game" not in st.session_state:
        st.session_state.current_game = None

    if "ng_level" not in st.session_state:
        st.session_state.ng_level = 1

    if "ng_number" not in st.session_state:
        st.session_state.ng_number = random.randint(1, 50)

    if "qm_data" not in st.session_state:
        st.session_state.qm_data = None

    # ---------------- START SCREEN ----------------
    if not st.session_state.game_started:

        if st.button("🚀 Start 5 Minute Break", key="start_btn"):
            st.session_state.game_started = True
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.ng_level = 1
            st.session_state.ng_number = random.randint(1, 50)
            st.session_state.qm_data = None
            st.session_state.current_game = None
            st.rerun()

    else:

        # ---------------- COUNTDOWN ----------------
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = 300 - elapsed

        if remaining <= 0:

            st.session_state.game_started = False

            st.markdown("""
                <div style='
                    position: fixed;
                    top: 40%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background-color: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0px 0px 25px rgba(0,0,0,0.3);
                    text-align: center;
                '>
                    <h2>⏰ 5 Minutes Completed!</h2>
                    <p>Break complete 😅<br><b>Now go study 📚🔥</b></p>
                </div>
            """, unsafe_allow_html=True)

            st.stop()

        mins = remaining // 60
        secs = remaining % 60

        st.warning(f"⏳ Time Left: {mins:02d}:{secs:02d}")
        st.success(f"🏆 Score: {st.session_state.score}")

        # ---------------- GAME SELECT ----------------
        game = st.radio(
            "Choose Game",
            [
                "🎯 Number Guessing Pro",
                "⚡ Quick Math Challenge",
                "✊ Rock Paper Scissors Battle"
            ],
            key="game_radio"
        )

        # If game changed → reset states cleanly
        if game != st.session_state.current_game:
            st.session_state.current_game = game
            st.session_state.qm_data = None
            st.rerun()

        # ===================================================
        # 🎯 NUMBER GUESSING
        # ===================================================
        if game == "🎯 Number Guessing Pro":

            max_range = 50 * st.session_state.ng_level

            st.subheader(f"Level: {st.session_state.ng_level}")
            st.write(f"Guess number between 1 and {max_range}")

            guess = st.number_input(
                "Enter Guess",
                min_value=1,
                max_value=max_range,
                step=1,
                key="ng_input"
            )

            if st.button("Submit Guess", key="ng_submit"):

                if guess > st.session_state.ng_number:
                    st.warning("Too High 📈 Try smaller number")
                elif guess < st.session_state.ng_number:
                    st.warning("Too Low 📉 Try bigger number")
                else:
                    st.success("Correct! Level Up 🚀 +10 points")
                    st.session_state.score += 10
                    st.session_state.ng_level += 1
                    new_range = 50 * st.session_state.ng_level
                    st.session_state.ng_number = random.randint(1, new_range)

        # ===================================================
        # ⚡ QUICK MATH
        # ===================================================
        elif game == "⚡ Quick Math Challenge":

            if st.session_state.qm_data is None:
                a = random.randint(5, 50)
                b = random.randint(5, 50)
                op = random.choice(["+", "-", "*"])

                if op == "+":
                    ans = a + b
                elif op == "-":
                    ans = a - b
                else:
                    ans = a * b

                st.session_state.qm_data = (a, b, op, ans)

            a, b, op, correct = st.session_state.qm_data

            st.write(f"{a} {op} {b} = ?")

            user_ans = st.number_input("Your Answer", step=1, key="qm_input")

            if st.button("Check Answer", key="qm_submit"):

                if user_ans == correct:
                    st.success("Correct! +5 points 🔥")
                    st.session_state.score += 5
                else:
                    st.error(f"Wrong! Correct answer: {correct}")

                st.session_state.qm_data = None
                st.rerun()

        # ===================================================
        # ✊ ROCK PAPER SCISSORS
        # ===================================================
        elif game == "✊ Rock Paper Scissors Battle":

            choice = st.radio(
                "Choose",
                ["Rock", "Paper", "Scissors"],
                key="rps_choice"
            )

            if st.button("Play Round", key="rps_play"):

                computer = random.choice(["Rock", "Paper", "Scissors"])
                st.write("Computer:", computer)

                if choice == computer:
                    st.info("Tie 🤝")
                elif (choice=="Rock" and computer=="Scissors") or \
                     (choice=="Paper" and computer=="Rock") or \
                     (choice=="Scissors" and computer=="Paper"):
                    st.success("You Win! +5 points 🎉")
                    st.session_state.score += 5
                else:
                    st.error("You Lose!")

        # ---------------- AUTO REFRESH ----------------
        time.sleep(1)
        st.rerun()
# ================= ABOUT ================= #
elif page == "About":
    st.title("About Project")
    st.write("""
    Emotion Aware Study Companion includes:

    • AI Emotion Detection  
    • Personalized Suggestions  
    • Motivation Generator  
    • Mood Analytics + Weekly Report  
    • Smart Break Timer with Games  

    Built using Streamlit & Machine Learning.
    """)