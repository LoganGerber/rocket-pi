from gpiozero import Button
from multiprocessing import Process, Event, Queue
from signal import pause

import time
import os

def track_time(event, queue):
    start = time.time()
    event.wait(3)
    event.clear()
    end = time.time()
    queue.put(end - start)

def handle_button_press(queue):
    while True:
        time_held = queue.get()
        if time_held >= 3:
            os.system('sudo shutdown now')

event = Event()
queue = Queue()

button = Button(17, hold_time=0.25, bounce_time=0.01)

was_held = False
def held():
    global was_held
    was_held = True
    p = Process(target=track_time, args=(event, queue), name='track_shutdown_press_time', daemon=True)
    p.start()

def released():
    global event
    global was_held
    if was_held:
        event.set()
        event.clear()
    was_held = False

button.when_held = held
button.when_released = released

handler = Process(target=handle_button_press, args=(queue,), name='handle_shutdown_press', daemon=True)
handler.start()

pause()

