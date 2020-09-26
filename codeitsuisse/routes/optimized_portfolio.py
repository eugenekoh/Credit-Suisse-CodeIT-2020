import logging
import numpy as np

import pandas as pd
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimized_portfolio():
    data = request.get_json()["inputs"]

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
    return corelation * spot_vol / futures_vol


def num_futures_contract(hedge_ratio, portfolio_val, futures_price, notional_val):
    return np.ceil(hedge_ratio * portfolio_val / (futures_price * notional_val))


def optimized_portfolio(portfolio_value, spot_volatility, df):
    df["OptimalHedgeRatio"] = hedge_ratio(df["CoRelationCoefficient"].values, spot_volatility,
                                          df["FuturePrcVol"].values)
    min_hedges = df[df["OptimalHedgeRatio"] == df["OptimalHedgeRatio"].min()].index
    min_future_vols = df[df["FuturePrcVol"] == df["FuturePrcVol"].min()].index

    total = min_hedges.union(min_future_vols)
    if len(total) == 1:
        row = df.iloc[total[0]]
        num = num_futures_contract(row["OptimalHedgeRatio"], portfolio_value, row["IndexFuturePrice"], row["Notional"])
        result = {
            "HedgePositionName": row["Name"],
            "OptimalHedgeRatio": round(row["OptimalHedgeRatio"], 3),
            "NumFuturesContract": int(num)
        }
        return result

    df = df.iloc[total]
    df["NumFuturesContract"] = num_futures_contract(df["OptimalHedgeRatio"].values, portfolio_value,
                                                    df["IndexFuturePrice"].values,
                                                    df["Notional"].values)

    min_num_futures = df[df["NumFuturesContract"] == df["NumFuturesContract"].min()]
    row = min_num_futures.iloc[0]
    if len(min_num_futures.index) > 1:
        logger.error("unable to decide by num_futures")

    hedge_result = {
        "HedgePositionName": row["Name"],
        "OptimalHedgeRatio": round(row["OptimalHedgeRatio"], 3),
        "NumFuturesContract": int(row["NumFuturesContract"])
    }

    return hedge_result
