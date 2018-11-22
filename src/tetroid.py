# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import cPickle
from game import *

def main():

    args = readCommand( sys.argv[1:] ) # Set game options for agent based on input
    agent = args['agent']
    exportFile = args['exportFile']
    train = args['train']
    noTest = args['noTest']

    game = Game()

    # train agent.
    if train:
        episodesInfo = []
        agent.startEpisode()
        while agent.isInTraining():
            game.runGame(agent, inTraining=True)
            agent.recordGame()
            print agent.gamesSoFar
            if agent.shouldStopEpisode():
                agent.stopEpisode()
                averageRewards = agent.episodeRewards / agent.gamesPerEpisode
                episodesInfo.append(
                    "TESTING GAMES UP TO " + str(agent.gamesPerEpisode * agent.episodesSoFar) + "\t\t" +
                    "Average Rewards for this set of episodes: " + str(averageRewards))
                agent.startEpisode()

        for episodeInfo in episodesInfo:
            print episodeInfo

        if exportFile:
            writeToFile(exportFile, agent.q_values)


    # test agent
    if not noTest:
        while True:
            game.runGame(agent)
            game.showTextScreen("Game Over")



def writeToFile(fileName, d):
    filePath = "../values/" + fileName + ".pickle"
    with open(filePath, "wb") as f:
        cPickle.dump(d, f)


def readDictFile(fileName):
    filePath = "../values/" + fileName + ".pickle"
    with open(filePath, "rb") as f:
        d = cPickle.load(f)
    return d


def parseAgentArgs(str):
    if str == None: return {}
    pieces = str.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts


def readCommand(argv):
    from optparse import OptionParser

    # THIS USAGE STRING IS STILL IN PROGRESS AND SHOULD BE DISREGARDED UNTIL COMPLETION
    usageStr = """
    USAGE:      python tetris.py <options>
    EXAMPLES:   (1) python tetroid.py
                    - use the Random Agent
                (2) python tetroid.py --agent QLearningAgent --agentArgs numTraining=5
                OR python tetroid.py -a QLearningAgent -g numTraining=5
                    - begins training tetroid agent with 5 sets of training episodes
    """

    parser = OptionParser(usageStr)

    parser.add_option('-a', '--agent', dest='agent',
                      help='the agent TYPE to use', default='RandomAgent')
    parser.add_option('-g','--agentArgs',dest='agentArgs',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-x', '--export', dest='exportFile',
                      help='Export Learned q-values/weights to ../values/FILENAME for future testing. Do not include filename extension',
                      metavar='FILENAME')
    parser.add_option('-l', '--load', dest='dictFile',
                      help='Read in a dictionary from ../values/FILENAME. Do not include filename extension',
                      metavar='FILENAME')
    parser.add_option('-n', '--no-test', dest='noTest',
                      action='store_true', default=False,
                      help='DO NOT run testing for agent')
    parser.add_option('-t', '--train', dest='train',
                      action='store_true', default=False,
                      help='Train agent from scratch or using loaded values')

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    agentOpts = parseAgentArgs(options.agentArgs)
    tetroidType = loadAgent(options.agent)

    if options.dictFile:
        values = readDictFile(options.dictFile)
        tetroid = tetroidType(values=values, **agentOpts)
    else:
        tetroid = tetroidType(**agentOpts)

    args = dict()
    args['agent'] = tetroid
    args['exportFile'] = options.exportFile
    args['noTest'] = options.noTest
    args['train'] = options.train
    return args


def loadAgent(tetroid):
    module = __import__("agents")
    return getattr(module, tetroid)


if __name__ == '__main__':
    main()
