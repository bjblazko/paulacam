import glob
import os
import time

# pip3 install Pillow (tested w/ 9.0.1)
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import lib.ColorOled128 as Oled
from lib.RotaryEncoder import RotaryEncoder

# https://picamera.readthedocs.io/en/release-1.13/install.html
__displayCounter = 0
__photo_list = list


def read_photos():
    print("--> READ pics")
    global __photo_list
    __photo_list = glob.glob("*.jpeg")
    print(f'Fetched {__photo_list.__sizeof__()}')
    #for i in __photo_list:
        #print(__photo_list[i])

def trigger_pressed(channel):
    print(f'------> Detected {channel}')
    photo_name = f'img-{time.time()}'
    image = __take_photo(photo_name)
    read_photos()
    __show_photo(image)


def __take_photo(name):
    filename = f'{name}.jpeg'
    cmdline = f'''
    libcamera-still \
    --camera 0 \
    --output {filename} \
    --immediate \
    --nopreview
    '''
    exec_result = os.system(cmdline)
    # print(exec_result)
    print(f'Saving picture to {filename}')
    time.sleep(1)
    return Image.open(filename)


def __show_photo(image):
    Oled.device_init()
    global __displayCounter
    __displayCounter = 0
    resized = image.resize((128, 96))
    draw = ImageDraw.Draw(resized)

    font = ImageFont.truetype('./resources/roboto-regular.ttf', 24)
    draw.text((2, 6), 'PaulaCam', fill="WHITE", font=font)
    draw.line([(0, 32), (128, 32)], fill="RED", width=2)
    Oled.display_image(resized)
    time.sleep(5)
    Oled.clear_screen()


def rotate_left():
    print("Left")


def rotate_right():
    print("Right")


if __name__ == '__main__':
    rotaryEncoder = RotaryEncoder()
    rotaryEncoder.on_click(trigger_pressed)
    rotaryEncoder.on_rotate(rotate_left, rotate_right)

    while True:
        print(f'OLED active for the last {__displayCounter} seconds')
        time.sleep(10)
        __displayCounter = __displayCounter + 10
        if __displayCounter > 30:
            print("OLED active for more than 30 seconds, turning black...")
            Oled.clear_screen()
