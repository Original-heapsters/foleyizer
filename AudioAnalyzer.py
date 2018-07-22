import random
from player import Player

class AudioAnalyzer:
    def __init__(self, play=None):
        self.play = Player()
        return

    def findDeadAreas(self):
        dummyJson = {
        'path':'./wav_files/africa-toto.wav',
        'title':'africa-toto.wav',
        'length': 240.0,
        'sections':[
        {
        'isDead':False,
        'start':0.0,
        'end':10.2
        },
        {
        'isDead':True,
        'start':10.2,
        'end':20.3
        },
        {
        'isDead':False,
        'start':20.3,
        'end':40.2
        },
        {
        'isDead':True,
        'start':40.2,
        'end':90.2
        },
        {
        'isDead':False,
        'start':90.2,
        'end':100.9
        },
        {
        'isDead':True,
        'start':100.9,
        'end':101.0
        },
        {
        'isDead':False,
        'start':101.0,
        'end':102.5
        },
        {
        'isDead':True,
        'start':102.5,
        'end':150.0
        },
        {
        'isDead':True,
        'start':150.0,
        'end':240.0
        }
        ]
        }
        finalMix = dummyJson['path']
        for k,v in dummyJson.items():
            if k == 'sections':
                for section in dummyJson[k]:
                    # print('The audio is dead: ' + str(section['isDead']) + ' starts at: ' + str(section['start']) + ' ends at: ' + str(section['end']))
                    duration = int(round(section['end'] - section['start']))
                    # print('Duration is ' + str(duration))
                    fillerChosen, iterations = self.findFittingFiller(desiredDuration=duration)

                    print('Decided to play ' + fillerChosen + ' x' + str(iterations) + ' To fill ' + str(duration) + ' starting at ' + str(section['start']))
                    finalMix = self.play.combineAudioFiles(src=finalMix, filler=fillerChosen, offset=section['start'])
        self.play.playWav(pathToWav=finalMix)


    def findFittingFiller(self, desiredDuration=0):

        pathToFillers = './wav_files/filler/'
        fillers = self.play.getListOfFillers(pathToFillerDir=pathToFillers)
        selectedFile = None
        for fi in fillers:
            print('.')
            if desiredDuration > 0 and self.getLengthOfAudio(pathToAudio=fi) % desiredDuration == 0:
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
