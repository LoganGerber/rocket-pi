import sys
import datetime
import multiprocessing as mp

import picamera
from gpiozero import LED, Button

def RecordVideo(stop_event):
    led = LED(26)
    try:
        button = Button(17, hold_time=0.25, bounce_time=0.01)

        # Set up camera
        cam = picamera.PiCamera(resolution=(1920,1080), framerate=30)

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

        should_record = False
        button_held = False

        record_number = 0
        led.on()
        # Video creation loop
        while not stop_event.is_set():
            if should_record:
                led.on()
                camera.start_recording(CreateFilename(recording_file_path, record_number))
                camera.wait_recording(10)
                record_number += 1
            else:
                led.off()
                button.wait_for_press(1)

            if button.is_pressed and not button_held:
                should_record = not should_record
                button_held = True
            elif not button.is_pressed and button_held:
                button_held = False

        camera.stop_recording()

    except:
        led.blink(on_time=0.5, off_time=0.5)

        stop_event.wait()

def DoNothing(signal, frame):
    pass

if __name__ == '__main__':
    stop_token = mp.Event()

    record_process = mp.Process(target=RecordVideo, args=(stop_token,), name='Record video')
    record_process.start()

    signal.signal(signal.SIGTERM, DoNothing)
    signal.signal(signal.SIGHUP, DoNothing)

    signal.pause()

    stop_token.set()
    record_process.join(11)

