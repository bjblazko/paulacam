import threading
import time

from RPi import GPIO

#
# GPIO pins (BCM)
#
GPIO_PIN_CLK = 17
GPIO_PIN_DT = 18
GPIO_PIN_BUTTON = 14


class RotaryEncoder():

    __last_value = 0

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def on_click(self, callback):
        GPIO.add_event_detect(GPIO_PIN_BUTTON, GPIO.FALLING, callback=callback, bouncetime=2500)

    def on_rotate(self, callback_clockwise, callback_counter_clockwise):
        rotation_thread = threading.Thread(target=detect_rotation, args=(callback_clockwise, callback_counter_clockwise), daemon=True)
        rotation_thread.start()


def detect_rotation(callback_clockwise, callback_counter_clockwise):
    clk_last_state = GPIO.input(GPIO_PIN_CLK)

    while True:
        clk_state = GPIO.input(GPIO_PIN_CLK)
        dt_state = GPIO.input(GPIO_PIN_DT)
        if clk_state != clk_last_state:
            clk_last_state = clk_state
            if dt_state != clk_state:
                callback_clockwise()
            else:
                callback_counter_clockwise()
        time.sleep(0.01)



