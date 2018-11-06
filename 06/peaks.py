import numpy
import sys
import wave
import struct

audioFilename = sys.argv[1]
file = wave.open(audioFilename, 'r')

sampleRate = file.getframerate() #window size
framesCount = file.getnframes()
channels = file.getnchannels()

signalArray = []
for num in range(framesCount):
	f = file.readframes(1)
	if(channels == 1): #mono
		signalArray.append(struct.unpack('<h', f)[0] * 1)
	else: #stereo
		ufArray = struct.unpack('<hh', f)
		signalArray.append((ufArray[0] + ufArray[1]) / 2)
		
windows = framesCount // sampleRate # cast to int
lowest = None
highest = None

for num in range(windows):
	low = num * sampleRate
	high = (num + 1) * sampleRate
	amplitudes = []
	
	for amp in numpy.fft.rfft(signalArray[low : high]):
		amplitudes.append(numpy.abs(amp))
	
	a = numpy.average(amplitudes)
	
	peaksIndex = []
	counter = 0
	for amp in amplitudes:
		if(amp >= 20 * a):
			peaksIndex.append(counter)
		counter  = counter + 1

	for peak in peaksIndex:
		if lowest is None or lowest > peak:
			lowest = peak
		if highest is None or highest < peak:
			highest = peak

if lowest is None or highest is None:
    print("no peaks")
else:
    print("low = " + str(lowest) + ", high = " + str(highest))