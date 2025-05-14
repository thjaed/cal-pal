import utime
import ujson
import asyncio
from pybuttons import Button

import calendar
import battery
from ui import UI

ui = UI()
ui.clear()

def press_handler(btn, pattern):
    if pattern == Button.SINGLE_PRESS and btn.get_id() == 15:
        ui.scroll += -50
    elif pattern == Button.SINGLE_PRESS and btn.get_id() == 14:
        ui.scroll += 50
        
# Pin numbers for your buttons
PINS = [12, 13, 14, 15]

# Create buttons
buttons = []

for pin in PINS:
    btn = Button(Button.MODE_DIGITAL, pin)

    btn.on_press(press_handler) \
       .on_press_for(press_handler, 700)  # 1000ms = long press
       
    buttons.append(btn)

async def monitor_buttons():
    while True:
        for btn in buttons:
            btn.read()
        await asyncio.sleep_ms(10)
        
async def main():
    asyncio.create_task(monitor_buttons())
    
    while True:
        time_secs = utime.time()

        clock = calendar.get_clock(time_secs)
        date = calendar.get_date(time_secs)
        battery_level = battery.percentage()

        

        with open("cal_today.jsonl", "r") as f:
            ui.clear_event_area()
            for index, line in enumerate(f):
                event = ujson.loads(line)
                
                ui.draw_event_box(
                    index=index,
                    title=event.get("title"),
                    time=f"{calendar.get_clock(event.get('start'))} - {calendar.get_clock(event.get('end'))}",
                    location=event.get("location"),
                    attendees="Attendees Placeholder"
                    )     
                
        ui.draw_menu_bar(clock=clock,
                         date=date,
                         battery_level=battery_level,
                         charging=battery.charging()
                         )

        ui.update()
        await asyncio.sleep_ms(33)

asyncio.run(main())
