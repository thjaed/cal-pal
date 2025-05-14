import utime
import ujson

def gen_cal_day(secs):
    current_time = utime.localtime(secs)

    day_start_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 0, 0, 0, current_time[6], current_time[7]))
    day_end_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 23, 59, 59, current_time[6], current_time[7]))

    todays_events = []

    with open("calendar.jsonl", "r") as f:
        for line in f:
            event = ujson.loads(line)
            start_sec = event.get("start")

            if (start_sec >= day_start_sec) and (start_sec <= day_end_sec):
                todays_events.append(event)

    with open("cal_today.jsonl", "w") as f:
        for event in todays_events:
            ujson.dump(event, f)
            f.write("\n")

# Months and days as strings for displaying date
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_clock(secs):
    time = utime.localtime(secs)
    
    # gets hour and minuite from time
    # Adds a 0 in front if less than 9
    hour = str(time[3]) if time[3] > 9 else f"0{time[3]}"
    minute = str(time[4]) if time[4] > 9 else f"0{time[4]}"
    
    return f"{hour}:{minute}"

def get_date(secs):
    time = utime.localtime(secs)
    
    day = days[time[6]]
    month = months[time[1] - 1]
    
    return f"{day} {time[2]} {month}"