from train_main import WorkoutGuide


not_in_schedule_keys, not_in_data_keys = WorkoutGuide(True).self_check()

print ("-------- now copy below line to the schedule list----------") if len(not_in_schedule_keys) > 0 else print ("--")

for key in not_in_schedule_keys:
    print (f'"{key}",')


print ("------- now copy below line to the json file-------------") if len(not_in_data_keys) > 0 else print ("--")

for key in not_in_data_keys:
    print (f'"{key}":30,')