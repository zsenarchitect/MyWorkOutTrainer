import streamlit as st
import time
from datetime import datetime, timedelta
import pprint
# from gtts import gTTS
from io import BytesIO
try:
    from gTTS import gTTS
except:
    pass
import os
import json
try:
    os.mkdir("temp")
except:
    pass

class WorkoutGuide:
    def __init__(self, is_gym):
        data = self.read_log()
        print (data)
        if data is None:
            
            st.write("there is no data")
        else:
            st.write("showing data:")


        for key,value in data.items():
            st.write("{}:{}".format(key,value))


        self.is_gym = is_gym
        self.sound_counter = 0

        with open("set_data.json", "r") as f:
            self.training_set = json.load(f)
        

        self.home_workout_schedule = {
            'Monday': [[('俄罗斯转体', 30), ('深蹲', 40)], 
                       [('平躺交叉脚', 30), ('宽臂俯卧撑', 30)], 
                       [('单脚站立右', 30), ('单脚站立左', 20)], 
                       [('宽臂俯卧撑', 30), ('up dog down dog 拉伸', 30)], 
                       [('侧身平板支撑左', 30), ('侧身平板支撑右', 30)], 
                       [('宽臂俯卧撑', 30), ('俄罗斯转体', 30)]],
            'Tuesday': [[('膝盖俯卧撑', 30), ('Lunges', 40)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)], 
                        [('Plank', 20), ('Side Plank', 20)]],
            'Wednesday':[[('Plank', 20), ('Side Plank', 20)], 
                        [('Push-up', 30), ('Sit-up', 40)], 
                        [('Squats', 30), ('Lunges', 40)], 
                        [('Bicycle Crunches', 30), ('Leg Raise', 40)]],
            'Thursday': [('Bicycle Crunches', 'Leg Raise'),
                        ('Squats', 'Lunges'), 
                        ('Plank', 'Side Plank'), 
                        ('Push-up', 'Sit-up')],
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
        self.today_workout = workout_data.get(current_day, [[('Rest', 1)]])
        st.write("Today's Exercises:")
        for group in self.today_workout:
            print (group)
            st.write(", ".join( list(group)))
        
        # Workout loop
        # self.bt_skip = st.empty()
        self.main_placeholder_display = st.empty()
        # Spacer
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

        for group in self.today_workout:
            for exercise in group:
                duration  = self.training_set.get(exercise, 30)
                self.rest_timer(10, extra_text = f"下一个动作:<br>{exercise}")
                self.workout_timer(duration, exercise)
            self.rest_timer(40)

        note ="Well done!<br>You've crushed it today!"
        self.main_placeholder_display.markdown(f"""<body style="text-align:center; font-size:80px; color: white;font-weight:bold;">{note}</body>""", unsafe_allow_html=True)

        self.speak("Well done, you've crushed it today!")


    def read_log(self):
        with open("training_log.json", "r") as f:
            return json.load(f)
        
    def log_training(self):
        pass
        # open "training_log.json" and append the current day's exercises to it, depending on the current session is in gym or in home
        # log the date, if this is gym or home, and the count of all actions today
        with open("training_log.json", "r") as f:
            data = json.load(f)
            # get today's date
            data.get("dates", []).append(datetime.now().strftime("%Y-%m-%d"))

            action_data = data.get("action_data", {})
            for group in self.today_workout:
                for exercise, duration in group:
                    if exercise in action_data:
                        action_data[exercise] += 1
                    else:
                        action_data[exercise] = 1
        
        with open("training_log.json", "w") as f:
            json.dump(data, f, indent=4)


    # Modified workout_timer and rest_timer with larger font size for countdown
    def workout_timer(self, duration, exercise):
        self.speak(f"Start {exercise}")
        max = duration
        for sec in range(duration, 0, -1):
            self.main_placeholder_display.markdown(f"""<body style="text-align:center; font-size:70px;font-weight:bold;">{exercise}<br>{sec}/{max}秒.</body>""", unsafe_allow_html=True)
            try:
                st.image(f"gifs/{exercise}.gif", width=400, caption=f"{exercise} in action")
            except:
                pass
            time.sleep(1)
        self.speak("Time's up! Next one.")
        self.play_sound()

    def rest_timer(self, duration, extra_text = None):
        self.speak(f"Rest for {duration} seconds")
        max = duration
        if not extra_text:
            note = "休息一下!"
        else:
            note = extra_text
        for sec in range(duration, 0, -1):
            self.main_placeholder_display.markdown(f"""<body style="text-align:center; font-size:70px; color: orange;font-weight:bold;">{note}<br>{sec}/{max}秒.</body>""", unsafe_allow_html=True)
            time.sleep(1)
            # try:
            #     if st.button("跳过这个休息"):
            #         break
            # except:
            #     pass
        self.speak("Rest time's over! Get ready.")
        self.play_sound()

    def play_sound(self, url = None):
        if not url:
            # default ring sounds
            url = "https://www.orangefreesounds.com/wp-content/uploads/2022/04/Small-bell-ringing-short-sound-effect.mp3"


        html_string = """
            <audio controls autoplay = "true">
                <source src={} type="audio/mp3">
            </audio>
            """.format(url)


        st.markdown("-----<br>", unsafe_allow_html=True)
        attr_name = "sound_{}".format(self.sound_counter)
        setattr(self, attr_name, st.empty())
        getattr(self, attr_name).markdown(html_string, unsafe_allow_html=True)

        self.sound_counter += 1

    
def main():
    
    st.markdown( """<style>
                body { text-align: center; }
                h1 {font-size: 100px; color: orange; text-align: center; }
                h2 {  font-size: 70px;  text-align: center; }
                </style>""", unsafe_allow_html=True)
    # st.markdown("<style>h1 { text-align: center; font-size:100px;}</style>", unsafe_allow_html=True)
    # st.markdown("<style>h2 { text-align: center; font-size:75px;}</style>", unsafe_allow_html=True)


    title = st.empty()
    title.markdown(f"""<body style = "<text-align: center; font-size:90px; font-weight:bold;">张森<br>练健身</body>""", unsafe_allow_html=True)
    
    # Spacer
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    is_started = False
    if st.button('开始健身房训练'):
        is_gym = True
        is_started = True
    if st.button('开始在家训练'):
        is_gym = False
        is_started = True
    
    if is_started:
        guide = WorkoutGuide(is_gym)
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