import numpy
import matplotlib.pyplot as plt
import pylab
from scipy.io import wavfile
from scipy.fftpack import fft

class Spectrogram:
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

    def plotTone(self, timeArray, amplitude, outFile='plot.png', showPlot=True, testAudio=None):
        if timeArray.any() and amplitude.any():
            #Plot the tone
            print('time array len - ' + str(len(timeArray)) + ' soundChannel len - ' + str(len(amplitude)))
            plt.plot(timeArray, amplitude, color='G')
            threshold = 0.48242188
            durationThreshold = 2000.0
            outJSON = {
            'path':testAudio
            }
            sections = []
            deadSection = False
            startTime = timeArray[0]
            newSection = {}
            print(max(amplitude))
            print(min(amplitude))
            for index in range(0,len(timeArray)):

                if index == 0:
                    # print('hit zero')
                    newSection['isDead'] = deadSection
                    newSection['start'] = timeArray[0]
                else:
                    if float(amplitude[index] * 1000000) < threshold:
                        # print(str(float(amplitude[index])) + ' was less than ' + str(threshold))
                        # print('hit violation')
                        if deadSection == False and abs(newSection['start'] - timeArray[index]) > durationThreshold:
                            # print('SWITCHED to being dead')
                            newSection['end'] = timeArray[index]
                            tmp = newSection
                            sections.append(tmp)
                            newSection = {}
                            deadSection = True
                            newSection['start'] = timeArray[index]
                            newSection['isDead'] = deadSection
                    else:
                        # print(str(float(amplitude[index])) + ' was greater than ' + str(threshold))

                        if deadSection == True and abs(newSection['start'] - timeArray[index]) > durationThreshold:
                            # print('SWITCHED to being alive')
                            newSection['end'] = timeArray[index]
                            othertmp = newSection
                            sections.append(othertmp)
                            newSection = {}
                            deadSection = False
                            newSection['start'] = timeArray[index]
                            newSection['isDead'] = deadSection
            print(len(sections))

            outJSON['sections'] = sections
            plt.xlabel('Time (ms)')
            plt.ylabel('Amplitude')
            plt.savefig(outFile, dpi=100)
            if showPlot:
                plt.show()
            return outFile, outJSON





if __name__ == '__main__':
    pathToWav = './wav_files/test.wav'
    path = Spectogram()
    wav = path.chooseWav(pathToWav)
    sound, graph, points = path.graphSetting(wav)
    dura = path.fileDuration(sound, graph)
    chan = path.soundChannel(sound)
    plotTime = path.plotTime(points,graph, chan)
    tone= path.plotTone(plotTime, chan)
