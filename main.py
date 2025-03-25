import streamlit as st
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
import os
import time
from datetime import datetime, timedelta
import base64
from streamlit.components.v1 import html
import plotly.graph_objects as go
import random
import requests



# Set up the Google API key
os.environ["GOOGLE_API_KEY"] = st.secrets['google_api_key']

# Configure the Gemini model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', generation_config=genai.GenerationConfig(
    temperature=0.7,
))

st.set_page_config(
    page_title="Inner Compass AI",

    layout="centered"
)

st.markdown("""
    <style>
    .stButton > button {
        background-color: #007BFF;
        color: white;
        width: 130px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize conversation memory
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Set session state for page and messages

if 'page' not in st.session_state:
    st.session_state.page = 'front'

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'start_time' not in st.session_state:
    st.session_state.start_time = None  # time.time() changes

if 'timer_complete' not in st.session_state:
    st.session_state.timer_complete = False

if 'interaction_count' not in st.session_state:
    st.session_state.interaction_count = 0

if 'page_history' not in st.session_state:
    st.session_state.page_history = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"  # Default starting page

if 'previous_page' not in st.session_state:
    st.session_state.previous_page = None  # To track last visited page




#Back button
def back_button():
    col1, col2 = st.columns([0.1, 0.9])  # Adjust the width of the columns
    with col1:
        if st.session_state.page_history:
            if st.button("Back"):
                st.session_state.page = st.session_state.page_history.pop()

def back_slash():
    col1, col2 = st.columns([0.1, 0.9])  # Adjust the width of the columns
    with col1:
        if st.session_state.page_history:
            if st.button("<"):
                st.session_state.page = st.session_state.page_history.pop()
# Used Gemini for response
def generate_ai_response(user_input):
    try:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()

        elapsed_time = time.time() - st.session_state.start_time
        conversation_history = st.session_state.memory.load_memory_variables({})["history"]

        if elapsed_time < 570:  # Less than 9.5 minutes
            prompt = f"{conversation_history}\nUser: {user_input}\nAI: Respond empathetically and supportively. Provide teaching and inspiring words. Focus on understanding the user's situation. Ask relevant questions if necessary."
        elif 570 <= elapsed_time < 600 and not st.session_state.timer_complete:  # Between 9.5 and 10 minutes
            prompt = f"{conversation_history}\nUser: {user_input}\nAI: Mention that the session is nearing its end and ask if the user would like a personalized daily planner."
        else:  # After 10 minutes
            prompt = f"{conversation_history}\nUser: {user_input}\nAI: Provide personalized suggestions for stress relief based on our conversation, including breathing exercises, meditation techniques, and home-based detoxification methods."

        response = model.generate_content(prompt)
        return response.text
    except ValueError as e:
        if "Invalid operation" in str(e):
            return "I'm sorry, but I'm not able to respond to that specific input. Could you please rephrase your question or concern?"
        else:
            raise


# Front Page
def front_page():

    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        .big-font {
            font-size: 48px !important;
            font-weight: bold;
        }
        .yellow-box {
            background-color: #FFD700;
            color: #000000;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        .yellow-box:hover {
            background-color: #FFA500;
        }
        .subtitle {
            font-size: 18px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">Inner Compass AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">The #1 Site for Mental Health Support</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Double Click to get personalized support from our compassionate AI assistant!</p>',
        unsafe_allow_html=True)

    if st.button("Start Sharing"):
        st.session_state.page_history.append('front')
        st.session_state.page = 'choice'

    st.markdown(
        '<p class="subtitle">NOTE: 1. Each session is 10 minutes long.</p>',
        unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">2. By the end of the session, you will receive a personalized planner.</p>',
        unsafe_allow_html=True)


# Second Page with three options: Chat, Meditation, Games
def second_page():
    back_button()
    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        .big-font {
            font-size: 48px !important;
            font-weight: bold;
        }
        .option-box {
            background-color: #FFD700;
            color: #000000;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .option-box:hover {
            background-color: #FFA500;
        }
        .subtitle {
            font-size: 18px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Welcome to Mental Health Support</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose an option:</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Chat"):
            st.session_state.page_history.append('choice')
            st.session_state.page = 'chat'
            if st.session_state.start_time is None:
                st.session_state.start_time = time.time()

    with col2:
        if st.button("Meditation"):
            st.session_state.page_history.append('choice')
            st.session_state.page = 'meditation'

    with col3:
        if st.button("Games"):
            st.session_state.page_history.append('choice')
            st.session_state.page = 'games'


def create_daily_planner(ai_response):

    st.subheader("Your Personalized Daily Planner", divider="rainbow")
    st.markdown("""
            <style>
            .stApp {
                background-color: #000000;
                color: #4A4A4A;
            }
            stTextInput > div > div > input {
                background-color: #FFE4B5;
            }
            </style>
            """, unsafe_allow_html=True)

    # List of inspirational quotes
    quotes = [
        "'The only way to do great work is to love what you do.' - Steve Jobs",
        "'Believe you can and you're halfway there.' - Theodore Roosevelt",
        "'The future belongs to those who believe in the beauty of their dreams.' - Eleanor Roosevelt",
        "'It always seems impossible until it's done.' - Nelson Mandela",
        "'Success is not final, failure is not fatal: it is the courage to continue that counts.' - Winston Churchill",
        "'The only limit to our realization of tomorrow will be our doubts of today.' - Franklin D. Roosevelt",
        "'Do what you can, with what you have, where you are.' - Theodore Roosevelt",
        "'Everything you've ever wanted is on the other side of fear.' - George Addair",
        "'The way to get started is to quit talking and begin doing.' - Walt Disney",
        "'Don't watch the clock; do what it does. Keep going.' - Sam Levenson"
    ]

    # Parse the AI response into sections
    sections = ai_response.split('\n\n')

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown("### Today's Focus")
    #     st.info(sections[0] if len(sections) > 0 else "Focus on self-care and personal growth.")

    #     st.markdown("### Breathing Exercise")
    #     st.success(sections[1] if len(sections) > 1 else "Practice deep breathing for 5 minutes.")

    # with col2:
    #     st.markdown("### Meditation Technique")
    #     st.warning(sections[2] if len(sections) > 2 else "Try a 10-minute guided meditation.")

    #     st.markdown("### Detoxification Method")
    #     st.error(sections[3] if len(sections) > 3 else "Drink plenty of water throughout the day.")

    st.markdown("### Daily Timeline")
    now = datetime.now()
    timeline = []
    for i in range(8, 22, 2):  # From 8 AM to 8 PM
        time = now.replace(hour=i, minute=0, second=0, microsecond=0)
        activity = sections[i // 2 - 3] if len(sections) > i // 2 - 3 else 'Take a moment for self-reflection.'
        timeline_entry = f"{time.strftime('%I:%M %p')} - {activity}"
        st.markdown(f"{timeline_entry}")
        timeline.append(timeline_entry)

    st.markdown("---")
    st.markdown("### Daily Inspiration")
    quote = random.choice(quotes)
    st.markdown(f"{quote}")

    # st.markdown("### Daily Progress")

    # Initialize the progress value in session state if it doesn't exist
    # if 'progress_value' not in st.session_state:
    #     st.session_state.progress_value = 50

    # Use a callback to update the session state

    planner_content = f"""Your Personalized Daily Planner


Daily Timeline:
{chr(10).join(timeline)}

Daily Inspiration: {quote}

"""

    st.download_button("Download Daily Planner", planner_content, file_name="daily_planner.txt", mime="text/plain")


# Chat Page
def chat_page():

    st.title("Let's Talk")
    # Custom component for continuous time update
    st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #4A4A4A;
    }
    .stTextInput > div > div > input {
        background-color: #FFE4B5;
    }
    </style>
    """, unsafe_allow_html=True)

    def sidebar_time_updater():
        return html(
            """
            <div id="time-remaining"  style="background-color: white; padding: 10px; border-radius: 5px; width: 30px;"></div>
            <script>
                function updateTime() {
                    const startTime = """ + str(st.session_state.start_time) + """;
                    const elapsedTime = (Date.now() / 1000) - startTime;
                    const remainingTime = Math.max(0, 600 - elapsedTime);
                    const minutes = Math.floor(remainingTime / 60);
                    const seconds = Math.floor(remainingTime % 60);
                    const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                    document.getElementById('time-remaining').innerText = timeString;
                    if (remainingTime > 0) {
                        setTimeout(updateTime, 1000);
                    } else {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'TIMER_COMPLETE'}, '*');
                    }
                }
                updateTime();
            </script>
            """,
            height=50,
        )

    with st.sidebar:
        back_slash()
        st.markdown("### Session Timer")
        sidebar_time_updater()



    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, 600 - elapsed_time)
    minutes, seconds = divmod(int(remaining_time), 60)
    # st.sidebar.metric("Time Remaining", f"{minutes}:{seconds:02d}")

    if remaining_time <= 40 and not st.session_state.get('warning_shown', False):
        st.toast("Your session is going to end soon!", icon="⚠")
        st.session_state.warning_shown = True

    if remaining_time == 0 and not st.session_state.timer_complete:
        st.session_state.timer_complete = True
        st.info("Session has ended. Generating your daily planner...")
        ai_response = generate_ai_response("Please create a daily planner for me.")
        create_daily_planner(ai_response)
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("How are you feeling today?")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        ai_response = generate_ai_response(user_input)
        st.session_state.memory.save_context({"input": user_input}, {"output": ai_response})
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        with st.chat_message("assistant"):
            st.markdown(ai_response)


