import time
import pyttsx3

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
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def workout_timer(self, duration, exercise):
        self.speak(f"Start {exercise}")
        for sec in range(duration, 0, -1):
            print(f"{sec} seconds remaining.")
            time.sleep(1)
        self.speak("Time's up! Next one.")

    def rest_timer(self, duration):
        self.speak(f"Rest for {duration} seconds")
        for sec in range(duration, 0, -1):
            print(f"{sec} seconds remaining.")
            time.sleep(1)
        self.speak("Rest time's over! Get ready.")

    def execute_workout(self):
        current_day = time.strftime("%A")
        print(f"Today is {current_day}, let's get started!")
        today_workout = self.workout_schedule.get(current_day, [[('Rest', 1)]])

        for group in today_workout:
            for exercise, duration in group:
                self.workout_timer(duration, exercise)
            self.rest_timer(40)

        print("Well done, you've crushed it today!")
        self.speak("Well done, you've crushed it today!")

if __name__ == "__main__":
    guide = WorkoutGuide()
    guide.execute_workout()
