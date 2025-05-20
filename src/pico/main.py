import asyncio
import utime
from pybuttons import Button
from ui import Menu, MenuBar, Home
import ui
import calendar

menu = Menu()
bar = MenuBar()
home = Home()

fps = 30
sleep_time = int((1/fps) * 1000) # Calculates time to sleep in ms
ui.setup()

def press_handler(btn, pattern):
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

async def monitor_buttons():
    while True:
        for btn in buttons:
            btn.read()
        await asyncio.sleep_ms(10) # 10ms poll time

async def update_menu_bar():
    while True:
        if ui.page == "home":
            bar.draw()
        await asyncio.sleep_ms(1000) # Refresh menu bar every sec

async def main():
    asyncio.create_task(monitor_buttons())
    asyncio.create_task(update_menu_bar())

    while True:
        ui.update()
        await asyncio.sleep_ms(sleep_time)

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

home.draw()
asyncio.run(main())