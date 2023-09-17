import streamlit as st
import time

class WorkoutGuide:
    def __init__(self):
        self.workout_schedule = {
            'Monday': [[('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)], [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Tuesday': [[('Squats', 30), ('Lunges', 40)], [('Push-up', 30), ('Sit-up', 40)], [('Bicycle Crunches', 30), ('Leg Raise', 40)], [('Plank', 20), ('Side Plank', 20)]],
            'Wednesday': [[('Plank', 20), ('Side Plank', 20)], [('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Thursday': [[('Bicycle Crunches', 30), ('Leg Raise', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)], [('Push-up', 30), ('Sit-up', 40)]],
            'Friday': [[('Jumping Jacks', 30), ('Mountain Climbers', 30)], [('Push-up', 30), ('Sit-up', 40)], [('Squats', 30), ('Lunges', 40)], [('Plank', 20), ('Side Plank', 20)]],
            'Saturday': [[('Rest', 1)]],
            'Sunday': [[('Rest', 1)]]
        }


      
    def speak(self, text):
        st.markdown(f"<p id='speech_text' style='display:none;'>{text}</p>", unsafe_allow_html=True)
        st.markdown("""
            <script>
                var text = document.getElementById("speech_text").textContent;
                var msg = new SpeechSynthesisUtterance(text);
                window.speechSynthesis.speak(msg);
            </script>
        """, unsafe_allow_html=True)

    def workout_timer(self, duration, exercise):
        self.speak(f"Start {exercise}")
        placeholder = st.empty()
        for sec in range(duration, 0, -1):
            placeholder.text(f"{sec} seconds remaining.")
            time.sleep(1)
        self.speak("Time's up! Next one.")

    def rest_timer(self, duration):
        self.speak(f"Rest for {duration} seconds")
        placeholder = st.empty()
        for sec in range(duration, 0, -1):
            placeholder.text(f"{sec} seconds remaining.")
            time.sleep(1)
        self.speak("Rest time's over! Get ready.")


    def execute_workout(self):
        current_day = time.strftime("%A")
        st.write(f"Today is {current_day}, let's get started!")
        today_workout = self.workout_schedule.get(current_day, [[('Rest', 1)]])

        for group in today_workout:
            for exercise, duration in group:
                self.workout_timer(duration, exercise)
            self.rest_timer(40)

        st.write("Well done, you've crushed it today!")
        self.speak("Well done, you've crushed it today!")

def main():
    st.title('Workout Guide')
    if st.button('Start Workout'):
        guide = WorkoutGuide()
        guide.execute_workout()

if __name__ == "__main__":
    main()
