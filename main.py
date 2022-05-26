import time
import sys
import math

import ctypes
from ctypes.wintypes import BOOL, HWND, LPARAM

TARGET_WINDOW_NAME = b"Windows PowerShell"
NAME_BUFFER_LENGTH = 50


def _find_terminal():
    found = 0
    @ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    def callback(handle, arg):
        nonlocal found
        buffer = ctypes.create_string_buffer(NAME_BUFFER_LENGTH)
        ctypes.windll.user32.GetWindowTextA(handle, buffer, NAME_BUFFER_LENGTH)
        if buffer.value == TARGET_WINDOW_NAME:
            found = handle
        return 1

    ctypes.windll.user32.EnumWindows(callback, 1)
    return found


def _flash_window(hwnd: int):
    ctypes.windll.user32.FlashWindow(hwnd, True)


def _block_with_display(delay_secs: int, check_interval_secs: int = 1):
    start_time = time.time()
    end_time = start_time + delay_secs
    total_minutes = (delay_secs // 60) + 1  # So we can get how many leading zeros to display
    while True:
        current = time.time()
        secs_left = end_time - current

        mins_left, secs_leftover = divmod(secs_left, 60)

        if secs_left > 0:
            print("\b" * 100, end="")
            print(f"Remaining: {int(mins_left):0{int(math.log10(total_minutes))}}:{int(secs_leftover):02}", flush=True, end="")
        else:
            return

        time.sleep(check_interval_secs)


def timer_loop(remind_every_mins: int):
    terminal_hwnd = _find_terminal()

    remind_every_secs = remind_every_mins * 60

    while True:
        _block_with_display(remind_every_secs)
        _flash_window(terminal_hwnd)


if __name__ == "__main__":
    try:
        minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 15
        timer_loop(minutes)
    except KeyboardInterrupt:
        pass