Game Sim Viz
------------

Author: CJ Larsen [seajaylarsen@email.arizona.edu]<br/>
Date: April 27, 2021

## Graph Notes

Consists of three bar charts (one for each scoring method), utilizing the same 1000 user simulated guesses for each graph. The scale ranges are 0-80 for both axes, so that the charts can be compared against eachother easily.

## How it Works

### To Create New Simulation Data Set

1 - Run newsim.py, this will generate the guesses/points.<br/>
2 - Refresh/open index.html in browser, this will create and display the charts.

### newsim.py

This Python script will simulate a season's worth of guesses/points for 1000 users. It runs as so:<br/>
* The 'actual' rainfall for the year is read in from input.json.
* Historical rainfall is read in from HistoricalCleaned.json. The standard deviation, mean, and decile ranges are also calculate for each month in each city.
- Guesses are simulated for each user by choosing a random decile (0-10, 10-20, ect) for each month in each city.
- Points are calculated for each guess based off of each scoring function (a, b or c).
- Points are converted and written to output.js so it can be visualized with d3.

### sim.js

This JavaScript file just creates three bar charts based off of the data in output.js.

## Included files

* README.md -- this file
* newsim.py -- python script to generate guesses/points
* sim.js -- js to create charts for each scoring method
* d3.js -- d3 library used for visualizing data
* index.html -- eventual content for the bar charts
* input.json -- input file containing total rainfall for each month in each city
* HistoricalCleaned.json -- historical rain data going back to 1899
* output.js -- output file from python to be used in javascript


# The Scoring System
------------------

Author: Dharma Hoy [dharmahoy@email.arizona.edu]<br/>
Data: May 7, 2021

## Overview

The scoring system has two parts. The first part determines the maximum points a user can get one month based on the actual amount of rainfall that was measured and the second part determines what percentage of the maximum point value the user gets based on how close their guess was to the actual rainfall. 

## Max Points Formula

The formula used to determine the max points for one month is as follows. 

<p align="center">  
max_points=-4*exp(-((log(x/m))^2))+8

In this formula m is the average rainfall from past data, s is the standard deviation of the past data, and x is the rainfall that was measured this year. When graphed with respect to x and standard deviation and average set constant the max points is at a minimum when the rainfall is equal to the average rainfall and increases as the rainfall gets further away from the average. This is because this scoring system takes into consideration the risk of a users guess. The further a guess is away from the average rainfall the riskier that guess is and the higher the potential reward. To use this formula, the actual rainfall for the month, the average and standard deviaton of the past rainfall of the month should be plugged into the equation as x, m, and s respectivly. 

## Get Points Function
This function uses the standard deviaton of past data, the actual rainfall for the month, the user guess, and the max point value determed by the formula and calculates the number of points the user gets. If the user is within or equal to a quarter of a standard deviation from the actual rainfall they recieve the max point value. If they are further than a quarter of a standard deviation away but less than or equal to half a standard deviation away they recieve 75% of the max point value. If the user is further than half a standard deviation away but less than or equal too three quarters of a standard deviation away they recieve 50% of the max point value. If they are further than three quarters of a standard deviation away but less than or equal to one standard deviation away they recieve 25% of the max point value. Any guess that is more than one standard deviation from the actual rainfall recieves zero points.
