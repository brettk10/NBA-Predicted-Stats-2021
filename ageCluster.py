import numpy as np
import csv
from pandas import DataFrame
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

playerLabels = ['Rk', 'Player', 'Pos', 'Age', 'Tm',
'G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB',
'DRB','TRB','AST','STL','BLK','TOV','PF','PTS']

def load_data():
    playerDictionary = {}
    ageDictionary = {}
    for age in range(18, 45):
        ageDictionary[age] = []
    playerList = []
    for years in range(2004, 2022):
        players = []
        fileName = 'CSVStats/' + str(years) + 'Stats.csv'
        with open(fileName) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                if row[5] is not 'G' and float(row[5]) <= 20:
                    continue
                else:
                    players.append(row)
        del players[0]
        for i, row in enumerate(players):
            if(row[4] == 'TOT'):
                temp = i + 1
                length = float(len(players))
                while(temp < length and players[temp][1] == row[1]):
                    del players[temp]
                    length -= 1
            temp = row[1]
            slash = temp.find('\\')
            if row[1][slash - 1] == '*':
                row[1] = row[1][:(slash - 1)]
            else:
                row[1] = row[1][:slash]
            row[3] = int(row[3])
            for i in range(5, 30):
                if(row[i] != ''):
                    row[i] = float(row[i])
                else:
                    row[i] = 0.0
            if row[1] in playerDictionary:
                playerDictionary[row[1]].append(row)
            else:
                playerDictionary[row[1]] = []
                playerDictionary[row[1]].append(row)
            ageDictionary[row[3]].append(row)
        playerList.append(players)
    for col in playerList[0][0]:
        playerLabels.append(col)
    return playerList, playerDictionary, ageDictionary

def writeToAgeCSV(ageDictionary):
    for age in ageDictionary.keys():
        filename = 'ageClusterCSV/' + str(age) + 'Players.csv'
        with open(filename, 'w',  newline = '') as file:
            writer = csv.writer(file)
            for row in ageDictionary[age]:
                writer.writerow(row)

def clustering(dataset, first, second, third, labels, clusterNum):
    xAxis = []
    yAxis = []
    zAxis = []
    for row in dataset:
        xAxis.append(row[first])
        yAxis.append(row[second])
        zAxis.append(row[third])
    Data = {labels[first]: xAxis, labels[second]: yAxis, labels[third]: zAxis}
    df = DataFrame(Data, columns = [labels[first], labels[second], labels[third]])

    fig, ax = plt.subplots(figsize = (14,10))

    kmeans = KMeans(n_clusters = clusterNum).fit(df)
    centroids = kmeans.cluster_centers_
    indices = df.index.values
    groups = kmeans.labels_

    playerNames = [[]] * clusterNum
    for i, row in enumerate(dataset):
        temp = groups[i]
        name = row[1]
        arr = playerNames[temp].copy()
        arr.append(row[1])
        playerNames[temp] = arr


    # print(groups[6])
    '''
    def printGroups():
        print(centroids[0])
        print(playerNames[0])
    '''

    # printGroups()

    # graphItems()

    '''
    def graphItems():
        ax.scatter(df[labels[first]], df[labels[second]], c = kmeans.labels_.astype(float), s = 50, alpha = 0.5)
        ax.scatter(centroids[:, 0], centroids[:, 1], c = 'red', s = 50)
        for i, row in enumerate(dataset):
          ax.annotate(row[1], (row[first], row[second]))

        ax.set_xlabel(labels[first], color = 'black')
        ax.set_ylabel(labels[second], color = 'black')
        ax.set_title(str(labels[first]) + ' vs. ' + str(labels[second]), color = 'black')

        plt.show()
    '''
    return groups, centroids, playerNames

