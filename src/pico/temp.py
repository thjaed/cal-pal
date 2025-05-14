from pybuttons import Button


def press_handler(btn, pattern):
    print("button", btn.get_id(), end=" ")
    if pattern == Button.SINGLE_PRESS:
        print("single pressed")
    elif pattern == Button.DOUBLE_PRESS:
        print("double pressed")
    elif pattern == Button.LONG_PRESS:
        print("long pressed")
        
# Pin numbers for your buttons
PINS = [12, 13, 14, 15]

# Create buttons
buttons = []

for pin in PINS:
    btn = Button(Button.MODE_DIGITAL, pin)

    btn.on_press(press_handler) \
       .on_press_for(press_handler, 700)  # 1000ms = long press
       
    buttons.append(btn)

while True:
    for btn in buttons:
        btn.read()