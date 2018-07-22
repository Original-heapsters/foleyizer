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
            return myAudio == pathToWav
        else:
            return None

##myAudio = "wav_files/test.wav"
    def graphSetting(self, myAudio):
        if myAudio:
            samplingFreq, mySound = wavfile.read(myAudio)
            mySoundDataType = mySound.dtype
            mySoundDataType = mySound.dtype
            print(mySoundDataType)
            mySound = mySound / (2.**15)
            mySoundShape = mySound.shape
            samplePoints = float(mySound.shape[0])
            return mySound, samplePoints

    def fileDuration(self, mySound, samplingFreq):
        if mySound and samplingFreq:
            signalDuration = mySound.shape[0]/samplingFreq

    def soundChannel(self, mySound):
        if mySound:
            if len(mySound.shape) > 1:
                mySoundOneChannel = mySound[:,0]
            else:
                mySoundOneChannel = mySound



#Read file and get sampling freq [ usually 44100 Hz ]  and sound object
##samplingFreq, mySound = wavfile.read(myAudio)

#Check if wave file is 16bit or 32 bit. 24bit is not supported
##mySoundDataType = mySound.dtype
##print(mySoundDataType)

#We can convert our sound array to floating point values ranging from -1 to 1 as follows

#mySound = mySound / (2.**15)

#Check sample points and sound channel for duel channel(5060, 2) or  (5060, ) for mono channel

##mySoundShape = mySound.shape
##samplePoints = float(mySound.shape[0])

#Get duration of sound file
##signalDuration =  mySound.shape[0] / samplingFreq

#If two channels, then select only one channel
##mySoundOneChannel = mySound[:,0]
##print(mySound.shape)
##if len(mySound.shape) > 1:
##    mySoundOneChannel = mySound[:,0]
##else:
##    mySoundOneChannel = mySound


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




#Plotting the tone

# We can represent sound by plotting the pressure values against time axis.
#Create an array of sample point in one dimension
##timeArray = numpy.arange(0, samplePoints, 1)

##timeArray = timeArray / samplingFreq

#Scale to milliSeconds
##timeArray = timeArray * 1000

#Plot the tone
##plt.plot(timeArray, mySoundOneChannel, color='G')
##plt.xlabel('Time (ms)')
##plt.ylabel('Amplitude')
##plt.savefig('plot.png', dpi=100)
##plt.show()

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

#Plot frequency content
#We can get frquency from amplitude and time using FFT , Fast Fourier Transform algorithm

#Get length of mySound object array
##mySoundLength = len(mySound)

#Take the Fourier transformation on given sample point
#fftArray = fft(mySound)
##fftArray = fft(mySoundOneChannel)

##numUniquePoints = numpy.ceil((mySoundLength + 1) / 2.0)
##fftArray = fftArray[0:numUniquePoints]

#FFT contains both magnitude and phase and given in complex numbers in real + imaginary parts (a + ib) format.
#By taking absolute value , we get only real part

##fftArray = abs(fftArray)

#Scale the fft array by length of sample points so that magnitude does not depend on
#the length of the signal or on its sampling frequency

##fftArray = fftArray / float(mySoundLength)

#FFT has both positive and negative information. Square to get positive only
##fftArray = fftArray **2

#Multiply by two (research why?)
#Odd NFFT excludes Nyquist point
##if mySoundLength % 2 > 0: #we've got odd number of points in fft
##    fftArray[1:len(fftArray)] = fftArray[1:len(fftArray)] * 2

##else: #We've got even number of points in fft
##    fftArray[1:len(fftArray) -1] = fftArray[1:len(fftArray) -1] * 2

##freqArray = numpy.arange(0, numUniquePoints, 1.0) * (samplingFreq / mySoundLength);

#Plot the frequency
##plt.plot(freqArray/1000, 10 * numpy.log10 (fftArray), color='B')
##plt.xlabel('Frequency (Khz)')
##plt.ylabel('Power (dB)')
##plt.show()

#Get List of element in frequency array
#print freqArray.dtype.type
##freqArrayLength = len(freqArray)
##print ("freqArrayLength =", freqArrayLength)
##numpy.savetxt("freqData.txt", freqArray, fmt='%6.2f')

#Print FFtarray information
##print ("fftArray length =", len(fftArray))
##numpy.savetxt("fftData.txt", fftArray)


if __name__ == '__main__':
    print('Big booty hoes')
