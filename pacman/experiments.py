import subprocess
import csv

if __name__ == '__main__':
    players = ["ReflexAgent", "MinimaxAgent", "AlphaBetaAgent", "RandomExpectimaxAgent"]
    layouts = ["capsuleClassic", "contestClassic", "mediumClassic", "minimaxClassic", "openClassic", "originalClassic",
               "smallClassic", "testClassic", "trappedClassic", "trickyClassic"]
    #depths = [2,3,4]
    depths = [2, 3]

    #experiments = pd.DataFrame(columns=['Name', 'Depth Limit', 'Layout', 'Average Score', 'Average Time'])
    experiments = list()
    i = 0
    for layout in layouts:

        for player in players:

            if not player == 'ReflexAgent':
                for depth in depths:
                    command  = 'python pacman.py -l ' + layout + ' -q -k 2 ' + '-n 7 -p ' + player + ' -a depth=' + str(depth)
                    res      = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
                    avgScore = float([c for c in res.replace('\n', ' ').replace('\r', ' ').split("  ") if "Average Score: " in c][0].split()[2])
                    times    = [float(c.split()[2]) for c in res.replace('\n', ' ').replace('\r', ' ').split("  ") if "Step Time: " in c]
                    avgTime  = sum(times) / float(len(times))
                    experiment = [player, depth, layout, avgScore, avgTime]
                    experiments.append(experiment)
                    i += 1
                    print('[INFO] - finished exp No.' + str(i) + ": " + command)


            else:
                command  = 'python pacman.py -l ' + layout + ' -q -k 2 ' + '-n 7 -p ' + player
                res      = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
                avgScore = float([c for c in res.replace('\n', ' ').replace('\r', ' ').split("  ") if "Average Score: " in c][0].split()[2])
                times    = [float(c.split()[2]) for c in res.replace('\n', ' ').replace('\r', ' ').split("  ") if "Step Time: " in c]
                avgTime  = sum(times) / float(len(times))
                experiment = [player, 1, layout, avgScore, avgTime]
                experiments.append(experiment)
                i += 1
                print('[INFO] - finished exp No.' + str(i) + ": " + command)

    with open('experiments.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(experiments)

    f.close()
