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
        
        self.context = "home"
        self.scroll_distance = 0
        self.box_height = 0
        self.event_heights = []
        
    def clear(self):
        self.display.set_backlight(0.8)
        self.display.set_pen(self.BLACK)
        self.display.clear()

    def clear_event_area(self):
        self.display.set_pen(self.BLACK)
        self.display.rectangle(0, 16, 320, 224)

    def update(self):
        self.display.update()
    
    def scroll_events(self, direction):
        visible_height = 225
        scroll_offset = -self.scroll_distance
        curr_height = 0

        if direction == "down":
            for box_height in self.event_heights:
                box_top = curr_height
                box_bottom = curr_height + box_height

                if box_bottom > scroll_offset + visible_height:
                    self.scroll_distance = -(box_bottom - visible_height)
                    return

                curr_height += box_height

        elif direction == "up":
            for index, box_height in enumerate(self.event_heights):
                box_top = curr_height

                if box_top >= scroll_offset:
                    if index > 0:
                        self.scroll_distance = -sum(self.event_heights[:index - 1])
                    else:
                        self.scroll_distance = 0
                    return

                curr_height += box_height
        
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
    
    def draw_event_box(self, total_content_height, title, time, location, attendees):
            self.total_content_height = total_content_height
            start_y = 16 + self.scroll_distance + total_content_height
            line_y = start_y
            
            self.box_height = 0
            
            if title: self.box_height += 20
            if time: self.box_height += 14
            if location: self.box_height += 14
            if attendees: self.box_height += 14
            
            self.box_height += 2
            self.event_heights.append(self.box_height)
            
            self.display.set_pen(self.GREY)
            self.display.rectangle(0, start_y, 320, self.box_height)
            self.display.set_pen(self.WHITE)
            self.display.line(0, self.box_height + line_y - 1, 320, self.box_height + line_y - 1) # Bottom bar
            
            self.display.set_pen(self.WHITE)
            
            if title:
                self.display.text(title, 5, line_y, scale=3)
                line_y += 20
            if time:
                self.display.text(time, 5, line_y, scale=2)
                line_y += 14
            if location:
                self.display.text(location, 5, line_y, scale=2)
                line_y += 14    
            if attendees:
                self.display.text(attendees, 5, line_y, scale=2)
                line_y += 14
                

