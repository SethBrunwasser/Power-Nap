import time
import win32gui
import win32con
import ctypes


# Works with Windows
def turnoff():
	# Shuts off display
	SC_MONITORPOWER = 0xF170
	win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)

def turnon():
	# Turning on the display using:
	# win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)
	# causes the display to turn off shortly after.
	# Instead we will simulate someone moving the mouse to wake the display

	mouse_event = ctypes.windll.user32.mouse_event
	MOUSEEVENTF_MOVE = 0x0001
	mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
