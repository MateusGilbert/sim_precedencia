#! /usr/bin/python3

from numpy import linspace, sin, zeros, concatenate as concat, multiply, pi, \
array
import sounddevice as sd
import librosa

def reverse_channels(sound):
	aux = sound.copy()
	aux.reverse()
	return aux

def play_audio(sound, framerate, reverse=False):
	if isinstance(sound, list):
		l_out, r_out = reverse_channels(sound) if reverse else sound
	output = array([list(i) for i in zip(l_out,r_out)])
	sd.play(output, framerate, mapping=[1,2])

def gen_audio(freq, intensity, delay, framerate=44100, T=2, fromfile=None,ret_im=False):
	if fromfile:
		l_data,_ = librosa.load(fromfile, sr=framerate)
		r_data = l_data.copy()
	else:
		t = linspace(0,T, int(framerate*T), endpoint=False)
		if isinstance(freq, int):
			freq = (freq,freq)
		l_data = sin(2*pi*freq[0]*t)
		r_data = sin(2*pi*freq[1]*t)
	if ret_im:
		return [l_data, r_data]
	data_left = intensity[0]*l_data
	data_right = intensity[1]*r_data
	l_delay, r_delay = delay
	d_time = abs(l_delay - r_delay)
	delay_vect = zeros(int(framerate*d_time))
	if l_delay > r_delay:
		data_left = concat((delay_vect, data_left))
		data_right = concat((data_right, delay_vect))
	elif l_delay < r_delay:
		data_right = concat((delay_vect, data_right))
		data_left = concat((data_left, delay_vect))
	if d_time != max(l_delay,r_delay):
		delay_vect = zeros(int(framerate*min(l_delay,r_delay)))
		data_right = concat((delay_vect, data_right))
		data_left = concat((delay_vect, data_left))
	return [data_left, data_right]

def sim_mov(sound, left2right=True):
	wrapping = linspace(0,1,len(sound[0]),endpoint=False)
	if left2right:
		data_left = multiply(wrapping[::-1],sound[0])
		data_right = multiply(wrapping,sound[1])
	else:
		data_left = multiply(wrapping,sound[0])
		data_right = multiply(wrapping[::-1],sound[1])
	return [data_left, data_right]

def sim_app(sound, approach=True):
	wrapping = linspace(0,1,len(sound[0]),endpoint=False)
	if approach:
		data_left = multiply(wrapping,sound[0])
		data_right = multiply(wrapping,sound[1])
	else:
		data_left = multiply(wrapping[::-1],sound[0])
		data_right = multiply(wrapping[::-1],sound[1])
	return [data_left, data_right]

if __name__ == '__main__':
	framerate = 44100
	audio = gen_audio(None, None, None, fromfile='footsteps.wav', ret_im=True)
	audio = sim_mov(audio)
	play_audio(audio, framerate)
	input()
	audio = gen_audio(440, (1.,1.), (0,0))
	play_audio(audio, framerate)
	input()
