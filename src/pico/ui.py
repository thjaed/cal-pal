from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2 # type: ignore

class UI:
    def __init__(self):
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=0)
        
        # Colours
        self.WHITE = self.display.create_pen(255, 255, 255)
        self.GREY = self.display.create_pen(80, 80, 80)
        self.DARK_GREY = self.display.create_pen(60, 60, 60)
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.GREEN = self.display.create_pen(0, 255, 0)   
    
    def clear(self):
        self.display.set_backlight(0.8)
        self.display.set_pen(self.BLACK)
        self.display.clear()
        
    def draw_menu_bar(self, clock, date, battery_level, charging):
        clock_width = self.display.measure_text(clock, scale=2)
        date_width = self.display.measure_text(date, scale=2)

        self.display.set_pen(self.GREY)
        self.display.rectangle(0, 0, 320, 15) # Top bar
        self.display.set_pen(self.WHITE)
        self.display.line(0, 14, 320, 14)

        self.display.set_pen(self.WHITE)
        self.display.set_font("bitmap6")
        self.display.text(clock, 0, 0, scale=2) # Clock
        self.display.text(date, int((clock_width + (290 - clock_width) / 2) - (date_width / 2)), 0, scale=2) # Date

        self.display.set_pen(self.WHITE)
        self.display.rectangle(290, 2, 25, 10) # White border
        self.display.rectangle(315, 4, 2, 6) # Notch
        self.display.set_pen(self.GREY)
        self.display.rectangle(292, 4, 21, 6) # Grey background

        if charging:
            self.display.set_pen(self.GREEN) # Battery icon green if charging
        else:
            self.display.set_pen(self.WHITE)

        self.display.rectangle(293, 5, (round((battery_level / 100) * 19)), 4) # Charge level
    
    def draw_event_box(self, index, title, time, location, attendees):
            y_offset = 16 + (index * 75)

            self.display.set_pen(self.GREY)
            self.display.rectangle(0, y_offset, 320, 75) # Event box
            self.display.set_pen(self.WHITE)
            self.display.line(0, y_offset + 74, 320, y_offset + 74) # Bottom bar

            self.display.text(title, 5, y_offset + 2, scale=3) # Title
            self.display.text(time, 5, y_offset + 27, scale=2) # Time
            self.display.text(location, 5, y_offset + 42, scale=2) # Location
            self.display.text(attendees, 5, y_offset + 57, scale=2) # Attendees
    
    def update(self):
        self.display.update()