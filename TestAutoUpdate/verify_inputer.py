import time
import codecs
import win32gui
import subprocess
import auto_inputer


def verify_inputer(input_file, output_file):
    notepad = subprocess.Popen ([r"notepad.exe", output_file])

    time.sleep (2.0)
    print("notepad pid:", notepad.pid)
    for hwnd in auto_inputer.get_hwnds_for_pid(notepad.pid):
        print(hwnd, "=>", win32gui.GetWindowText(hwnd))
        win32gui.SetForegroundWindow(hwnd)

    f = codecs.open(input_file, 'r', 'utf-8')
    s = f.readlines()
    for line in s:
        line = line.rstrip('\n\r')
        auto_inputer.press_key(*line)

        auto_inputer.press_once('enter')
        auto_inputer.press_once('tab')
        auto_inputer.press_key(*line)
        auto_inputer.press_once('spacebar')
        auto_inputer.press_once('enter')
        time.sleep(0.09)

    auto_inputer.press_key('ctrl','s')
    auto_inputer.press_key('alt','F4')
    f.close()
