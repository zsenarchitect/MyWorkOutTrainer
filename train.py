import streamlit as st
import time
from gtts import gTTS
from io import BytesIO



class WorkoutGuide:
    def __init__(self):
        self.workout_schedule = {
            'Monday': [[('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)], [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Tuesday': [[('Squats', 30), ('Lunges', 40)], [('Push-up', 30), ('Sit-up', 40)], [('Bicycle Crunches', 30), ('Leg Raise', 40)], [('Plank', 20), ('Side Plank', 20)]],
            'Wednesday': [[('Plank', 20), ('Side Plank', 20)], [('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Thursday': [[('Bicycle Crunches', 30), ('Leg Raise', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)], [('Push-up', 30), ('Sit-up', 40)]],
            'Friday': [[('Jumping Jacks', 30), ('Mountain Climbers', 30)], [('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)]],
            'Saturday': [[('Rest', 1)]],
            'Sunday':  [[('Jumping Jacks', 3), ('Mountain Climbers', 5)]]
        }
        self.sound_file = BytesIO()
        tts = gTTS('Add text-to-speech to your app', lang='en')
        tts.write_to_fp(self.sound_file)
        st.audio(self.sound_file)


      
    def speak(self, text):
        st.markdown(f"<p id='speech_text' style='display:none;'>{text}</p>", unsafe_allow_html=True)
        st.markdown("""
            <script>
                var text = document.getElementById("speech_text").textContent;
                var msg = new SpeechSynthesisUtterance(text);
                window.speechSynthesis.speak(msg);
            </script>
        """, unsafe_allow_html=True)
        




    def execute_workout(self):
        st.markdown("<style>h1 { text-align: center; }</style>", unsafe_allow_html=True)
        current_day = time.strftime("%A")
        st.write(f"Today is {current_day}, let's get started!")
        
        # Display the full list of exercises for today
        today_workout = self.workout_schedule.get(current_day, [[('Rest', 1)]])
        st.write("Today's Exercises:")
        for group in today_workout:
            st.write(", ".join([exercise for exercise, _ in group]))
        
        # Workout loop
        placeholder = st.empty()
        for group in today_workout:
            for exercise, duration in group:
                self.workout_timer(duration, exercise, placeholder)
                self.rest_timer(40, placeholder)

        st.write("Well done, you've crushed it today!")
        self.speak("Well done, you've crushed it today!")

    # Modified workout_timer and rest_timer with larger font size for countdown
    def workout_timer(self, duration, exercise, placeholder):
        self.speak(f"Start {exercise}")
        max = duration
        for sec in range(duration, 0, -1):
            placeholder.markdown(f"<h1>{exercise}<br>{sec}/{max} seconds.</h1>", unsafe_allow_html=True)
            try:
                st.image(f"gifs/{exercise}.gif", width=400, caption=f"{exercise} in action")
            except:
                pass
            time.sleep(1)
        self.speak("Time's up! Next one.")

    def rest_timer(self, duration, placeholder):
        self.speak(f"Rest for {duration} seconds")
        max = duration
        for sec in range(duration, 0, -1):
            placeholder.markdown(f"<h1 style='font-size:60px;'>Take a rest!<br>{sec}/{max} seconds.</h1>", unsafe_allow_html=True)
            time.sleep(1)
        self.speak("Rest time's over! Get ready.")


def main():
    st.title('Workout Guide')
    if st.button('Start Workout'):
        guide = WorkoutGuide()
        guide.execute_workout()

if __name__ == "__main__":
    main()
