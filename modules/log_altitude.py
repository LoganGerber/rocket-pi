from ctypes import c_bool
import multiprocessing as mp
import datetime
import signal
import time
import os
import sys

import board
import busio
import adafruit_bmp3xx
from gpiozero import LED

LOG_RATE = 20

def LogAltitude(rate, stop_event):
    try:
        # Set up altimeter info
        i2c = busio.I2C(board.SCL, board.SDA)
        bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

        bmp.pressure_oversampling = 8

        # Get the average pressure of 40 samples over roughly 2 seconds
        avg_pressure = 0
        avg_sample_count = 0

        for i in range(40):
            avg_pressure = (avg_pressure * avg_sample_count + bmp.pressure) / (avg_sample_count + 1)
            avg_sample_count += 1
            time.sleep(1/20)

        # Set the baseline pressure to this average, effectively setting our current altitude to zero
        bmp.sea_level_pressure = avg_pressure

        # Get the current date and time to use for creating the log directory and file
        current_date = str(datetime.datetime.now()).split(' ')

        # Remove the decimals from the seconds in the current time
        current_date[1] = current_date[1].split('.')[0]

        # Replace the ':' with '-' in the current time
        current_date[1] = current_date[1].replace(':', '-')

        # Ensure the log directory exists
        log_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(log_dir, '../logs/altitude/{}'.format(current_date[0]))

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create log file
        log_name = current_date[1] + '-altitude.log'
        log = open(os.path.join(log_dir, log_name), 'w')

        # Logging loop
        while not stop_event.is_set():
            log.write('{} {}\n'.format(str(datetime.datetime.now().time()), str(bmp.altitude)))
            time.sleep(1/rate)

        log.close()
    except:
        led = LED(26)
        led.blink(on_time=0.5, off_time=0.5)

        stop_event.wait()

def DoNothing(signal, frame):
    pass

if __name__ == '__main__':

    stop_token = mp.Event()

    log_process = mp.Process(target=LogAltitude, args=(LOG_RATE, stop_token), name='Log Altitude')
    log_process.start()

    signal.signal(signal.SIGTERM, DoNothing)
    signal.signal(signal.SIGHUP, DoNothing)

    signal.pause()

    stop_token.set()
    log_process.join(10)