def writeClustersToCSV():
    for age in range(19, 38):
        filename = 'ageClusterCSV/' + str(age) + 'Players.csv'
        playerList = []
        with open(filename) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                for i in range(5, 30):
                    if(row[i] != ''):
                        row[i] = float(row[i])
                    else:
                        row[i] = 0.0
                playerList.append(row)
        _, _, playerNames = clustering(playerList, 10, 13, 20, playerLabels, 10)
        filepath = "CSVStats/ageClusters/" + str(age) + "PercentageClusters.csv"
        # First let's put all the clusters in an array
        with open(filepath, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(['Clusters'])
            for row in playerNames:
                writer.writerow(row)

def findMultiplier(stat1, stat2):
    if stat1 == 0:
        return 0
    return float(stat2 / stat1)

# Test method to determine what Giannis' 27 year old year will be after his 26 cluster
def testForPlayer(playerDictionary, player):
    playerRow = []
    currentIndex = len(playerDictionary[player]) - 1
    currPlayer = [float(playerDictionary[player][currentIndex][29]),
    float(playerDictionary[player][currentIndex][24]),
    float(playerDictionary[player][currentIndex][23])]
    currentAge = playerDictionary[player][currentIndex][3]
    filename = 'CSVStats/ageClusters/' + str(currentAge) + 'Clusters.csv'
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            if player in row:
                playerRow = row
    # print(playerRow)
    ppgMultipliers = []
    fgMultipliers = []
    tfgMultipliers = []
    for name in playerRow:
        tempStats = playerDictionary[name]
        index = 0
        for i, row in enumerate(tempStats):
            if float(row[3]) == currentAge:
                index = i
                break
        if (len(tempStats) - 1) == index:
            continue
        else:
            # print(str(tempStats[index][29]) + ' ' + str(tempStats[index + 1][29]))
            ppgMult = findMultiplier(float(tempStats[index][29]), float(tempStats[index + 1][29]))
            fgMult = findMultiplier(float(tempStats[index][24]), float(tempStats[index + 1][24]))
            tfgMult = findMultiplier(float(tempStats[index][23]), float(tempStats[index + 1][23]))
            ppgMultipliers.append(ppgMult)
            fgMultipliers.append(fgMult)
            tfgMultipliers.append(tfgMult)
    if(len(ppgMultipliers) == 0):
        return currPlayer
    ppgAverage = float(sum(ppgMultipliers) / len(ppgMultipliers))
    # print(ppgAverage)
    apgAverage = float(sum(fgMultipliers) / len(fgMultipliers))
    rbgAverage = float(sum(tfgMultipliers) / len(tfgMultipliers))

    newPlayer = [round(currPlayer[0] * ppgAverage, 1), round(currPlayer[1] * apgAverage, 1), round(currPlayer[2] * rbgAverage, 1)]

    return newPlayer

def testForPlayerPercentage(playerDictionary, player):
    playerRow = []
    currentIndex = len(playerDictionary[player]) - 1
    currPlayer = [float(playerDictionary[player][currentIndex][10]),
    float(playerDictionary[player][currentIndex][13]),
    float(playerDictionary[player][currentIndex][20])]
    currentAge = playerDictionary[player][currentIndex][3]
    filename = 'CSVStats/ageClusters/' + str(currentAge) + 'PercentageClusters.csv'
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            if player in row:
                playerRow = row
    # print(playerRow)
    FGMultipliers = []
    TFGMultipliers = []
    FTMultipliers = []
    for name in playerRow:
        tempStats = playerDictionary[name]
        index = 0
        for i, row in enumerate(tempStats):
            if float(row[3]) == currentAge:
                index = i
                break
        if (len(tempStats) - 1) == index:
            continue
        else:
            FGMult = findMultiplier(float(tempStats[index][10]), float(tempStats[index + 1][10]))
            TFGMult = findMultiplier(float(tempStats[index][13]), float(tempStats[index + 1][13]))
            FTMult = findMultiplier(float(tempStats[index][20]), float(tempStats[index + 1][20]))
            FGMultipliers.append(FGMult)
            TFGMultipliers.append(TFGMult)
            FTMultipliers.append(FTMult)
    if(len(FGMultipliers) == 0):
        return currPlayer
    FGAverage = float(sum(FGMultipliers) / len(FGMultipliers))
    TFGAverage = float(sum(TFGMultipliers) / len(TFGMultipliers))
    FTAverage = float(sum(FTMultipliers) / len(FTMultipliers))

    newPlayer = [currPlayer[0] * FGAverage, currPlayer[1] * TFGAverage, currPlayer[2] * FTAverage]

    return newPlayer

def writePlayersToCSV(playerDictionary):
    filename = 'yearClusterCSV/2021Cluster.csv'
    playerNames = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            for name in row:
                playerNames.append(name)
    playerNames.sort()
    filepath = 'predictedStats.csv'
    with open(filepath, 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'PPG', 'APG', 'RBG', 'FG%', '3PT%', 'FT%'])
        for name in playerNames:
            tempStats = testForPlayer(playerDictionary, name)
            tempPercentage = testForPlayerPercentage(playerDictionary, name)
            tempStats.append(round(tempPercentage[0] * 100.0, 1))
            tempStats.append(round(tempPercentage[1] * 100.0, 1))
            tempStats.append(round(tempPercentage[2] * 100.0, 1))
            tempStats.insert(0, name)
            writer.writerow(tempStats)






if __name__ == '__main__':
    _, playerDictionary, ageDictionary  = load_data()
    # writeToAgeCSV(ageDictionary)
    # writeClustersToCSV()
    # print(testForPlayerPercentage(playerDictionary, 'Stephen Curry'))
    writePlayersToCSV(playerDictionary)
