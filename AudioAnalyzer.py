import random
from player import Player

class AudioAnalyzer:
    def __init__(self, play=None):
        self.play = Player()
        return

    def findDeadAreas(self):
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
        originalAudio = dummyJson['path']
        finalMix = None
        intermediateMixes = []
        counter = 0
        for k,v in dummyJson.items():
            if k == 'sections':
                for section in dummyJson[k]:
                    if section['isDead']:
                        # print('The audio is dead: ' + str(section['isDead']) + ' starts at: ' + str(section['start']) + ' ends at: ' + str(section['end']))
                        duration = int(round(section['end'] - section['start']))
                        # print('Duration is ' + str(duration))
                        fillerChosen, iterations = self.findFittingFiller(desiredDuration=duration)

                        print('Decided to play ' + fillerChosen + ' x' + str(iterations) + ' To fill ' + str(duration) + ' starting at ' + str(section['start']))
                        intermediateMixes.append((fillerChosen,section['start']))
                        counter += 1

        finalMix = self.play.combineAudioFiles(src=originalAudio, fillersWithOffsets=intermediateMixes)
        self.play.playWav(pathToWav=finalMix)


    def findFittingFiller(self, desiredDuration=0):

        pathToFillers = './wav_files/filler/'
        fillers = self.play.getListOfFillers(pathToFillerDir=pathToFillers)
        selectedFile = None
        for fi in fillers:
            print('.')
            if desiredDuration > 0 and int(round(self.play.getWavLength(pathToWav=fi))) % desiredDuration == 0:
                print('Found it! ' + fi)
                selectedFile = fi
                break

        if not selectedFile:
            print('No Dice')
            selectedFile = random.choice(fillers)

        return selectedFile, 1

    def getLengthOfAudio(self, pathToAudio):
        return random.randint(0,10)

if __name__ == '__main__':
    analyzer = AudioAnalyzer()
    analyzer.findDeadAreas()
