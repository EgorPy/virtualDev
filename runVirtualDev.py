import keyboard
import time
import os
import win32com.client

path = os.path.expanduser("~")
print(path)
path = path.replace("\\", "/")
path = path.lower()
print(path)

time.sleep(2)

for i in range(1):
    keyboard.press_and_release("windows")
    time.sleep(1)

    for j in "cmd\n":
        keyboard.press_and_release(str(j))
        time.sleep(0.3)

    for j in f"cd {path}/desktop/virtualdev\n":
        if j == ":":
            keyboard.press_and_release("shift+;")
        else:
            keyboard.press_and_release(str(j))
        time.sleep(0.01)

    for j in "python main.py\n":
        keyboard.press_and_release(str(j))
        time.sleep(0.01)
