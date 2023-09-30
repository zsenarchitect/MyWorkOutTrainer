import streamlit as st
import time
import io
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

        with io.open("set_data.json", "r", encoding="utf-8") as f:
            self.training_set = json.load(f)
        

        self.home_workout_schedule = {
            "Monday": [["俄罗斯转体", "深蹲"], 
                       ["平躺交叉脚", "宽臂俯卧撑"], 
                       ["单脚站立,右", "单脚站立,左","倒立"], 
                       ["宽臂俯卧撑", "up dog down dog 拉伸"], 
                       ["侧身平板支撑,左", "侧身平板支撑,右","腹部着地腰挺"], 
                       ["宽臂俯卧撑", "俄罗斯转体"]],
            "Tuesday": [["膝盖俯卧撑", "深蹲"], 
                        ["宽臂俯卧撑",  "侧卧弹力带开腿,左", "侧卧弹力带开腿,右"], 
                        ["平躺蹬自行车", "窄臂俯卧撑"], 
                        ["侧身平板支撑,左", "侧身平板支撑,右"]],
            "Wednesday":[["俄罗斯转体", "深蹲"], 
                       ["平躺交叉脚", "宽臂俯卧撑"], 
                       ["单脚站立,右", "单脚站立,左"], 
                       ["窄臂俯卧撑", "up dog down dog 拉伸"], 
                       ["侧身平板支撑,左", "侧身平板支撑,右"], 
                       ["宽臂俯卧撑", "俄罗斯转体"]],
            "Thursday": "Monday",
            "Friday": "Tuesday",
            "Saturday": "Monday",
            "Sunday":  "Wednesday"
        }      


        self.gym_workout_schedule = {
            "Monday": [["坐举哑铃上举", "深蹲"], 
                       ["两臂平举", "半仰哑铃上举"], 
                       ["单脚站立,右", "单脚站立,左"], 
                       ["宽臂俯卧撑", "小臂正手腕部"], 
                       ["窄臂俯卧撑", "小臂反手腕部"], 
                       ["俯身拉举,左", "俯身拉举,右"]],
            "Tuesday": [["负重举肩","膝盖俯卧撑"], 
                        ["宽臂俯卧撑", "两臂平举"], 
                        ["小臂反手腕部","小臂正手腕部", "负重举肩"], 
                        ["单脚站立,左", "单脚站立,右"]],
            "Wednesday":[["深蹲", "俯身拉举,左","俯身拉举,右"], 
                        ["侧身平板支撑,左", "侧身平板支撑,右"], 
                        ["深蹲", "宽臂俯卧撑", "负重正跨步下蹲，左右"], 
                        ["平躺蹬自行车", "平躺蹬自行车"]],
            "Thursday": "Monday",
            "Friday": "Tuesday",
            "Saturday":  "Monday",
            'Sunday':  "Wednesday"
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
        self.today_workout = workout_data.get(current_day, [[('Missing day', 33)]])
        if isinstance(self.today_workout, str):
            self.today_workout = workout_data.get(self.today_workout, [[('Missing', 27)]])
        
        actions_passed = []
        action_doing = None
        actions_to_do = []
        # st.write("Today's Exercises:")
        for group in self.today_workout:
            print (group)
            # st.write(", ".join( group))
            actions_to_do.append("---")       
            actions_to_do.extend(group)
        # Workout loop
        # self.bt_skip = st.empty()
        self.display_action_passed = st.empty()
        self.main_placeholder_display = st.empty()
        self.display_action_to_do = st.empty()
        # Spacer
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        self.debug_text = st.empty()
        
        self.self_check()


        
        for group in self.today_workout:
            for exercise in group:
                duration  = self.training_set.get(exercise, 29)
                
                self.reader_out(exercise, is_next = True)
                self.rest_timer(10, extra_text = f"下一个动作:<br>{exercise}")

                self.reader_out(exercise, is_next = False)
                if action_doing != None:
                    actions_passed.append(action_doing)
                    actions_passed_note = "<br>".join(actions_passed)
                else:
                    actions_passed_note = ""
                
                if actions_to_do[0] == "---":
                    actions_to_do.pop(0)
                action_doing = actions_to_do.pop(0)
                
                actions_to_do_note = "<br>".join(actions_to_do)
                
                if actions_passed_note != "":
                    self.display_action_passed.markdown(f"<body style='text-align:center; font-size:20px; color: grey;font-weight:light;'>{actions_passed_note}</body>", unsafe_allow_html=True)
                if actions_to_do_note != "":
                    self.display_action_to_do.markdown(f"<body style='text-align:center; font-size:20px; color: white;font-weight:bold;'>{actions_to_do_note}</body>", unsafe_allow_html=True)
                self.workout_timer(duration, exercise)


            self.rest_timer(40)

        note ="Well done!<br>You've crushed it today!"
        self.main_placeholder_display.markdown(f"""<body style="text-align:center; font-size:80px; color: white;font-weight:bold;">{note}</body>""", unsafe_allow_html=True)

        self.speak("Well done, you've crushed it today!")

    def self_check(self):
        pass
        # for all the action from self.setting_map, make sure all of the key there is being used at least once in home schdule and gym scheduele.
        # if not, show them in self.debug_text
        self.debug_text.text = "OK"



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

        #https://cp.sync.com/mfs-60:17a21c594d1a7553c5a0352d2633d8d8=============================/u/next_%E5%8D%8A%E4%BB%B0%E5%93%91%E9%93%83%E4%B8%8A%E4%B8%BE.mp3?cachekey=60:17a21c594d1a7553c5a0352d2633d8d8=============================&datakey=WdMRuax3ta96cxCO9hLCy2LvjwirjdzO35ZAWKhItXn3ls52Dm7xZNKWr2G9ORN/N/26BcGdeES997GEFxchDjeMDL+r3cRHMBXaJU6wFzEbF56owV/XlQGWaFHbL4xyHTPL2qCv3lDKyZvQRTBUJKi7NQL0Q5Ofke8J4HQjqSFrXLi2wY2eRP3jfuIibzHw6xxqbpIfujGikIrwdymuY4oCWNdEjshBqj8/GkUaAH2mfYLjoGUPz9XZGT1DRg2YT3Ex8JIXlUpFtfbu8usFrWgXBO1BqPqswlQTEuuYhgm28GQOLTsMwnJc74GTAuDVcB8xNY3MVO/heaLo1Hww1w&mode=101&api_version=1&header1=Q29udGVudC1UeXBlOiBhdWRpby9tcGVn&header2=Q29udGVudC1EaXNwb3NpdGlvbjogaW5saW5lOyBmaWxlbmFtZT0ibmV4dF8lRTUlOEQlOEElRTQlQkIlQjAlRTUlOTMlOTElRTklOTMlODMlRTQlQjglOEElRTQlQjglQkUubXAzIjtmaWxlbmFtZSo9VVRGLTgnJ25leHRfJUU1JThEJThBJUU0JUJCJUIwJUU1JTkzJTkxJUU5JTkzJTgzJUU0JUI4JThBJUU0JUI4JUJFLm1wMzs&servtime=1695439522723&engine=cp-3.1.38&userid=2141860011&deviceid=4747950011&devicetypeid=3&access_token=3a608bbd02263318b8b85da9e4a086ddc31484ccb2aed67d9fdb2f22817874dd

        #https://cp.sync.com/mfs-60:8327c6c348789e2d445a632e7f258132=============================/u/next_%E4%BF%84%E7%BD%97%E6%96%AF%E8%BD%AC%E4%BD%93.mp3?cachekey=60:8327c6c348789e2d445a632e7f258132=============================&datakey=FDwLrncnj6DOAx6HqaQNQIdfpHICq9vDOpaS/RsdV/npGKahk6SptZmLspfLZUkWlAOqHc5PB0p0PfJj7pii2fdti+vI/rJXzmR2B4oA1KmEibkIdbiEzod5mAOZWlO3CXWZk19+bj+8Qd0hp1jNTaG5CSFvALISfG1spL/QByryAa7kwLpZSdbtKnsAuZlAnvoGnftgJFGSTPbSb9YPsrT2llbPz70KsHi3VpQD/p3OH8USvucdNG3Rd4sqU2G4dZjZyGuWyjfDgAdwhgYn28YXouR9C2tSw3gsyHnyuhrdhI1541/lc0ZNgKXp6rcpaDfsMeg/0UEqvEgT+2ieJA&mode=101&api_version=1&header1=Q29udGVudC1UeXBlOiBhdWRpby9tcGVn&header2=Q29udGVudC1EaXNwb3NpdGlvbjogaW5saW5lOyBmaWxlbmFtZT0ibmV4dF8lRTQlQkYlODQlRTclQkQlOTclRTYlOTYlQUYlRTglQkQlQUMlRTQlQkQlOTMubXAzIjtmaWxlbmFtZSo9VVRGLTgnJ25leHRfJUU0JUJGJTg0JUU3JUJEJTk3JUU2JTk2JUFGJUU4JUJEJUFDJUU0JUJEJTkzLm1wMzs&servtime=1695439602660&engine=cp-3.1.38&userid=2141860011&deviceid=4747950011&devicetypeid=3&access_token=3a608bbd02263318b8b85da9e4a086ddc31484ccb2aed67d9fdb2f22817874dd

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

    
    def reader_out(self, exercise, is_next = False):
        if is_next:
            file_path = f"audios\\next_{exercise}.mp3"
        else:
            file_path = f"audios\\start_{exercise}.mp3"
        
        # if not os.path.exists(file_path):
        #     return

        #file_raw = file_path.split("\\")[-1]
        #url  = f"https://cp.sync.com/mfs-60:8327c6c348789e2d445a632e7f258132=============================/u/{file_raw}?cachekey=60:8327c6c348789e2d445a632e7f258132=============================&datakey=FDwLrncnj6DOAx6HqaQNQIdfpHICq9vDOpaS/RsdV/npGKahk6SptZmLspfLZUkWlAOqHc5PB0p0PfJj7pii2fdti+vI/rJXzmR2B4oA1KmEibkIdbiEzod5mAOZWlO3CXWZk19+bj+8Qd0hp1jNTaG5CSFvALISfG1spL/QByryAa7kwLpZSdbtKnsAuZlAnvoGnftgJFGSTPbSb9YPsrT2llbPz70KsHi3VpQD/p3OH8USvucdNG3Rd4sqU2G4dZjZyGuWyjfDgAdwhgYn28YXouR9C2tSw3gsyHnyuhrdhI1541/lc0ZNgKXp6rcpaDfsMeg/0UEqvEgT+2ieJA&mode=101&api_version=1&header1=Q29udGVudC1UeXBlOiBhdWRpby9tcGVn&header2=Q29udGVudC1EaXNwb3NpdGlvbjogaW5saW5lOyBmaWxlbmFtZT0ibmV4dF8lRTQlQkYlODQlRTclQkQlOTclRTYlOTYlQUYlRTglQkQlQUMlRTQlQkQlOTMubXAzIjtmaWxlbmFtZSo9VVRGLTgnJ25leHRfJUU0JUJGJTg0JUU3JUJEJTk3JUU2JTk2JUFGJUU4JUJEJUFDJUU0JUJEJTkzLm1wMzs&servtime=1695439602660&engine=cp-3.1.38&userid=2141860011&deviceid=4747950011&devicetypeid=3&access_token=3a608bbd02263318b8b85da9e4a086ddc31484ccb2aed67d9fdb2f22817874dd"
        html_string = """
            <audio controls autoplay = "true">
                <source src={} type="audio/mp3">
            </audio>
            """.format(file_path)
        

        st.markdown("-----<br>--{}".format(file_path), unsafe_allow_html=True)
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



def system_autoplay_audio(file_path: str):
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



if __name__ == "__main__":
    


    import base64

    # import streamlit as st




    # st.write("# Auto-playing Audio!")

    # autoplay_audio("local_audio.mp3")

    main()