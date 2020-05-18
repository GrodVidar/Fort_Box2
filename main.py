from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import RPi.GPIO as GPIO
import Keypad

from time import sleep, strftime
from datetime import datetime

from subprocess import call
ROWS = 4
COLS = 4
keys = ['1', '2', '3', 'A',
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D']

row_pins = [12, 16, 18, 22]
col_pins = [19, 15, 13, 11]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
servo1 = GPIO.PWM(7, 50)
servo1.start(3)
sleep(0.2)


def get_cpu_temp():
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format(float(cpu)/1000) + ' C'


def get_time_now():
    return datetime.now().strftime('   %H:%M:%S')


def lock_servo():
    servo1.ChangeDutyCycle(3)
    sleep(0.2)


def open_servo():
    servo1.ChangeDutyCycle(8)
    sleep(0.2)


def loop():
    mcp.output(3, 1)
    lcd.begin(16, 2)
    keypad = Keypad.Keypad(keys, row_pins, col_pins, ROWS, COLS)
    keypad.setDebounceTime(50)
    while True:
        idle = True
        while idle:
            lcd.setCursor(0, 0)
            lcd.message('CPU: ' + get_cpu_temp() + '\n')
            lcd.message(get_time_now())
            # check if keypad says *
            key = keypad.getKey()
            if key != keypad.NULL:
                print("you pressed key: ", key)
                if key == '*':
                    idle = False
                elif key == '#':
                    lock_servo()
                elif key == 'A':
                    destroy()
                    call("sudo poweroff", shell=True)
            sleep(1)
        lcd.clear()
        active = True
        run_once = True
        while active:
            if run_once:
                with open('text.txt', 'r') as f:
                    code = f.readline().rstrip()
                run_once = False
            lcd.setCursor(0, 0)
            lcd.message("Enter Code:\n")
            message = ''
            entering = True
            while entering:
                key = keypad.getKey()
                if key != keypad.NULL:
                    if key == '*':
                        entering = False
                    else:
                        message += key
                        lcd.setCursor(0, 1)
                        lcd.message(message)
            # lcd.message(message)
            if message == code:
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.message("Opening!")
                open_servo()
                sleep(1)
                active = False
            else:
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.message("WRONG CODE!!!")
                sleep(1)
                lcd.clear()


def destroy():
    servo1.stop()
    lcd.clear()
    GPIO.cleanup()


PCF8574_address = 0x27
PCF8574A_address = 0x3F

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except Exception as e:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except Exception as ex:
        print("I2C address error!")
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
