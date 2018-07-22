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
            print(samplingFreq)
            mySoundDataType = mySound.dtype
            print(mySoundDataType)
            mySound = mySound / (2.**15)
            mySoundShape = mySound.shape
            samplePoints = float(mySound.shape[0])
            print(samplePoints)
            print(samplingFreq)
            return mySound, samplingFreq, samplePoints

    def fileDuration(self, mySound, samplingFreq):

        if mySound.any():
            print(mySound.shape[0])
            signalDuration = float(mySound.shape[0])/samplingFreq
            print('Signal Duration')
            print(signalDuration)
            return signalDuration

    def soundChannel(self, mySound):
        if mySound.any():
            if len(mySound.shape) > 1:
                mySoundOneChannel = mySound[:,0]
                return mySoundOneChannel
            else:
                mySoundOneChannel = mySound
                return mySoundOneChannel


    def plotTime(self, samplePoints,samplingFreq, mySoundOneChannel):
        if samplePoints and samplingFreq and mySoundOneChannel.any():
            timeArray = numpy.arange(0,samplePoints,1)
            timeArray = timeArray / samplingFreq
            timeArray = timeArray * 1000
            return timeArray

    def plotTone(self, timeArray, mySoundOneChannel):
        if timeArray.any() and mySoundOneChannel.any():
            #Plot the tone
            plt.plot(timeArray, mySoundOneChannel, color='G')
            plt.xlabel('Time (ms)')
            plt.ylabel('Amplitude')
            plt.savefig('plot.png', dpi=100)
            plt.show()





if __name__ == '__main__':
    pathToWav = './wav_files/test.wav'
    path = Spectogram()
    wav = path.chooseWav(pathToWav)
    sound, graph, points = path.graphSetting(wav)
    dura = path.fileDuration(sound, graph)
    chan = path.soundChannel(sound)
    plotTime = path.plotTime(points,graph, chan)
    tone= path.plotTone(plotTime, chan)


