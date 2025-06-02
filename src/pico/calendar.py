import utime
import ujson
import os

class Calendar:
    def __init__(self):
        self.cal_generated_today = False
        # Months and days as strings for displaying date
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def gen_cal_day(self, secs): # Generates a cal_today.jsonl file containing events for the day given
        current_time = utime.localtime(secs)

        day_start_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 0, 0, 0, current_time[6], current_time[7]))
        day_end_sec = utime.mktime((current_time[0], current_time[1], current_time[2], 23, 59, 59, current_time[6], current_time[7]))

        todays_events = []

        if "calendar.jsonl" not in os.listdir():
            with open("calendar.jsonl", "w"): pass
        else:
            with open("calendar.jsonl", "r") as f:
                for line in f:
                    event = ujson.loads(line)
                    start_sec = event.get("start")

                    if (start_sec >= day_start_sec) and (start_sec <= day_end_sec): # If today
                        todays_events.append(event)

            with open("cal_today.jsonl", "w") as f:
                for event in todays_events:
                    ujson.dump(event, f)
                    f.write("\n")

    def get_clock(self, secs): # Returns a clock string from timestamp
        time = utime.localtime(secs)

        # gets hour and minuite from time
        # Adds a 0 in front if less than 9
        hour = str(time[3]) if time[3] > 9 else f"0{time[3]}"
        minute = str(time[4]) if time[4] > 9 else f"0{time[4]}"

        return f"{hour}:{minute}"

    def get_date(self, secs): # Returns a date string from timestamp
        time = utime.localtime(secs)

        day = self.days[time[6]]
        month = self.months[time[1] - 1]

        return f"{day} {time[2]} {month}"

    def update_calendar(self):
        time = utime.time()
        localtime = utime.localtime()
        if (localtime[3] == 23 and localtime[4] == 59) and self.cal_generated_today == True:
               self.cal_generated_today = False

        # Generate calendar if it does not exist
        if "cal_today.jsonl" not in os.listdir():
            self.gen_cal_day(time)
            self.cal_generated_today = True
            return True

        # Generate calendar at start of day
        elif (localtime[3] == 0 and localtime[4] == 0) and self.cal_generated_today == False:
            self.gen_cal_day(time)
            self.cal_generated_today = True
            return True
        
        else:
            return False
    
    def remove_past_events(self):
        time = utime.time()
        with open("cal_today.jsonl", "r") as f:
            future_events = []
            total_events = 0
            for line in f:
                total_events += 1
                event = ujson.loads(line)
                if event.get('end') > time:
                    future_events.append(event)
                    
        if len(future_events) < total_events:
            with open("cal_today.jsonl", "w") as f:
                for event in future_events:
                    ujson.dump(event, f)
                    f.write("\n")
            return True
        else:
            return False