def debug_audio_url(url):
    try:
        # Allow redirects to follow the 303 response
        response = requests.get(url, allow_redirects=True)

        st.write(f"You can download relaxing audio curated only for you: {response.url}")


        if response.status_code == 200:
            st.success("URL seems to be accessible")
            return response.url  # Return the final URL after redirection
        else:
            st.error(f"URL returned status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred while checking URL: {str(e)}")
        return None


# Meditation Page with Radar Chart
# Meditation Page with Radar Chart
# Meditation Page with Radar Chart
def meditation_page():
    back_button()
    st.title("Guided Meditation")
    st.markdown("""
        <p>Close your eyes, take a deep breath, and follow this guided meditation:</p>
        <ul>
            <li><strong>Breathing Exercise:</strong> Inhale deeply, hold for 5 seconds, then exhale slowly.</li>
            <li><strong>Focus:</strong> Let go of any stressful thoughts and focus on the present moment.</li>
        </ul>
    """, unsafe_allow_html=True)

    factors = ['Stress', 'Anxiety', 'Sleeplessness', 'Fatigue', 'Emotional Imbalance']
    levels = ['Very Little', 'Little', 'Moderate', 'Extreme', 'Very Extreme']

    stress_level = st.select_slider('Stress Level', options=levels)
    anxiety_level = st.select_slider('Anxiety Level', options=levels)
    sleepless_level = st.select_slider('Sleeplessness Level', options=levels)
    fatigue_level = st.select_slider('Fatigue Level', options=levels)
    emotion_level = st.select_slider('Emotional Imbalance Level', options=levels)

    level_map = {'Very Little': 1, 'Little': 2, 'Moderate': 3, 'Extreme': 4, 'Very Extreme': 5}
    values = [
        level_map[stress_level],
        level_map[anxiety_level],
        level_map[sleepless_level],
        level_map[fatigue_level],
        level_map[emotion_level]
    ]

    # Calculate average stress level
    average_stress = sum(values) / len(values)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=factors,
        fill='toself',
        name='Current Levels'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5]
            )),
        showlegend=False,
        title="Your Emotional & Physical Levels"
    )

    st.plotly_chart(fig)

    # Display average stress level
    st.subheader(f"Your Average Stress Level: {average_stress:.2f}")

    # Play song based on average stress level
    audio_url = None
    if average_stress < 2:
        audio_url = "https://drive.google.com/uc?export=download&id=1vSOgKuuvRTcm9zw3p1GEu6af5SC6UUXA"
    elif average_stress < 3.5:
        audio_url = "https://drive.google.com/uc?export=download&id=1kGyl7HQbOU8fZkuF6h4ZLdLjp-XyvmcM"
    else:
        audio_url = "https://drive.google.com/uc?export=download&id=1Mc1ixbPQJfKEYzLsX6NEfBptiXocLG_c"

    final_url = debug_audio_url(audio_url)

    # Additional meditation guidance
    st.markdown("""
        ### Meditation Tips
        - Find a comfortable position
        - Focus on your breath
        - Let thoughts come and go without judgment
        - Start with 5 minutes and gradually increase duration
    """)





