import pandas as pd
import os
from pprint import pprint
import matplotlib.pyplot as plt

def mergeCsv():
    results = '..\\results\\'
    layoutRes = []

    for filename in os.listdir(results):

        layoutRes.append(results + filename)

    with open('Dump.csv', 'w') as DumpFile:
        for f in layoutRes:

            with open(f, 'r') as layoutFile:
                for line in layoutFile:

                    DumpFile.write(line)

    try:
        os.remove('experiments.csv')
    except OSError:
        pass

    with open('experiments.csv', 'w') as endFile, open('Dump.csv', 'r') as DumpFile:
        for line in DumpFile:
            if not line.strip(): continue  # skip the empty line
            endFile.write(line)  # non-empty line. Write it to output

    os.remove('Dump.csv')

def plot_score_depth():

    experiments_pd = pd.read_csv('experiments.csv', header=None)

    agents = experiments_pd[0].unique()

    agents_depths_values = dict()

    for agent in agents:
        agent_pd = experiments_pd.loc[experiments_pd[0] == agent]
        #print(agent_pd)

        depths = agent_pd[1].unique()
        agents_depths_values[agent] = list()
        for depth in depths:
            agent_depth_pd = agent_pd.loc[agent_pd[1] == depth]
            #print(agent_depth_pd)
            agents_depths_values[agent].append((depth, agent_depth_pd[3].mean()))

    pprint(agents_depths_values)
    try:
        os.remove('agent_depth_scores_table.csv')
    except OSError:
        pass

    with open('agent_depth_scores_table.csv', 'w') as tableFile:
        headers = 'name, 1, '
        for d in depths: headers += str(d) + ', '
        headers = headers[:-2] + '\n'
        tableFile.write(headers)

        for agent, values in agents_depths_values.items():
            row = agent + ', '
            if len(values) > 1:
                row = row + ', '
            for v in values: row += str(v[1]) + ', '
            row = row[:-2] + '\n'

            tableFile.write(row)


    for agent, values in agents_depths_values.items():
        depths = [v[0] for v in values]
        scores = [v[1] for v in values]
        if len(depths)>1:
            plt.plot(depths, scores, label=agent)
        else:
            plt.plot(depths, scores, 'o', label=agent)

    plt.legend()
    plt.xlabel('depth')
    plt.ylabel('score')
    plt.title("Each Agent Score as Function of it's Algo Depth")
    plt.savefig('agents_depth_scores')
    plt.show()













if __name__ == '__main__':
    mergeCsv()
    plot_score_depth()




