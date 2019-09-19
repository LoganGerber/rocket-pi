import os
from signal import pause

from utils.button_timer import ButtonTimer

def shutdown(hold_time: float) -> None:
    if hold_time >= 3:
        os.system('sudo shutdown now')

if __name__ == '__main__':
    listener = ButtonTimer(17, 3)
    listener.add_callback(shutdown)

    pause()
