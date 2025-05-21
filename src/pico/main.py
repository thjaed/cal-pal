import asyncio
import utime
from pybuttons import Button
from ui import Menu, MenuBar, Home
import ui
import calendar

menu = Menu()
bar = MenuBar()
home = Home()

sleeping = False
sleep_time = 20
last_interaction_time = utime.time()

fps = 30
display_update_time = int((1/fps) * 1000) # Calculates time to sleep in ms
ui.setup()

def press_handler(btn, pattern):
    global last_interaction_time, sleeping
    last_interaction_time = utime.time()
    if sleeping:
        device_wake_up()
    else:
        if pattern == Button.SINGLE_PRESS:
            if btn.get_id() == BUTTON_A:
                if ui.page == "menu":
                    menu.exec() # Run the code associated with the button

            if btn.get_id() == BUTTON_B:
                if ui.page == "home": # Go to menu page
                    menu.go()
                elif ui.page == "menu": # Go to home page
                    home.go()

            if btn.get_id() == BUTTON_X:
                if ui.page == "home": # Scroll events page up
                    home.scroll(direction="up")
                elif ui.page == "menu": # Highlight the button above
                    menu.scroll(direction="up")

            elif btn.get_id() == BUTTON_Y:
                if ui.page == "home":  # Scroll events page down
                    home.scroll(direction="down")
                elif ui.page == "menu": # Highlight the button below
                    menu.scroll(direction="down")

def device_to_sleep():
    global sleeping
    sleeping = True
    ui.screen_off()

def device_wake_up():
    global sleeping
    sleeping = False
    ui.screen_on()

async def monitor_buttons():
    while True:
        for btn in buttons:
            btn.read()
        await asyncio.sleep_ms(10) # 10ms poll time

async def update_menu_bar():
    while True:
        if ui.page == "home" and not sleeping:
            bar.draw()
        await asyncio.sleep_ms(1000) # Refresh menu bar every sec

async def sleep_handler():
    global last_interaction_time, sleeping
    while True:
        time = utime.time()
        if time - 20 > last_interaction_time:
            device_to_sleep()
        await asyncio.sleep_ms(display_update_time)

async def main():
    asyncio.create_task(monitor_buttons())
    asyncio.create_task(update_menu_bar())
    asyncio.create_task(sleep_handler())

    while True:
        if not sleeping:
            ui.update()
        await asyncio.sleep_ms(display_update_time)

# Button setup
PINS = [12, 13, 14, 15]
BUTTON_A = 12
BUTTON_B = 13
BUTTON_X = 14
BUTTON_Y = 15
buttons = []

for pin in PINS:
    btn = Button(Button.MODE_DIGITAL, pin)

    btn.on_press(press_handler) \
       .on_press_for(press_handler, 700)  # 700ms = long press
    buttons.append(btn)

home.go()
asyncio.run(main())