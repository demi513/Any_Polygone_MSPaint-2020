

#Credits to Daniel Liu for doing the math


import pyautogui
import math
import tkinter as tk 
from pynput.mouse import Button, Controller

mouse = Controller()

def ask():
	global close
	def do():
		global close
		win.destroy()
		close = True
	def grab():
		global area, num_sides
		fine = True
		try:
			area = int(entry_area.get())
			if area < 1:
				entry_area.delete(0,tk.END)
				entry_area.insert(1,'Invalid')
				fine = False
		except:
			entry_area.delete(0,tk.END)
			entry_area.insert(1,'Invalid')
			fine = False
		try:
			num_sides = int(entry_num_sides.get())
			if num_sides < 3:
				fine = False
				entry_num_sides.delete(0,tk.END)
				entry_num_sides.insert(1,'Invalid')

		except:
			entry_num_sides.delete(0,tk.END)
			entry_num_sides.insert(1,'Invalid')
			fine = False
		if fine:
			win.destroy()

	close = False
	win = tk.Tk()
	win.title('Useless')
	win.protocol('WM_DELETE_WINDOW', do)

	win.rowconfigure([i for i in range(1)], weight=1)
	win.columnconfigure([i for i in range(2)],weight=1)
	
	frm_enter = tk.Frame(master=win)
	frm_enter.grid(row=0, column=0)
	frm_enter.rowconfigure([i for i in range(2)],weight=1)
	frm_enter.columnconfigure([i for i in range(2)],weight=1)

	lbl_area = tk.Label(master=frm_enter, text='Area')
	lbl_area.grid(row=0, column=0, sticky='nsew')

	entry_area = tk.Entry(master=frm_enter, width=20)
	entry_area.grid(row=0, column=1, sticky='nsew')

	lbl_num_sides = tk.Label(master=frm_enter, text='Number of sides')
	lbl_num_sides.grid(row=1, column=0, sticky='nsew')

	entry_num_sides = tk.Entry(master=frm_enter, width=20)
	entry_num_sides.grid(row=1, column=1, sticky='nsew')

	btn_start = tk.Button(master=win, text='Start drawing!', command=grab)
	btn_start.grid(row=0, column=1, sticky='nsew')

	while True:
		try:
			win.update_idletasks()
			win.update()
		except:
			break
	try:
		up = (4 * area)
		angle = 90 - (180 /num_sides)
		apot = math.tan(math.radians(angle))
		side = math.sqrt(up/num_sides / apot)
		return area, num_sides, side, apot
	except:
		pass
def inside_angle(num_sides):
	return 360/num_sides

def get_pos(ask_ret, mouse_pos):
	if close:
		exit()
	list_pos = []
	area, num_sides, side, apot = ask_ret
	apot = apot * side/2
	x,y = mouse_pos
	#x,y = (0,0)
	angle = inside_angle(num_sides)
	distance = math.sqrt((apot**2) + (side/2)**2)
	pos = angle/2
	while True:
		pos += angle
		if pos >= 90:
			break
	phet = abs(pos - 90)
	changex = math.cos(math.radians(phet)) * distance
	changey = math.sin(math.radians(phet)) * distance
	newx = x + changex
	newy = y - changey
	list_pos.append((newx, newy))
	for i in range(num_sides-1):
		phet = phet + angle
		remove = phet
		if phet >= 270:
			remove = 360 - remove
		elif phet >= 90:
			remove = 180 - remove

		remove = abs(remove)
		changex = math.cos(math.radians(remove)) * distance
		changey = math.sin(math.radians(remove)) * distance
		if phet >= 270:
			newx = x + changex
			newy = y + changey

		elif phet >= 180:
			newx = x - changex
			newy = y + changey		

		elif phet >= 90:
			newx = x - changex
			newy = y - changey		

		elif phet >= 0:
			newx = x + changex
			newy = y - changey	

		list_pos.append((newx, newy))
	return list_pos


while True:
	list_pos = get_pos(ask(), pyautogui.position())
	x1,y1 = list_pos.pop(0)
	list_pos.insert(0,(x1, y1))
	pyautogui.moveTo(x1,y1,1)
	list_pos.append((x1, y1))
	for i in list_pos:
		x, y = i
		pyautogui.mouseDown(x,y)

