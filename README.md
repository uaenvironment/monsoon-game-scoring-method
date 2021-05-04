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

