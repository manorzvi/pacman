from layout import getLayout
from pacman import *
from submission import *
from ghostAgents import *
from textDisplay import *

players = [OriginalReflexAgent, ReflexAgent, MinimaxAgent, AlphaBetaAgent, RandomExpectimaxAgent]
depths = [2, 3, 4]
layouts = ['capsuleClassic', 'contestClassic', 'mediumClassic',
           'minimaxClassic', 'openClassic', 'originalClassic',
           'smallClassic', 'testClassic', 'trappedClassic', 'trickyClassic']
ghosts = [RandomGhost(1), RandomGhost(2)]


def run_game(player, layout_name, file_ptr, depth=1):
    layout = getLayout(layout_name)
    if depth > 1:
        player.depth = depth

    games = runGames(layout, player, ghosts, NullGraphics(), 7, False, 0, False, 30)
    scores = [game.state.getScore() for game in games]
    times = [game.my_avg_time for game in games]
    avg_score = sum(scores) / float(len(scores))
    avg_time = sum(times) / float(len(times))
    line = (player.__class__.__name__ + ',' +
            str(depth) + ',' +
            layout_name + ',' +
            '%.2f' % avg_score + ',' +
            '%.2f' % (avg_time * 1e6) + 'E-06\n')
    file_ptr.write(line)
    return


if __name__ == '__main__':
    base = time.time()
    i = 0
    for layout in layouts:
        with open('results_' + layout + '.csv', 'w+') as file_ptr:
            for player in players:
                if player in [OriginalReflexAgent, ReflexAgent]:
                    i += 1
                    print('[Experiment ' + str(i) + '] - python pacman.py -l ' + str(layout) + ' -p ' + str(player) + ' -n 7 -q')
                    run_game(player(), layout, file_ptr)
                else:
                    for d in depths:
                        i += 1
                        print('[Experiment ' + str(i) + '] - python pacman.py -l ' + str(layout) + ' -p ' + str(player) + '-a depth=' + str(d) + ' -n 7 -q')
                        run_game(player(), layout, file_ptr, d)

            file_ptr.write('\n')
    file_ptr.close()
    print('experiments time: ' + str((time.time() - base)/60) + ' min')
