import asyncio
import ctypes
import sys

from ytcpr.__main__ import run_ytcpr


def set_fullscreen():
    # Get the handle of the console window
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Set the window state to maximized
    ctypes.windll.user32.ShowWindow(hwnd, 3)  # 3 corresponds to SW_MAXIMIZE



if __name__ == '__main__':
    set_fullscreen()
    if __name__ == "__main__":
        email = input("Enter the Email: ")
        password = input("Enter the Password: ")
        if not email or not password:
            print(f'Email or Password is Required, Existing...!')
            sys.exit(1)
        video_id = str(input("Enter The Video ID (Optional): "))
        if not video_id:
            video_id = []
        else:
            video_id = video_id.split(',')
        asyncio.run(run_ytcpr(email, password, video_id))
