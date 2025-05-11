from icalendar import Calendar
from datetime import datetime
import json
import sys
import time

start_time = time.time()

input_file = sys.argv[1]

with open(input_file, "rb") as f:
    cal = Calendar.from_ical(f.read())

events = []

for event in cal.events:
    
    new_event = {
        "title": event.get("SUMMARY"),
        "start": int(event.get("DTSTART").dt.timestamp()),
        "end": int(event.get("DTEND").dt.timestamp()),
        "attendees": event.get("ATTENDEE"),
        "location": event.get("LOCATION")
        }
    
    new_event = {key: value for key, value in new_event.items() if value is not None}
            
    rrule = event.get("RRULE")
    
    if rrule:
        
        repeat = {
        "freq": rrule.get("FREQ", [None])[0],
        "interval": int(rrule.get("INTERVAL", [1])[0]),
        "byday": rrule.get("BYDAY", []),
        }
        
        until = rrule.get("UNTIL")
        if isinstance(until, list):
            repeat["until"] = int(until[0].timestamp())
        else:
            repeat["until"] = int(until.dt.timestamp())

        
        repeat = {key: value for key, value in repeat.items() if value is not None}
        
        new_event["repeat"] = repeat

    events.append(new_event)
    
events.sort(key=lambda e: e["start"])

with open("calendar.jsonl", "w") as f:
    for event in events:
        json.dump(event, f)
        f.write("\n")
    
print(f"Converted {len(events)} events in {round(time.time() - start_time, 4)} seconds")