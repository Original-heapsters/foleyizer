import numpy
import matplotlib.pyplot as plt
import pylab
from scipy.io import wavfile
from scipy.fftpack import fft

class Spectogram:
    def __init__(self):
        return

    def chooseWav(self, pathToWav=None):
        if pathToWav is not None and pathToWav != '':
            return pathToWav
        else:
            return None

##myAudio = "wav_files/test.wav"
    def graphSetting(self, myAudio):
        if myAudio:
            samplingFreq, mySound = wavfile.read(myAudio)
            mySoundDataType = mySound.dtype
            print(mySoundDataType)
            mySound = mySound / (2.**15)
            mySoundShape = mySound.shape
            samplePoints = float(mySound.shape[0])
            print(samplePoints)
            return mySound, samplingFreq, samplePoints

    def fileDuration(self, mySound, samplingFreq, samplePoints):
        if mySound and samplingFreq:
            signalDuration = mySound.shape[0]/samplingFreq
            print(signalDuration)

    def soundChannel(self, mySound):
        if mySound:
            if len(mySound.shape) > 1:
                mySoundOneChannel = mySound[:,0]
            else:
                mySoundOneChannel = mySound


    def plotTime(self, samplePoints,samplingFreq, mySoundOneChannel):
        if samplePoints and samplingFreq and mySoundOneChannel:
            timeArray = numpy.arange(0,samplePoints,1)
            timeArray = timeArray / samplingFreq
            timeArray = timeArray * 1000
            return timeArray

    def plotTone(self, timeArray, mySoundOneChannel):
        if timeArray and mySoundOneChannel:
            #Plot the tone
            plt.plot(timeArray, mySoundOneChannel, color='G')
            plt.xlabel('Time (ms)')
            plt.ylabel('Amplitude')
            plt.savefig('plot.png', dpi=100)
            plt.show()



    def freqCont(self, mySound, mySoundOneChannel):
       if mySound and mySoundOneChannel:
            mySoundLength = len(mySound)
            fftArray = fft(mySoundOneChannel)
            numUniquePoints = numpy.ceil((mySoundLength + 1) / 2.0)
            fftArray = fftArray[0:numUniquePoints]
            fftArray = abs(fftArray)
            fftArray = fftArray / float(mySoundLength)
            fftArray = fftArray **2
            if mySoundLength % 2 > 0: #we've got odd number of points in fft
                fftArray[1:len(fftArray)] = fftArray[1:len(fftArray)] * 2

            else: #We've got even number of points in fft
                fftArray[1:len(fftArray) -1] = fftArray[1:len(fftArray) -1] * 2

            freqArray = numpy.arange(0, numUniquePoints, 1.0) * (samplingFreq / mySoundLength);
            return freqArray

    def plotFreq(self, fftArray, freqArray):
        if fftArray and freqArray:
            #Plot the frequency
            plt.plot(freqArray/1000, 10 * numpy.log10 (fftArray), color='B')
            plt.xlabel('Frequency (Khz)')
            plt.ylabel('Power (dB)')
            lt.show()

    def freqAr(self, freqArray):
        if freqArray:
            #Get List of element in frequency array
            #print freqArray.dtype.type
            freqArrayLength = len(freqArray)
            print ("freqArrayLength =", freqArrayLength)
            numpy.savetxt("freqData.txt", freqArray, fmt='%6.2f')

            #Print FFtarray information
            print ("fftArray length =", len(fftArray))
            numpy.savetxt("fftData.txt", fftArray)



if __name__ == '__main__':
    pathToWav = './wav_files/test.wav'
    path = Spectogram()
    wav = path.chooseWav(pathToWav)
    sound, graph, points = path.graphSetting(wav)
    mySound, samplingFreq, samplePoints = path.fileDuration(sound, graph, points)



    print('Big booty hoes')
