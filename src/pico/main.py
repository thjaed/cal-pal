from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2 # type: ignore
import utime
from machine import ADC, Pin

vsys = ADC(Pin(29))                 # reads the system input voltage
charging = Pin(24, Pin.IN)          # reading GP24 tells us whether or not USB power is connected
conversion_factor = 3 * 3.3 / 65535

full_battery = 4.2                  # reference voltages for a full/empty battery, in volts
empty_battery = 2.8                 # the values could vary by battery size/manufacturer so you might need to adjust them

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)

WHITE = display.create_pen(255, 255, 255)
GREY = display.create_pen(80, 80, 80)
BLACK = display.create_pen(0, 0, 0)
GREEN = display.create_pen(0, 255, 0)

display.set_backlight(0.8)
display.set_pen(BLACK)
display.clear()

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

while True:
    time = utime.localtime(utime.time())
    
    hour = str(time[3]) if time[3] > 9 else f"0{time[3]}"
    minute = str(time[4]) if time[4] > 9 else f"0{time[4]}"
    second = str(time[5]) if time[5] > 9 else f"0{time[5]}"
    
    day = days[time[6]]
    month = months[time[1] - 1]
    
    clock = f"{hour}:{minute}:{second}"
    date = f"{day} {time[2]} {month}"
    
    # convert the raw ADC read into a voltage, and then a percentage    
    voltage = vsys.read_u16() * conversion_factor
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100
    
    percentage_text = f"{round(percentage)}%"
    
    clock_width = display.measure_text(clock, scale=2)
    date_width = display.measure_text(date, scale=2)
    percentage_width = display.measure_text(percentage_text, scale=2)
    
    display.set_pen(GREY)
    display.rectangle(0, 0, 320, 15)
    
    display.set_pen(WHITE)
    display.set_font("bitmap6")
    display.text(clock, 0, 0, scale=2)
    display.text(date, int((320 / 2) - (date_width / 2)), 0, scale=2)
    
    if charging.value() == 1:
        display.set_pen(GREEN)       
    display.text(percentage_text, 320-percentage_width, 0, scale=2)
    
    
    display.update()