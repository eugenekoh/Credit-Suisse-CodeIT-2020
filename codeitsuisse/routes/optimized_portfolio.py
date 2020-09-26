import json
import logging
import time

import numpy as np
from sklearn import preprocessing
import pandas as pd
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimized_portfolio():
    data = request.get_json()["inputs"]
    # logger.info(request.get_json())
    outputs = []

    for d in data:
        portfolio_value = d["Portfolio"]["Value"]
        spot_volatility = d["Portfolio"]["SpotPrcVol"]
        df = pd.DataFrame(d["IndexFutures"])
        outputs.append(optimized_portfolio(portfolio_value, spot_volatility, df))

    result = {
        "outputs": outputs
    }

    return jsonify(result)


def hedge_ratio(corelation, spot_vol, futures_vol):
    return np.round(corelation * spot_vol / futures_vol, 3)


def num_futures_contract(hedge_ratio, portfolio_val, futures_price, notional_val):
    return np.round(hedge_ratio * portfolio_val / (futures_price * notional_val))


def optimized_portfolio(portfolio_value, spot_volatility, df):
    df["OptimalHedgeRatio"] = hedge_ratio(df["CoRelationCoefficient"].values, spot_volatility,
                                          df["FuturePrcVol"].values)
    df["NumFuturesContract"] = num_futures_contract(df["OptimalHedgeRatio"].values, portfolio_value,
                                                    df["IndexFuturePrice"].values,
                                                    df["Notional"].values)
    min_max_scaler = preprocessing.MinMaxScaler()
    df['FuturePrcVolScaled'] = min_max_scaler.fit_transform(df['FuturePrcVol'].values)
    df['HRVolCombined'] = df['OptimalHedgeRatio'] + df['FuturePrcVolScaled']

    min_hr_vols = df[df["HRVolCombined"] == df["HRVolCombined"].min()].index
    if len(min_hr_vols) == 1:
        row = df.iloc[min_hr_vols[0]]
        result = {
            "HedgePositionName": row["Name"],
            "OptimalHedgeRatio": row["OptimalHedgeRatio"],
            "NumFuturesContract": int(row["NumFuturesContract"])
        }
        return result
    
    if len(min_hr_vols) > 1:
        df = df.iloc[min_hr_vols]
        min_num_futures = df[df["NumFuturesContract"] == df["NumFuturesContract"].min()]
        row = df.iloc[min_num_futures[0]]
        result = {
            "HedgePositionName": row["Name"],
            "OptimalHedgeRatio": row["OptimalHedgeRatio"],
            "NumFuturesContract": int(row["NumFuturesContract"])
        }
        return result
    # min_hedges = df[df["OptimalHedgeRatio"] == df["OptimalHedgeRatio"].min()].index
    # min_future_vols = df[df["FuturePrcVol"] == df["FuturePrcVol"].min()].index

    # total = min_hedges.union(min_future_vols)
    # if len(total) == 1:
    #     row = df.iloc[total[0]]
    #     num = num_futures_contract(row["OptimalHedgeRatio"], portfolio_value, row["IndexFuturePrice"], row["Notional"])
    #     result = {
    #         "HedgePositionName": row["Name"],
    #         "OptimalHedgeRatio": row["OptimalHedgeRatio"],
    #         "NumFuturesContract": int(num)
    #     }
    #     return result

    # df = df.iloc[total]

    # min_num_futures = df[df["NumFuturesContract"] == df["NumFuturesContract"].min()]
    # row = min_num_futures.iloc[0]
    # if len(min_num_futures.index) > 1:
    #     logger.error("unable to decide by num_futures")

    # hedge_result = {
    #     "HedgePositionName": row["Name"],
    #     "OptimalHedgeRatio": row["OptimalHedgeRatio"],
    #     "NumFuturesContract": int(row["NumFuturesContract"])
    # }

    # return hedge_result
