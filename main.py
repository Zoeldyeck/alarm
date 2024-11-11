import streamlit as st
import time
from datetime import datetime, timedelta
import base64
# Set up the page title and tabs
st.title("Alarm, Stopwatch, and Timer")
def autoplay_audio(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
# Initialize tabs for each functionality
tabs = st.tabs(["Alarm", "Stopwatch", "Timer"])
alert_sound = "alert.mp3"
# ALARM FUNCTIONALITY
with tabs[0]:
    st.header("Alarm")
    alarm_time = st.time_input("Set Alarm Time")
    if st.button("Set Alarm"):
        st.success(f"Alarm set for {alarm_time}")
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == alarm_time.strftime("%H:%M:%S"):
                st.warning("⏰ Time's up! The alarm is ringing!")
                st.audio(alert_sound, format="audio/mp3")
                break
            time.sleep(1)
 # STOPWATCH FUNCTIONALITY
with tabs[1]:
    st.header("Stopwatch")
    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
    if "stopwatch_start_time" not in st.session_state:
        st.session_state.stopwatch_start_time = None
    if "stopwatch_elapsed_time" not in st.session_state:
        st.session_state.stopwatch_elapsed_time = timedelta(0)

    def start_stopwatch():
        st.session_state.stopwatch_start_time = datetime.now()
        st.session_state.stopwatch_running = True

    def stop_stopwatch():
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_elapsed_time += datetime.now() - st.session_state.stopwatch_start_time
        st.audio(alert_sound, format="audio/mp3")

    def reset_stopwatch():
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_elapsed_time = timedelta(0)

    if st.button("Start", on_click=start_stopwatch):
        st.write("Stopwatch started.")
    if st.button("Stop", on_click=stop_stopwatch):
        st.write("Stopwatch stopped.")
    if st.button("Reset", on_click=reset_stopwatch):
        st.write("Stopwatch reset.")

    if st.session_state.stopwatch_running:
        elapsed = datetime.now() - st.session_state.stopwatch_start_time + st.session_state.stopwatch_elapsed_time
    else:
        elapsed = st.session_state.stopwatch_elapsed_time

    st.subheader(f"Elapsed Time: {str(elapsed)}")

# TIMER FUNCTIONALITY
with tabs[2]:
    st.header("Timer")
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    timer_duration = st.number_input("Set Timer Duration (seconds)", min_value=1, max_value=3600, value=10)
    def start_timer():
        st.session_state.timer_running = True
    def stop_timer():
        st.session_state.timer_running = False

    if st.button("Start Timer", on_click=start_timer):
        st.write("Timer started.")
    if st.button("Stop Timer", on_click=stop_timer):
        st.write("Timer stopped.")    
        # Run the timer loop with repeat until stop button is pressed
    while st.session_state.timer_running:
        end_time = datetime.now() + timedelta(seconds=timer_duration)
        while datetime.now() < end_time and st.session_state.timer_running:
            remaining = end_time - datetime.now()
            st.write(f"Remaining Time: {str(remaining)}")
            time.sleep(1)
        if st.session_state.timer_running:
            st.warning("⏰ Timer is up!")
            autoplay_audio("alert.mp3")
