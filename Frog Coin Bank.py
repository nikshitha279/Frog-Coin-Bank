from machine import Pin, PWM, TouchPad, ADC
import time
import neopixel

# Setup servo motor
servo = PWM(Pin(5), freq=50)

# Setup capacitive touch sensor
touch = TouchPad(Pin(4))

# Setup sound sensor (analog input)
sound_sensor = ADC(Pin(34))
sound_sensor.atten(ADC.ATTN_11DB)  # Full range (0-3.3V)

# Setup Neopixel (16 LEDs)
np = neopixel.NeoPixel(Pin(27), 16)  # Neopixel on GPIO14, 16 LEDs

# Function to set servo angle
def set_angle(angle):
    duty = int(((angle / 180) * 102) + 26)  # Map 0-180° to duty cycle
    servo.duty(duty)

# Function to set all Neopixel LEDs to a color
def set_neopixel(r, g, b):
    for i in range(16):  # Loop through all 16 pixels
        np[i] = (r, g, b)
    np.write()

# Function for rainbow effect on all pixels
def rainbow_effect():
    colors = [
        (255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
        (0, 255, 255), (0, 0, 255), (127, 0, 255), (255, 0, 127)
    ]
    print("Running Rainbow Effect...")
    for color in colors:
        for i in range(16):
            np[i] = color
        np.write()
        time.sleep(0.2)

    print("Turning off LEDs after rainbow effect")
    set_neopixel(0, 0, 0)  # Turn off LEDs
    time.sleep(0.5)  # Small delay before rechecking input

# Thresholds
sound_threshold = 2000  # Adjust based on your sensor
touch_threshold = 300  # Adjust for touch sensitivity

# Start at 90° (neutral position)
set_angle(90)

while True:
    sound_level = sound_sensor.read()
    touch_value = touch.read()

    if sound_level < sound_threshold:  # If silent
        if touch_value < touch_threshold:  # If touch detected
            print("Touch detected, moving servo")
            set_neopixel(0, 255, 0)  # Green (ready to take action)

            # Move to 0° (anticlockwise)
            set_angle(0)
            time.sleep(0.5)

            # Move to 180° (clockwise)
            set_angle(180)
            time.sleep(0.5)

            # Run the rainbow effect and then turn off LEDs
            rainbow_effect()

    else:
        print("Sound detected!")
        set_neopixel(255, 0, 0)  # Red (sound detected)

    time.sleep(0.1)  # Small delay for stability
