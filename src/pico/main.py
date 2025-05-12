from machine import ADC, Pin
import utime
import ujson
import asyncio

import calendar
import battery
from ui import UI

ui = UI()
ui.clear()

while True:
    time_secs = utime.time()
    
    clock = calendar.get_clock(time_secs)
    date = calendar.get_date(time_secs)
    battery_level = battery.percentage()
    
    ui.draw_menu_bar(clock=clock,
                     date=date,
                     battery_level=battery_level,
                     charging=battery.charging()
                     )
    
    with open("cal_today.jsonl", "r") as f:
        for index, line in enumerate(f):
            event = eval(line)
            
            ui.draw_event_box(
                index=index,
                title=event.get("title"),
                time=f"{calendar.get_clock(event.get('start'))} - {calendar.get_clock(event.get('end'))}",
                location=event.get("location"),
                attendees="Attendees Placeholder"
                )     
        
    ui.update()