# Games Page
def games_page():
    back_button()
    st.title("Stress-Relief Games")
    st.markdown("""
        <p>Here are some games to help you relax and relieve stress:</p>
        <ul>
            <li><strong>Super Mario:</strong> A relaxing adventure game. <a href="https://supermarioplay.com">Play now</a></li>
            <li><strong>Bubble Shooter:</strong> A relaxing pop game. <a href="https://poki.com/en/g/bubble-shooter-lak">Play now</a></li>
            <li><strong>Maze:</strong> A relaxing puzzle game. <a href="https://poki.com/en/g/maze-path-of-light">Play now</a></li>
            <li><strong>Infinity Loop Hex: </strong> A relaxing puzzle game. <a href="https://poki.com/en/g/infinity-loop-hex">Play now</a></li>
            <li><strong>Subway Surfers: </strong>An adventurous obstacle game<a href="https://poki.com/en/g/subway-surfers">Play now</a></li>
            <li><strong>Tetris: </strong>Your nostalgic block game<a href="https://www.goodoldtetris.com/">Play now</a></li>
            <li><strong>Sllides: </strong>The 1900s block game<a href="https://sllides.com/">Play now</a></li>
        </ul>
    """, unsafe_allow_html=True)

    st.markdown("### Relaxation Exercise")
    st.write("Try this quick relaxation technique:")
    st.write("1. Close your eyes and take a deep breath.")
    st.write("2. Tense all your muscles for 5 seconds.")
    st.write("3. Release the tension and relax for 10 seconds.")
    st.write("4. Repeat this process 3 times.")

    st.markdown("### Mood Tracker")
    mood = st.slider("How do you feel after playing?", 1, 10, 5)
    st.write(f"Your mood: {mood}/10")
    if mood < 5:
        st.write("Remember, it's okay to have off days. Try another game or activity!")
    else:
        st.write("Great! Keep up the positive activities!")


# Main app logic to handle page navigation
def main():
    if st.session_state.page == 'front':
        front_page()
    elif st.session_state.page == 'choice':
        second_page()
    elif st.session_state.page == 'chat':
        chat_page()
    elif st.session_state.page == 'meditation':
        meditation_page()
    elif st.session_state.page == 'games':
        games_page()

st.markdown(
    "<div style='position: fixed; bottom: 10px; left: 10px; font-size: 12px;'>Disclaimer: This AI assistant is not a substitute for professional mental health care.</div>",
    unsafe_allow_html=True
)


if __name__ == '__main__':
    main()
