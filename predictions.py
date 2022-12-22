import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import norm, gamma, poisson

# read in data
matches = pd.read_csv("spi_matches_latest.csv")
table = pd.read_csv("league_table.csv")
matches["spi_diff"] = matches.spi1 - matches.spi2
matches["xg_diff"] = matches.xg1 - matches.xg2
matches["xg_total"] = matches.xg1 + matches.xg2
matches["score_diff"] = matches.score1 - matches.score2

# split data into train and test
train = matches.dropna()
test = matches[(matches.league == "Barclays Premier League") & (matches.date > "2022-12-25")].iloc[:, 0:8]
test["spi_diff"] = test.spi1 -test.spi2

# train model to predict xg_diff
X_train = np.array(train.spi_diff).reshape(-1, 1)
y_train = np.array(train.xg_diff)
xg_diff_lm_fit = LinearRegression().fit(X_train, y_train)
xg_diff_lm_sigma = mean_squared_error(y_train, xg_diff_lm_fit.predict(X_train))

# function to simulate season
def sim_season(matches):
    n = len(matches)

    # get xg_diff predictions
    X_test = np.array(matches.spi_diff).reshape(-1, 1)
    matches["predicted_xg_diff"] = norm.rvs(loc=xg_diff_lm_fit.predict(X_test), scale=xg_diff_lm_sigma, size=n)

    # get xg_total predictions
    matches["predicted_xg_total"] = gamma.rvs(a=2.35*2.5, scale=1/2.5, size=n) + abs(matches.predicted_xg_diff)

    # calculated predicted xg for each team
    matches["predicted_xg1"] = (matches.predicted_xg_total + matches.predicted_xg_diff) / 2
    matches["predicted_xg2"] = (matches.predicted_xg_total - matches.predicted_xg_diff) / 2

    # get predicted score
    matches["predicted_score1"] = poisson.rvs(mu=matches.predicted_xg1, size=n)
    matches["predicted_score2"] = poisson.rvs(mu=matches.predicted_xg2, size=n)

    # calculate points
    condition_list = [
        matches.predicted_score1 > matches.predicted_score2,
        matches.predicted_score1 == matches.predicted_score2
    ]
    matches["points1"] = np.select(condition_list, [3, 1], default=0)
    matches["points2"] = np.select(condition_list, [0, 1], default=3)

    return(matches)

def get_points(sim_season, cur_table):
    clubs = sorted(sim_season.team1.unique())

    points = []
    for i in clubs:
        cur_points = sum(cur_table[cur_table.Team == i].Points)
        team1_points = sum(sim_season[sim_season.team1 == i].points1)
        team2_points = sum(sim_season[sim_season.team2 == i].points2)
        points.append(cur_points + team1_points + team2_points)
    
    results = pd.DataFrame({"club": clubs, "points": points}).sort_values(by=["points"], ascending=False)

    return(results)

if __name__ == '__main__':
    print(get_points(sim_season(test), table))