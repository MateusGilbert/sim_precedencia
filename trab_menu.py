#! /usr/bin/python3

import tkinter as tk
from tkinter import filedialog as fd
from func import play_audio, gen_audio, sim_mov, sim_app
from PIL import Image as im, ImageTk as im_tk

def click():
	l_int = float(entries['left_int'].get())
	r_int = float(entries['right_int'].get())
	l_dly = float(entries['left_delay'].get())*1e-3
	r_dly = float(entries['right_delay'].get())*1e-3
	if bool_wav.get():
		filename = entries['wav'].get()
		if not filename:
			return
		audio = gen_audio(None,(l_int,r_int),(l_dly,r_dly),fromfile=filename)
	else:
		freq = int(entries['freq'].get()) if not bool_freq.get() else (int(entries['l_freq'].get()),int(entries['r_freq'].get()))
		audio = gen_audio(freq,(l_int,r_int),(l_dly,r_dly))
	if booleans['mov']:
		if booleans['mov_lat'].get():
			if booleans['mov_left'].get():
				audio = sim_mov(audio)
			else:
				audio = sim_mov(audio,left2right=False)
		if booleans['mov_vert'].get():
			if booleans['mov_back'].get():
				audio = sim_app(audio)
			else:
				audio = sim_app(audio,approach=False)
	play_audio(audio, 44100, reverse=False)

def enable_freq():
	if bool_wav.get():
		return
	if bool_freq.get():
		if 'l_freq' in entries.keys():
			entries['l_freq'].config(state='normal')
			entries['r_freq'].config(state='normal')
			entries['freq'].config(state='disable')
		else:
			l_left_freq = tk.Label(win, text='Freq.').grid(row=5, column=1)
			l_left_hz = tk.Label(win, text='Hz').grid(row=5, column=3)
			l_right_freq = tk.Label(win, text='Freq.').grid(row=5, column=6)
			l_right_hz = tk.Label(win, text='Hz').grid(row=5, column=8)
			e_left_hz = tk.Entry(win, width=4)
			e_left_hz.grid(row=5,column=2)
			e_left_hz.insert(0, '440')
			e_right_hz = tk.Entry(win, width=4)
			e_right_hz.grid(row=5,column=7)
			e_right_hz.insert(0, '440')
			entries['l_freq'] = e_left_hz
			entries['r_freq'] = e_right_hz
			entries['freq'].config(state='disabled')
	else:
		entries['l_freq'].config(state='disabled')
		entries['r_freq'].config(state='disabled')
		entries['freq'].config(state='normal')

def get_wav():
	op = booleans['wav'].get()
	if op:
		entries['wav'].config(state='normal')
		buttons['ch_file'].config(state='normal')
		entries['freq'].config(state='disabled')
		if 'l_freq' in entries.keys():
			entries['l_freq'].config(state='disabled')
			entries['r_freq'].config(state='disabled')
	else:
		entries['wav'].config(state='disabled')
		buttons['ch_file'].config(state='disabled')
		if not booleans['freq'].get():
			entries['freq'].config(state='normal')
		else:
			entries['l_freq'].config(state='normal')
			entries['r_freq'].config(state='normal')

def get_file():
	filename = fd.askopenfilename()
	print(filename)
	entries['wav'].insert(0,filename)

def sec_win_close():
	booleans['mov'] = False
	new_win.quit()
	new_win.destroy()

def mov_sim():
	global new_win
	booleans['mov'] = True
	new_win = tk.Toplevel()
	title = 'Simulação de Movimento'
	new_win.title(title)
	#checks
	chk_lat = tk.Checkbutton(new_win, text='Mov. Lateral', var=booleans['mov_lat'])
	chk_lat.grid(row=0, column=0)
	chk_vert = tk.Checkbutton(new_win, text='Mov. Aprox./Afast.', var=booleans['mov_vert'])
	chk_vert.grid(row=0,column=2)
	#radio buts
	bool_left_mov = tk.Radiobutton(new_win, text='Esquerda', variable=booleans['mov_left'], value=True)
	bool_left_mov.grid(row=1, column=0)
	bool_right_mov = tk.Radiobutton(new_win, text='Direita', variable=booleans['mov_left'], value=False)
	bool_right_mov.grid(row=1, column=2)
	bool_back = tk.Radiobutton(new_win, text='Aproximar', variable=booleans['mov_back'], value=True)
	bool_back.grid(row=2, column=0)
	bool_front = tk.Radiobutton(new_win, text='Afastar', variable=booleans['mov_back'], value=False)
	bool_front.grid(row=2, column=2)
	#button
	exit = tk.Button(new_win, text='Sair', command=sec_win_close)
	exit.grid(row=4,column=0)
	new_win.mainloop()

