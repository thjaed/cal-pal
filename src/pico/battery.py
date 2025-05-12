from machine import ADC, Pin

# system input voltage
vsys = ADC(Pin(29))  
# tells us whether or not USB power is connected          
recieving_power = Pin(24, Pin.IN)          

conversion_factor = 3 * 3.3 / 65535

# reference voltages for a full/empty battery, in volts
# the values could vary by battery size/manufacturer so you might need to adjust them
full_battery = 4.2
empty_battery = 2.8

def percentage():
    # convert the raw ADC read into a voltage, and then a percentage    
    voltage = vsys.read_u16() * conversion_factor
    percentage = round(100 * ((voltage - empty_battery) / (full_battery - empty_battery)))
    if percentage > 100:
        percentage = 100
    
    return percentage

def charging():
    if recieving_power.value() == 1:
        return True
    else:
        return False