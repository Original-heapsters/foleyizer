import os
import random
from .player import Player

class AudioAnalyzer:
    def __init__(self, play=None):
        self.play = Player()
        return

    def findDeadAreas(self, inputJson=None, altPath=None, outDir=None):
        dummyJson = {
        'path':'./wav_files/badness.wav',
        'title':'badness.wav',
        'length': 25.1827,
        'sections':[
        {
        'isDead':False,
        'start':0.0,
        'end':1.702
        },
        {
        'isDead':True,
        'start':1.702,
        'end':2.037
        },
        {
        'isDead':False,
        'start':2.037,
        'end':2.5
        },
        {
        'isDead':True,
        'start':2.5,
        'end':3.0
        },
        {
        'isDead':False,
        'start':3.0,
        'end':9.7
        },
        {
        'isDead':True,
        'start':9.7,
        'end':14.0
        },
        {
        'isDead':False,
        'start':14.0,
        'end':20.5
        },
        {
        'isDead':True,
        'start':20.5,
        'end':21.5
        },
        {
        'isDead':False,
        'start':21.5,
        'end':22.5
        },
        {
        'isDead':True,
        'start':22.5,
        'end':24.0
        },
        {
        'isDead':False,
        'start':24.0,
        'end':25.1827
        }
        ]
        }

        if not inputJson:
            analysisJson = dummyJson
        else:
            analysisJson = inputJson

        if not altPath:
            originalAudio = analysisJson['path']
        else:
            originalAudio = altPath
        audioCombinationCommand = 'ffmpeg -y -loglevel panic -i ' + originalAudio + ' '
        filterCommand = '-filter_complex \"'
        finalMix = None
        intermediateMixes = []
        counter = 1
        startingLetter = 'b'
        allLetters = ''
        finalMix = os.path.join(outDir, 'mixed_audio.wav')
        for k,v in analysisJson.items():
            if k == 'sections':
                for section in analysisJson[k]:
                    if section['isDead']:
                        duration = int(round(section['end'] - section['start']))
                        fillerChosen, _ = self.findFittingFiller(desiredDuration=duration)

                        audioCombinationCommand += '-i ' + fillerChosen + ' '
                        filterCommand += '[' + str(counter) + ']adelay=' + str(section['start']*1000) + '|' + str(section['start']*1000) + '[' + startingLetter + '];'
                        allLetters += '[' + startingLetter + ']'

                        counter += 1
                        startingLetter = chr(ord(startingLetter) + 1)

        filterCommand += '[0]' + allLetters + 'amix=' + str(counter) + '\" -ar 44100 ' + finalMix
        os.system(audioCombinationCommand + filterCommand)

        return finalMix, originalAudio

    def playMix(self, mixPath=None):
        self.play.playWav(pathToWav=mixPath)

    def findFittingFiller(self, desiredDuration=0):

        pathToFillers = './static/wav_files/filler/'
        fillers = self.play.getListOfFillers(pathToFillerDir=pathToFillers)
        selectedFile = None
        findRandom = True
        if not findRandom:
            for fi in fillers:
                print('.')
                if desiredDuration > 0 and int(round(self.play.getWavLength(pathToWav=fi))) % desiredDuration == 0:
                    print('Found it! ' + fi)
                    selectedFile = fi
                    break

            if not selectedFile:
                print('No Dice')
                selectedFile = random.choice(fillers)
        else:
            selectedFile = random.choice(fillers)

        return selectedFile, 1

if __name__ == '__main__':
    analyzer = AudioAnalyzer()
    finalMix = analyzer.findDeadAreas()
    analyzer.playMix(mixPath=finalMix)
