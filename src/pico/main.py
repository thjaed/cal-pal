import utime
import ujson
import asyncio
from pybuttons import Button

import calendar
import battery
from ui import UI

ui = UI()
ui.clear()
fps = 30
sleep_time = int((1/fps) * 1000)

PINS = [12, 13, 14, 15]
buttons = []

def press_handler(btn, pattern):
    if pattern == Button.SINGLE_PRESS and btn.get_id() == 14: # Button X
        ui.scroll_events(direction="up")
        update_events_page()
    elif pattern == Button.SINGLE_PRESS and btn.get_id() == 15: # Button Y
        ui.scroll_events(direction="down")
        update_events_page()

for pin in PINS:
    btn = Button(Button.MODE_DIGITAL, pin)

    btn.on_press(press_handler) \
       .on_press_for(press_handler, 700)  # 700ms = long press
    buttons.append(btn)

async def monitor_buttons():
    while True:
        for btn in buttons:
            btn.read()
        await asyncio.sleep_ms(10) # 10ms poll time
        
def update_menu_bar():
        time_secs = utime.time()

        clock = calendar.get_clock(time_secs)
        date = calendar.get_date(time_secs)
        battery_level = battery.percentage()
        
        ui.draw_menu_bar(clock=clock,
                         date=date,
                         battery_level=battery_level,
                         charging=battery.charging()
                         )

def update_events_page():
    ui.clear_event_area()
    
    with open("cal_today.jsonl", "r") as f:
        total_content_height = 0
        ui.event_heights = []
        for line in f:
            event = ujson.loads(line)
 
            ui.draw_event_box(
                total_content_height=total_content_height,
                title=event.get("title"),
                time=f"{calendar.get_clock(event.get('start'))} - {calendar.get_clock(event.get('end'))}",
                location=event.get("location"),
                attendees=event.get("attendees")
            )
            
            total_content_height += ui.box_height
            
    
    update_menu_bar()

async def update_menu_bar_loop():
    while True:
        update_menu_bar()
        await asyncio.sleep_ms(1000)
         
async def main():
    asyncio.create_task(monitor_buttons())
    asyncio.create_task(update_menu_bar_loop())
    
    while True:
        ui.update()
        await asyncio.sleep_ms(sleep_time)
        
update_events_page()
asyncio.run(main())

