# English Premier League 2022 Predictions

Model predicting the outcome of the 2022 English Premier League season.
The model simulates each game individually, so it is capable of making game by game predictions.
Below, I show the model's predictions for league champion based on 10,0000 simulations of the season after returning from the world cup.

## Champion Predictions

Champion probabilities by club.
I've included [FiveThirtyEight's](https://projects.fivethirtyeight.com/soccer-predictions/premier-league/) forecast as of 11-13-2022 for comparision.
We have the same top nine clubs but in different orders.

| Club | Prob. | FiveThirtyEight Prob. |
| ---- | ----- | --------------------- |
| Arsenal | 46.62% | 36% |
| Manchester City | 45.00% | 53% |
| Tottenham | 3.17% | 2% |
| Newcastle | 2.84% | 2% |
| Manchester United | 1.18 % | 2% |
| Liverpool | 0.68% | 3% |
| Chelsea | 0.43% | <1% |
| Brighton | 0.07% | <1% |
| Crystal Palace | 0.01% | <1% |
| All Others | <0.01% | <1% |

## About

`exploratory.ipynb` has some nice graphs and justifications for some modeling decisions.
`predictions.py` contains the model and code used to get the champion probabilities.

## Data

[FiveThirtyEight SPI Data](https://github.com/fivethirtyeight/data/tree/master/soccer-spi) was used for this project. 
`spi_matches_latest.csv` was downloaded on 12-04-2022.
`league_table.csv` contains the league table as of 12-25-2022 -- the last day before the Premier League returns from the World Cup break.

