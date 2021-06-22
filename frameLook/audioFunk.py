#https://heartbeat.fritz.ai/working-with-audio-signals-in-python-6c2bd63b2daf
#import numpy as py
#import matplotlib as plt 
import librosa
#path of the audio file
print("1")
audio_data = 'test.m4a'
#This returns an audio time series as a numpy array with a default sampling rate(sr) of 22KHZ
x = librosa.load(audio_data, sr=None)
print('2')

#We can change this behavior by resampling at sr=44.1KHz.
x = librosa.load(audio_data, sr=44000)
print('3')
#%matplotlib inline


plt.figure(figsize=(14, 5))
#plotting the sampled signal
librosa.display.waveplot(x, sr=sr)