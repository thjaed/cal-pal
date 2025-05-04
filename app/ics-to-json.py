from icalendar import Calendar
from datetime import datetime
import json
import sys
import time

start_time = time.time()

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "rb") as f:
    cal = Calendar.from_ical(f.read())

events = []

for event in cal.events:
    title = event.get("SUMMARY")
    start = event.get("DTSTART").dt.isoformat()
    end = event.get("DTEND").dt.isoformat()
    attendee = event.get("ATTENDEE")
    location = event.get("LOCATION")
    
    new_event = {
        "title": title,
        "start": start,
        "end": end,
        "attendees": attendee,
        "location": location
        }
    
    # Remove empty values    
    new_event = {key: value for key, value in new_event.items() if value is not None}
    
    events.append(new_event)
    

events.sort(key=lambda e: e["start"])

with open(output_file, "w") as f:
    json.dump(events, f, indent=2)
    
print(f"Converted {len(events)} events in {round(time.time() - start_time, 4)} seconds")