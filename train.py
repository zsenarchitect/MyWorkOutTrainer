import streamlit as st
import time
# from gtts import gTTS
from io import BytesIO



class WorkoutGuide:
    def __init__(self, is_gym):
        self.is_gym = is_gym

        self.home_workout_schedule = {
            'Monday': [[('俄罗斯转体', 30), ('深蹲', 40)], 
                       [('平躺交叉脚', 30), ('宽臂俯卧撑', 30)], 
                       [('单脚站立右', 30), ('单脚站立左', 20)], 
                       [('宽臂俯卧撑', 30), ('up dog down dog 拉伸', 30)], 
                       [('侧身平板支撑左', 30), ('侧身平板支撑右', 30)], 
                       [('宽臂俯卧撑', 30), ('俄罗斯转体', 30)]],
            'Tuesday': [[('膝盖平板支撑', 30), ('Lunges', 40)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)], 
                        [('Plank', 20), ('Side Plank', 20)]],
            'Wednesday':[[('Plank', 20), ('Side Plank', 20)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Thursday': [[('Bicycle Crunches', 30), ('Leg Raise', 40)],
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Plank', 20), ('Side Plank', 20)], 
                        [('Push-up', 30), ('Sit-up', 40)]],
            'Friday': [[('Jumping Jacks', 30), ('Mountain Climbers', 30)],
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Plank', 20), ('Side Plank', 20)]],
            'Saturday': [[('Rest', 1)]],
            'Sunday':  [[('俄罗斯转体', 5), ('深蹲', 5)], 
                       [('平躺交叉脚', 30), ('宽臂俯卧撑', 30)], 
                       [('单脚站立右', 30), ('单脚站立左', 20)], 
                       [('宽臂俯卧撑', 30), ('up dog down dog 拉伸', 30)], 
                       [('侧身平板支撑左', 30), ('侧身平板支撑右', 30)], 
                       [('宽臂俯卧撑', 30), ('俄罗斯转体', 30)]]
        }      


        self.gym_workout_schedule = {
            'Monday': [[('坐举哑铃上举', 30), ('深蹲', 40)], 
                       [('两臂平举', 30), ('半仰哑铃上举', 30)], 
                       [('单脚站立右', 30), ('单脚站立左', 20)], 
                       [('宽臂俯卧撑', 30), ('小臂正手腕部', 30)], 
                       [('窄臂俯卧撑', 30), ('小臂反手腕部', 30)], 
                       [('俯身拉举左', 30), ('俯身拉举右', 30)]],
            'Tuesday': [[('Squats', 30), ('Lunges', 40)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)], 
                        [('Plank', 20), ('Side Plank', 20)]],
            'Wednesday':[[('Plank', 20), ('Side Plank', 20)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Thursday': [[('Bicycle Crunches', 30), ('Leg Raise', 40)],
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Plank', 20), ('Side Plank', 20)], 
                        [('Push-up', 30), ('Sit-up', 40)]],
            'Friday': [[('Jumping Jacks', 30), ('Mountain Climbers', 30)],
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Plank', 20), ('Side Plank', 20)]],
            'Saturday': [[('Rest', 1)]],
            'Sunday':  [[('吃饭Jumping Jacks', 3), ('Mountain Climbers', 5)]]
        }
        # self.sound_file = BytesIO()
        # tts = gTTS('Add text-to-speech to your app', lang='en')
        # tts.write_to_fp(self.sound_file)
        # st.audio(self.sound_file)


      
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
        workout_data = self.gym_workout_schedule if self.is_gym else self.home_workout_schedule
        today_workout = workout_data.get(current_day, [[('Rest', 1)]])
        st.write("Today's Exercises:")
        for group in today_workout:
            st.write(", ".join([exercise for exercise, _ in group]))
        
        # Workout loop
        self.bt_skip = st.empty()
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
            placeholder.markdown(f"<h1  style='font-size:75px;'>{exercise}<br>{sec}/{max}秒.</h1>", unsafe_allow_html=True)
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
            placeholder.markdown(f"<h1 style='font-size:75px;'>休息一下!<br>{sec}/{max}秒.</h1>", unsafe_allow_html=True)
            time.sleep(1)
            if self.bt_skip.button("跳过这个休息"):
                break
        self.speak("Rest time's over! Get ready.")


def main():
    st.title('Workout Guide')
    if st.button('Start Gym Workout'):
        guide = WorkoutGuide(is_gym = True)
        guide.execute_workout()
    if st.button('Start Home Workout'):
        guide = WorkoutGuide(is_gym = False)
        guide.execute_workout()

if __name__ == "__main__":
    main()