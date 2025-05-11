import utime
import ujson

current_time = utime.localtime()

day_start_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 0, 0, 0, current_time[6], current_time[7]))
day_end_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 23, 59, 59, current_time[6], current_time[7]))

todays_events = []

with open("calendar.jsonl", "r") as f:
    for event in f:
        event = eval(event)
        start_sec = event.get("start")
        
        if (start_sec >= day_start_sec) and (start_sec <= day_end_sec):
            todays_events.append(event)
            
with open("cal_today.jsonl", "w") as f:
    for event in todays_events:
        ujson.dump(event, f)
        f.write("\n")