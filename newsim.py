
import json
import math
import statistics
import numpy as np
import random
import matplotlib.pyplot as plt

# constants
CITIES = ['Albuquerque', 'El Paso', 'Flagstaff', 'Phoenix', 'Tucson']
MONTHS = ['June', 'July', 'August', 'September']
METHODS = ['a', 'b', 'c', 'd', 'e', 'f']
GUESSNUM = 1000


def main():
    actuRain = getActuRain()
    histRain = getHistRain()
    guessDict = getGuesses(histRain)
    pointDict = calcPoints(actuRain, histRain, guessDict)
    exportData(pointDict)


def getActuRain():
    '''
    getActuRain() - reads in rain data from input.js
    '''
    f = open('input.json',)
    data = json.load(f)

    # rain totals for each month
    total = {}

    for city in CITIES:
        actRain = {}

        actRain['June'] = float(data[city]['June'])
        actRain['July'] = float(data[city]['July'])
        actRain['August'] = float(data[city]['August'])
        actRain['September'] = float(data[city]['September'])
        total[city] = actRain

    f.close()

    return total


def getHistRain():
    '''
    histRain() - read in historical rain data to be used later
    '''
    rainData = {}
    for city in CITIES:
        # arrays to hold rain logs
        juneRain = []
        julyRain = []
        augRain = []
        sepRain = []

        f = open('HistoricalCleaned.json',)
        data = json.load(f)

        for year, info in data.items():
            # populate arrays
            juneRain.append(float(info[city]["June"]))
            julyRain.append(float(info[city]["July"]))
            augRain.append(float(info[city]["August"]))
            sepRain.append(float(info[city]["September"]))

        f.close()

        # get standard deviation, decile ranges, and mean rain (all are need
        # to get point values)
        rainData[city] = {}

        rainData[city]["JuneRain"] = statistics.stdev(juneRain)
        rainData[city]["JuneDeciles"] = np.percentile(
            np.array(juneRain), np.arange(0, 100, 10))
        rainData[city]["JuneMean"] = statistics.mean(juneRain)

        rainData[city]["JulyRain"] = statistics.stdev(julyRain)
        rainData[city]["JulyDeciles"] = np.percentile(
            np.array(julyRain), np.arange(0, 100, 10))
        rainData[city]["JulyMean"] = statistics.mean(julyRain)

        rainData[city]["AugustRain"] = statistics.stdev(augRain)
        rainData[city]["AugustDeciles"] = np.percentile(
            np.array(augRain), np.arange(0, 100, 10))
        rainData[city]["AugustMean"] = statistics.mean(augRain)

        rainData[city]["SeptemberRain"] = statistics.stdev(sepRain)
        rainData[city]["SeptemberDeciles"] = np.percentile(
            np.array(sepRain), np.arange(0, 100, 10))
        rainData[city]["SeptemberMean"] = statistics.mean(sepRain)

    return rainData


def getGuesses(histRain):
    '''
    getGuesses(histRain) - simulate a season's worth of guesses for each guess,
    guesses are made based of random deciles
    '''
    guesses = {}

    for i in range(GUESSNUM):   # for each guess
        guesses[i] = {}
        for month in MONTHS:    # guess for each month
            guesses[i][month] = {}
            for city in CITIES:     # guess for each city each month
                guesses[i][month][city] = histRain[city][month +
                                                         'Deciles'][int(random.randint(0, 9))]

    return guesses


def calcPoints(actuRain, histRain, guessDict):
    '''
    calcPoints(actuRain, histRain, guessDict) - calculates appropriate points
    based of of each guess
    '''
    # inner function to yield points
    def getPoints(stdDev, mean, guess, actual, scoreFunc):
        '''
        getPoints(stdDev, mean, guess, actual, scoreFunc) - calculates the max
        points based off of user's choice, then returns the points rewarded
        '''
        # using dharma's original (a, b, c) and skewed (d, e, f) functions
        if (scoreFunc == 'a'):
            maxPoints = -4 * \
                math.exp((-(actual - mean)**2) / (2*(stdDev**2))) + 8
        elif (scoreFunc == 'b'):
            maxPoints = -2 * \
                math.exp((-(actual - mean)**2) / (2*(stdDev**2))) + 6
        elif (scoreFunc == 'c'):
            maxPoints = -1 * \
                math.exp((-(actual - mean)**2) / (2*(stdDev**2))) + 5
        elif (scoreFunc == 'd'):
            if (actual == 0):
                maxPoints = 8
            else:
                maxPoints = -4 * \
                    math.exp(-((math.log(actual / mean))**2) /
                             (2 * (stdDev / 2)**2)) + 8
        elif (scoreFunc == 'e'):
            if (actual == 0):
                maxPoints = 6
            else:
                maxPoints = -2 * \
                    math.exp(-((math.log(actual / mean))**2) /
                             (2 * (stdDev / 2)**2)) + 6
        elif (scoreFunc == 'f'):
            if (actual == 0):
                maxPoints = 5
            else:
                maxPoints = -1 * \
                    math.exp(-((math.log(actual / mean))**2) /
                             (2 * (stdDev / 2)**2)) + 5

        # calc actual points recieved
        if (guess < actual - stdDev or guess > actual + stdDev):
            return 0
        elif (guess < actual - stdDev*0.75 or guess > actual + stdDev*0.75):
            return round(maxPoints*0.25)
        elif (guess < actual - stdDev*0.5 or guess > actual + stdDev*0.5):
            return round(maxPoints*0.5)
        elif (guess < actual - stdDev*0.25 or guess > actual + stdDev*0.25):
            return round(maxPoints*0.75)
        else:
            return round(maxPoints)

    pointDict = {}
    for method in METHODS:
        pointArr = []
        for num, info in guessDict.items():
            totalPoints = 0
            for month, guesses in info.items():
                for city, guess in guesses.items():
                    temp = getPoints(histRain[city][month + 'Rain'], histRain[city]
                                     [month + 'Mean'], guess, actuRain[city][month], method)
                    totalPoints = totalPoints + temp
            pointArr.append(totalPoints)
        pointArr.sort()
        pointDict[method] = pointArr

    return pointDict


def exportData(pointDict):
    '''
    exportData(pointDict) - converts the data to a nice dictionary to be used
    by d3, writes it to output.js
    '''
    test = {}
    for method, points in pointDict.items():
        temp = {}
        for point in points:
            if str(point) not in temp:
                # point dict (object for js)
                temp[str(point)] = {
                    'x': point,
                    'y': 1
                }
            else:
                temp[str(point)]['y'] = temp[str(point)]['y'] + 1
        test[method] = temp

    # get only the array of point objects
    exportDict = {}
    for method, v in test.items():
        exportDict[method] = []
        for items in v.values():
            exportDict[method].append(items)

    with open('output.js', 'w') as outfile:
        outfile.write('let data = ')
        json.dump(exportDict, outfile)


main()
