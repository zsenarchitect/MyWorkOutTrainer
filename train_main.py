import streamlit as st
import time
from datetime import datetime, timedelta
# from gtts import gTTS
from io import BytesIO
try:
    from gTTS import gTTS
except:
    pass
import os
try:
    os.mkdir("temp")
except:
    pass

class WorkoutGuide:
    def __init__(self, is_gym):
        self.is_gym = is_gym
        self.sound_counter = 0
        

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
                       [('平躺交叉脚', 3), ('宽臂俯卧撑', 4)], 
                       [('单脚站立右', 2), ('单脚站立左', 4)], 
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


      
    def speak(self, text, is_chinese = True):
        output_language = "zh-cn" if is_chinese else "en"
        try:
            tts = gTTS(text, lang=output_language, tld="co.uk", slow=False)
        except:
            print ("cannot speak")
            return
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        my_file_name += "_{}".format(self.sound_counter)
        tts.save(f"temp/{my_file_name}.mp3")
        audio_file = open(f"temp/{my_file_name}.mp3", "rb")
        # audio_bytes = audio_file.read()
        # st.audio(audio_bytes, format="audio/mp3", start_time=0)
        
        with open(f"temp/{my_file_name}.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            html_string = f"""
                <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
 

            attr_name = "tts_sound_{}".format(self.sound_counter)
            setattr(self, attr_name, st.empty())
            getattr(self, attr_name).markdown(html_string, unsafe_allow_html=True)

            self.sound_counter += 1






        return
        st.markdown(f"<p id='speech_text' style='display:none;'>{text}</p>", unsafe_allow_html=True)
        st.markdown("""
            <script>
                var text = document.getElementById("speech_text").textContent;
                var msg = new SpeechSynthesisUtterance(text);
                window.speechSynthesis.speak(msg);
            </script>
        """, unsafe_allow_html=True)
        




    def execute_workout(self):
        # Get current time in UTC
        utc_now = datetime.utcnow()

        # UTC offset for US Eastern Time (EST/EDT)
        # EST is UTC-5, EDT is UTC-4
        if time.localtime().tm_isdst:
            offset = timedelta(hours=-4)
        else:
            offset = timedelta(hours=-5)

        # Convert to US Eastern Time
        eastern_now = utc_now + offset

        # Get the weekday name
        current_day = eastern_now.strftime("%A")
        # current_day = time.strftime("%A")
        st.write(f"Today is {current_day}, let's get started!")
        
        # Display the full list of exercises for today
        workout_data = self.gym_workout_schedule if self.is_gym else self.home_workout_schedule
        today_workout = workout_data.get(current_day, [[('Rest', 1)]])
        st.write("Today's Exercises:")
        for group in today_workout:
            st.write(", ".join([exercise for exercise, _ in group]))
        
        # Workout loop
        # self.bt_skip = st.empty()
        placeholder = st.empty()
        # Spacer
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        for group in today_workout:
            for exercise, duration in group:
                self.rest_timer(8, placeholder, extra_text = f"下一个动作:<br>{exercise}")
                self.workout_timer(duration, exercise, placeholder)
            self.rest_timer(40, placeholder)

        st.write("Well done, you've crushed it today!")
        self.speak("Well done, you've crushed it today!")

    # Modified workout_timer and rest_timer with larger font size for countdown
    def workout_timer(self, duration, exercise, placeholder):
        self.speak(f"Start {exercise}")
        max = duration
        for sec in range(duration, 0, -1):
            placeholder.markdown(f"<h2>{exercise}<br>{sec}/{max}秒.</h2>", unsafe_allow_html=True)
            try:
                st.image(f"gifs/{exercise}.gif", width=400, caption=f"{exercise} in action")
            except:
                pass
            time.sleep(1)
        self.speak("Time's up! Next one.")
        self.play_sound()

    def rest_timer(self, duration, placeholder, extra_text = None):
        self.speak(f"Rest for {duration} seconds")
        max = duration
        if not extra_text:
            note = "休息一下!"
        else:
            note = extra_text
        for sec in range(duration, 0, -1):
            placeholder.markdown(f"<h2>{note}<br>{sec}/{max}秒.</h2>", unsafe_allow_html=True)
            time.sleep(1)
            # try:
            #     if st.button("跳过这个休息"):
            #         break
            # except:
            #     pass
        self.speak("Rest time's over! Get ready.")

    def play_sound(self, url = "https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3"):
        html_string = """
            <audio controls autoplay = "true">
                <source src={} type="audio/mp3">
            </audio>
            """.format(url)

        attr_name = "sound_{}".format(self.sound_counter)
        setattr(self, attr_name, st.empty())
        getattr(self, attr_name).markdown(html_string, unsafe_allow_html=True)

        self.sound_counter += 1

    
def main():
    st.markdown( """<style>
                body { text-align: center; }
                h1 { text-align: center; font-size: 100px; color: orange}
                h2 { text-align: center; font-size: 75px; }
                </style>""", unsafe_allow_html=True)
    # st.markdown("<style>h1 { text-align: center; font-size:100px;}</style>", unsafe_allow_html=True)
    # st.markdown("<style>h2 { text-align: center; font-size:75px;}</style>", unsafe_allow_html=True)


    title = st.empty()
    title.markdown(f"<h3 style = <text-align: center;>张森练健身</h3>", unsafe_allow_html=True)
    
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button('开始健身房训练'):
        guide = WorkoutGuide(is_gym = True)
        guide.execute_workout()
    if st.button('开始在家训练'):
        guide = WorkoutGuide(is_gym = False)
        guide.execute_workout()

if __name__ == "__main__":
    


    import base64

    # import streamlit as st


    def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )


    # st.write("# Auto-playing Audio!")

    # autoplay_audio("local_audio.mp3")

    main()