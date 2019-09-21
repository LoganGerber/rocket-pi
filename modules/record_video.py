import os
import time
import datetime

import picamera
import gpiozero

from utils.button_timer import ButtonTimer

if __name__ == '__main__':
    try:
        led = gpiozero.LED(26)

        should_record = False
        def toggle_record(hold_time):
            nonlocal should_record
            should_record = not should_record

        # Set up button listener
        button = ButtonTimer(17)
        button.add_callback(toggle_record)

        # Set up camera
        cam = picamera.PiCamera(resolution=(1920, 1080), framerate=30)

        # Get the current date and time to use for creating the log directory and file
        current_date = str(datetime.datetime.now()).split(' ')

        # Remove the decimals from the seconds in the current time
        current_date[1] = current_date[1].split('.')[0]

        # Replace the ':' with '-' in the current time to make it a valid directory name
        current_date[1] = current_date[1].replace(':', '-')

        # Ensure the log directory exists
        log_dir = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(log_dir, '../logs/video/{}'.format(current_date[0]))

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Define Filename generating function
        def CreateFilename(file_number):
            file_name = '{:03d}.h264'.format(file_number)
            return os.path.join(log_dir, file_name)

        record_number = 0
        led.off()

        # Video creation loop
        while True:
            if should_record:
                if not cam.recording:
                    led.on()
                    cam.start_recording(CreateFilename(record_number))
                else:
                    cam.split_recording(CreateFilename(record_number))

                cam.wait_recording(10)
                record_number += 1
            else:
                if cam.recording:
                    cam.stop_recording()
                    led.off()

                time.sleep(1)
    except Exception:
        led.blink(on_time=0.5, off_time=0.5)