win = tk.Tk()
title = 'Efeito de Precedência'
win.title(title)

prog_label = tk.Label(win, text=title).grid(row=0,column=1)
#labels
l_freq = tk.Label(win, text='Frequência').grid(row=1,column=0)
l_freq_bool = tk.Label(win, text='Dif. Freq.').grid(row=1, column=4)
l_freq2 = tk.Label(win, text='Hz').grid(row=1, column=2)
l_left_channel = tk.Label(win, text='Canal Esquerdo:').grid(row=2,column=0)
l_right_channel = tk.Label(win, text='Canal Direito:').grid(row=2,column=5)
l_left_int = tk.Label(win, text='Intensidade').grid(row=3,column=1)
l_right_int = tk.Label(win, text='Intensidade').grid(row=3,column=6)
l_left_delay = tk.Label(win, text='Delay').grid(row=4,column=1)
l_left_ms = tk.Label(win, text='ms').grid(row=4,column=3)
l_right_delay = tk.Label(win, text='Delay').grid(row=4,column=6)
l_right_ms = tk.Label(win, text='ms').grid(row=4,column=8)
l_wav = tk.Label(win, text='Arq. Audio:').grid(row=7,column=0)

#entries
e_freq = tk.Entry(win, width=5)
e_freq.grid(row=1,column=1)
e_freq.insert(0, '440')
e_left_int = tk.Entry(win, width=4)
e_left_int.grid(row=3,column=2)
e_left_int.insert(0, '1')
e_right_int = tk.Entry(win, width=4)
e_right_int.grid(row=3,column=7)
e_right_int.insert(0, '1')
e_left_delay = tk.Entry(win, width=4)
e_left_delay.grid(row=4,column=2)
e_left_delay.insert(0, '0')
e_right_delay = tk.Entry(win, width=4)
e_right_delay.grid(row=4,column=7)
e_right_delay.insert(0, '0')
e_wav = tk.Entry(win, width=10)
e_wav.grid(row=7, column=1)
e_wav.config(state='disabled')

#booleans
bool_freq = tk.BooleanVar()
bool_freq.set(False)
bool_wav = tk.BooleanVar()
bool_wav.set(False)
bool_mov = False
bool_lat = tk.IntVar()
bool_vert = tk.IntVar()
bool_left_mov = tk.BooleanVar()
bool_left_mov.set(True)
bool_back = tk.BooleanVar()
bool_back.set(True)

#buttons
play = tk.Button(win, text='Reproduzir', command=click)
play.grid(row=8,column=4)
same_freq = tk.Radiobutton(win, text='Sim', variable=bool_freq, value=True, command=enable_freq)
same_freq.grid(row=1,column=5)
same_freq2 = tk.Radiobutton(win, text='Não', variable=bool_freq, value=False, command=enable_freq)
same_freq2.grid(row=1,column=6)
wav1 = tk.Radiobutton(win, text='Sim', variable=bool_wav, value=True, command=get_wav)
wav1.grid(row=7,column=5)
wav2 = tk.Radiobutton(win, text='Não', variable=bool_wav, value=False, command=get_wav)
wav2.grid(row=7,column=6)
f_img = im_tk.PhotoImage(im.open('folder_icon.png').resize((20,20)))
ch_file = tk.Button(win, image=f_img, command=get_file, height=20, width=20)
ch_file.grid(row=7,column=2)
ch_file.config(state='disabled')
mov_sim = tk.Button(win, text='Simular Mov.', command=mov_sim)
mov_sim.grid(row=8,column=5)
exit = tk.Button(win,text='Sair', command=win.quit)
exit.grid(row=8,column=6)

global entries, booleans, buttons
entries = {'freq': e_freq, 'left_int': e_left_int, 'right_int': e_right_int, 'left_delay': e_left_delay, 'right_delay': e_right_delay, 'wav': e_wav}
booleans = {'freq': bool_freq, 'wav': bool_wav, 'mov': bool_mov, 'mov_lat': bool_lat, 'mov_vert': bool_vert, 'mov_left': bool_left_mov, 'mov_back': bool_back}
buttons = {'play': play, 'ch_file': ch_file}

win.mainloop()
