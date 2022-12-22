import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


# read in data
matches = pd.read_csv("spi_matches_latest.csv")
matches["spi_diff"] = matches.spi1 - matches.spi2
matches["xg_diff"] = matches.xg1 - matches.xg2
matches["xg_total"] = matches.xg1 + matches.xg2
matches["score_diff"] = matches.score1 - matches.score2

# split data into train and test
train = matches.dropna()
test = matches[(matches.league == "Barclays Premier League") & (matches.date > "2022-12-25")]

# train model to predict xg_diff for test data
X_train = np.array(train.spi_diff).reshape(-1, 1)
y_train = np.array(train.xg_diff)
xg_diff_lm_fit = LinearRegression().fit(X_train, y_train)

X_test = np.array(test.spi_diff).reshape(-1, 1)
test["xg_diff"] = xg_diff_lm_fit.predict(X_test)

if __name__ == '__main__':
    pass