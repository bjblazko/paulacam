import spidev
import RPi.GPIO as GPIO

import time

#
# Python Driver based on Waveshare OLED 1,5" original driver for SSD1327.
# Slimmed down and applied Pythin coding style more or less.
#
# Device: https://www.waveshare.com/1.5inch-oled-module.htm
# Wiki: https://www.waveshare.com/wiki/1.5inch_OLED_Module
# Newer original files: https://www.waveshare.net/w/upload/2/2c/OLED_Module_Code.7z
#

#
# Raspberry GPIO pin numbers (BCM), adapt to your needs:
# https://pinout.xyz
#
OLED_RST_PIN = 25
OLED_DC_PIN = 24
OLED_CS_PIN = 8

SSD1351_WIDTH = 128
SSD1351_HEIGHT = 128
SSD1351_CMD_SETCOLUMN = 0x15
SSD1351_CMD_SETROW = 0x75
SSD1351_CMD_WRITERAM = 0x5C

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(OLED_RST_PIN, GPIO.OUT)
GPIO.setup(OLED_DC_PIN, GPIO.OUT)
GPIO.setup(OLED_CS_PIN, GPIO.OUT)
# init
GPIO.setwarnings(False)
GPIO.setup(OLED_RST_PIN, GPIO.OUT)
GPIO.setup(OLED_DC_PIN, GPIO.OUT)
GPIO.setup(OLED_CS_PIN, GPIO.OUT)

color_fill_byte = [0x00, 0x00] * SSD1351_WIDTH

SPI = spidev.SpiDev(0, 0)
SPI.max_speed_hz = 9000000
SPI.mode = 0b00


def set_coordinate(x, y):
    if (x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT):
        return
    # Set x and y coordinate
    write_command(SSD1351_CMD_SETCOLUMN)
    write_data(x)
    write_data(SSD1351_WIDTH - 1)
    write_command(SSD1351_CMD_SETROW)
    write_data(y)
    write_data(SSD1351_HEIGHT - 1)
    write_command(SSD1351_CMD_WRITERAM)


def display_image(Image):
    if Image is None:
        return

    set_coordinate(0, 0)
    buffer1 = Image.load()
    for j in range(0, SSD1351_WIDTH):
        for i in range(0, SSD1351_HEIGHT):
            color_fill_byte[i * 2] = ((buffer1[i, j][0] & 0xF8) | (buffer1[i, j][1] >> 5))
            color_fill_byte[i * 2 + 1] = (((buffer1[i, j][1] << 3) & 0xE0) | (buffer1[i, j][2] >> 3))
        write_datas(color_fill_byte)


def write_command(cmd):
    oled_cs(0)
    oled_dc(0)
    spi_writebyte([cmd])
    oled_cs(1)


def write_data(dat):
    oled_cs(0)
    oled_dc(1)
    spi_writebyte([dat])
    oled_cs(1)


def write_datas(data):
    oled_cs(0)
    oled_dc(1)
    spi_writebyte(data)
    oled_cs(1)


def oled_cs(x):
    if x == 1:
        GPIO.output(OLED_CS_PIN, GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_CS_PIN, GPIO.LOW)


def oled_dc(x):
    if x == 1:
        GPIO.output(OLED_DC_PIN, GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_DC_PIN, GPIO.LOW)


def oled_rst(x):
    if x == 1:
        GPIO.output(OLED_RST_PIN, GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_RST_PIN, GPIO.LOW)


def spi_writebyte(byte):
    SPI.writebytes(byte)


def delay(x):
    time.sleep(x / 1000.0)


def device_init():
    print('Initializing OLED...')
    oled_cs(0)
    oled_rst(0)
    delay(500)
    oled_rst(1)
    delay(500)

    write_command(0xfd)  # command lock
    write_data(0x12)
    write_command(0xfd)  # command lock
    write_data(0xB1)

    write_command(0xae)  # display off
    write_command(0xa4)  # Normal Display mode

    write_command(0x15)  # set column address
    write_data(0x00)  # column address start 00
    write_data(0x7f)  # column address end 95
    write_command(0x75)  # set row address
    write_data(0x00)  # row address start 00
    write_data(0x7f)  # row address end 63

    write_command(0xB3)
    write_data(0xF1)

    write_command(0xCA)
    write_data(0x7F)

    write_command(0xa0)  # set re-map & data format
    write_data(0x74)  # Horizontal address increment

    write_command(0xa1)  # set display start line
    write_data(0x00)  # start 00 line

    write_command(0xa2)  # set display offset
    write_data(0x00)

    write_command(0xAB)
    write_command(0x01)

    write_command(0xB4)
    write_data(0xA0)
    write_data(0xB5)
    write_data(0x55)

    write_command(0xC1)
    write_data(0xC8)
    write_data(0x80)
    write_data(0xC0)

    write_command(0xC7)
    write_data(0x0F)

    write_command(0xB1)
    write_data(0x32)

    write_command(0xB2)
    write_data(0xA4)
    write_data(0x00)
    write_data(0x00)

    write_command(0xBB)
    write_data(0x17)

    write_command(0xB6)
    write_data(0x01)

    write_command(0xBE)
    write_data(0x05)

    write_command(0xA6)

    clear_screen()
    write_command(0xaf)

    print('...done')


def clear_screen():
    ram_address()
    write_command(0x5c)
    color_fill_byte = [0x00, 0x00] * SSD1351_WIDTH
    oled_cs(0)
    oled_dc(1)
    for i in range(0, SSD1351_HEIGHT):
        spi_writebyte(color_fill_byte)
    oled_cs(1)


def ram_address():
    write_command(0x15)
    write_data(0x00)
    write_data(0x7f)
    write_command(0x75)
    write_data(0x00)
    write_data(0x7f)
