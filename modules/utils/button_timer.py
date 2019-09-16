import time
import queue
from typing import Callable, Any

from gpiozero import Button

class ButtonTimer:
    def __init__(self, button_pin, timeout: float = None) -> None:
        self.timeout = timeout

        self.button_was_held = False

        self.button = Button(button_pin, hold_time=0.1, bounce_time=0.01)
        self.button.when_pressed = self._button_pressed
        self.button.when_held = self._button_held
        self.button.when_released = self._button_released

        self.time_pressed = None

        self.callbacks = []

        self.waiting_for_press = False
        self.waiting_queue = queue.Queue()

    def add_callback(self, callback: Callable[[float], Any]) -> None:
        self.callbacks.append(callback)

    def wait_for_press(self, timeout: float = None) -> float:
        while not self.waiting_queue.empty():
            self.waiting_queue.get()
        self.waiting_for_press = True
        try:
            time_pressed = self.waiting_queue.get(True, timeout)
        except queue.Empty:
            time_pressed = None
        self.waiting_for_press = False
        return time_pressed


    def _button_pressed(self) -> None:
        self.time_pressed = time.time()
        self.button_was_held = True

    def _button_held(self) -> None:
        if time.time() - self.time_pressed >= self.timeout:
            self._button_released()

    def _button_released(self) -> None:
        if self.button_was_held:
            time_held = time.time() - self.time_pressed

            for callback in self.callbacks:
                callback(time_held)
            if self.waiting_for_press:
                self.waiting_queue.put(time_held)

            self.button_was_held = False
