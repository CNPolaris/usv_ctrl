import time
import serial
import binascii

from utils.logger import logger

ser = serial.Serial(
    port='com3',
    baudrate=57600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
every_time = time.strftime('%Y-%m-%d %H:%M:%S')
data = ''

if not ser.isOpen():
    ser.open()

while True:
    data = ser.readline()

    print(every_time, data)
