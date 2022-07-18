Table of Contents
-----------------
[Introduction](https://github.com/UAEnvironmentIT/monsoon-game-scoring-method#introduction)<br>
[Included Files](https://github.com/UAEnvironmentIT/monsoon-game-scoring-method#included-files)<br>
[The Scoring System](https://github.com/UAEnvironmentIT/monsoon-game-scoring-method#the-scoring-system)<br>
[The Scoring System - Technical Description](https://github.com/UAEnvironmentIT/monsoon-game-scoring-method#for-the-more-technically-interested)<br>
[Game Simulation](https://github.com/UAEnvironmentIT/monsoon-game-scoring-method#game-sim-viz)<br>

Introduction
------------

This repository contains a description of the scoring system used in the [Monsoon Fantasy](https://monsoonfantasy.arizona.edu/home) game and a simulation that was used to compare different scoring methods before the final scoring method was decided upon. The final scoring method takes into account both the risk and accuracy of a players guess. First, a potential maximum points value is determined for a guess. This value is higher the further a guess is from the historical rainfall average. Then, the player gets a percentage of their potential maximum points value depending on how close their guess is to the actual rainfall. This is explained in more detail in the scoring system section below. The simulation is for demonstration purposes. It creates a dataset with guesses and points for simulated users than graphs their total points. 

## Included files

* README.md -- this file
* newsim.py -- python script to generate guesses/points
* sim.js -- js to create charts for each scoring method
* d3.js -- d3 library used for visualizing data
* index.html -- eventual content for the bar charts
* input.json -- input file containing total rainfall for each month in each city
* HistoricalCleaned.json -- historical rain data going back to 1899
* output.js -- output file from python to be used in javascript

The Scoring System
------------------

***Overview***

Points are scored each month and for each city, with the winner determined by the total points accumulated over the three months and five cities. 

For each month and each city, points are calculated by considering the riskiness of the forecast and its accuracy. The risk of the forecast depends on how likely the forecasted value is to actually occur based on the historical record. Less likely estimates are those that occur further from the average. Riskier forecasts have higher *possible* points. They are *possible* points because the scoring also depends on the accuracy of the forecast. The more accurate the forecast is, the more points the player receives.

Let’s look at an example for Tucson (at the Tucson International Airport).

A histogram of July rainfall totals for Tucson between 1950-2020 (71 years) is shown below in the figure’s blue bars. Each vertical bar represents the number of times Tucson received rainfall in July within an inch range. For example, in 21 of the 71 years, Tucson received between 4 and 5 inches. An extremely dry July such as in 2020 when Tucson received 0.46 inches, were much less frequent; only 1 July on record had between 0 and 1 inches. Similarly, July rainfall that was extremely high was infrequent too, with only 3 occurrences of more than 9 inches for the month of July.      

![tucsonbargraph](https://user-images.githubusercontent.com/80312888/120421554-602c9580-c31b-11eb-93cd-8846f5158df6.JPG)

***Maximum Potential Points for your Forecast***

Because Tucson experienced only a few months with rainfall between 1 and 2 inches, a player who forecasts 1.5 inches has the potential to earn a higher number of points than someone who estimates a forecast closer to the average rainfall (about 6 inches) for the month. In other words, lower probable outcomes generate greater benefits—higher risk equals higher reward.

***Total Points Based on Accuracy***

Riskiness determines the maximum points that can be obtained. The accuracy determines how many of those points are actually scored. Accuracy is determined by comparing the forecast to the actual rainfall. The more accurate the forecast, the more of the maximum points awarded.

Because it is unlikely that any forecast is perfect, accuracy is determined in four tiers. Each tier represents a range. The range is smallest for the tier that awards the most points. In other words, to score 100% of the maximum points, the actual rainfall has to be close to the forecast.

The range is calculated with the standard deviation of the city’s historical rainfall. One standard deviation basically accounts for about 68% of the data. The four tiers are fractions of a standard deviation, as shown in the table.

| Accuracy Range               | % of Maximum Points |
| ---------------------------- | ------------------- |
| +/-  0.25 standard deviation | 100                 |
| +/-  0.50 standard deviation | 75                  |
| +/-  0.75 standard deviation | 50                  |
| +/-  1.00 standard deviation | 25                  |
|  >   1.00 standard deviation | 0                   |

Again, let’s look at Tucson in July as an example. One standard deviation equals about 1 inch of rain. Therefore, to score 100% of the maximum points for a forecast of 5 inches, the rainfall would need to fall between 4.75 and 5.25 inches. A score of 75% of the maximum points occurs if the rainfall is within 4.50 and 5.50 (but, obviously, not within 4.75 and 5.25 because that would receive 100% of the points). 

You can see how riskiness and accuracy are combined to generate points in the table. Example is from Tucson, where the standard deviation is 1 inch.

| **Description of Guess**  | **Forecast Estimate (inches)** | **Possible Maximum Points** | **Actual Rainfall (inches)** | **Total Points Scored** |
| ------------------------- | ------------------------------ | --------------------------- | ---------------------------- | ----------------------- |
| Risky and accurate        | 5.0                            | 7                           | 4.8                          | 7                       |
| Risky but inaccurate      | 5.0                            | 7                           | 2.4                          | 0                       |
| Less risky and accurate   | 2.4                            | 4                           | 2.4                          | 4                       |
| Less risky but inaccurate | 2.4                            | 4                           | 3.0                          | 2                       |


For those interested in how the maximum points are derived mathematically, please read on ☺. 

## For the more technically interested...
***Here’s how we calculate the maximum points.***

First, the monthly total rainfall distributions are not normally distributed. They have a positive skew which means the mean value is greater than the median value. We therefore used an equation to account for this skew.

We used a log-normal formula to determine the maximum points in a positively skewed distribution as follows.

Max points = -4 * exp(-((log(x/m))^2) / (2*(s/2)^2)) +8

The variables in this formula are the following:

- “x” is the users predicted rainfall in the month this year, 
- “m” is the average rainfall for the month calculated from the historical record, and
- “s” is the standard deviation of the historical data. 

We can graph this equation with respect to the user's predicted rainfall on the x-axis and the possible maximum points scored on the y-axis. We show this for Tucson’s July rainfall where the mean is 2.39 inches and the standard deviation is 1.03 inches.

![tucsonmaxpoints](https://user-images.githubusercontent.com/80312888/120421592-720e3880-c31b-11eb-91f0-a75b44401588.JPG)

This graph shows that as the forecasted value is further away from the mean, the maximum possible points are higher. The graph also shows that the lowest maximum points are for values that are closer to the mean. 

***Here’s how we calculate the points scored each month.***

We calculate the points by determining how close the forecast is to the actual rainfall values and allocating a fraction of the maximum points based on this accuracy. Accuracy is determined by the standard deviation. There are four tiers as described in the table above. 

***JavaScript Code.***

The following code is how we calculate points. It is written in JavaScript.

```
function getScore(average,standardDeviation,rainfall,guess){
    // find max points
    maxPoints = -4 * Math.exp(-((Math.log(guess/average))**2)/(2*(standardDeviation/2)**2))+8
    // greater than 1 standard deviation
    if (guess < (rainfall-standardDeviation) || guess > (rainfall+standardDeviation)){
        points=0
        return points
    }else if (guess < (rainfall-0.75*standardDeviation) || guess > (rainfall+0.75*standardDeviation)){
        // greater than 0.75 standard deviations 
        points=Math.round(maxPoints*0.25) 
        return points
    }else if (guess < (rainfall-0.5*standardDeviation) || guess > (rainfall+0.5*standardDeviation)){
        // greater than 0.5 standard deviation
        points=Math.round(maxPoints*0.5)
        return points
    }else if (guess < (rainfall-0.25*standardDeviation) || guess > (rainfall+0.25*standardDeviation)){
        // greater than .25 standard deviations
        points=Math.round(maxPoints*0.75)
        return points
    }else {
        points=maxPoints
        return points
    }
}
```

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
