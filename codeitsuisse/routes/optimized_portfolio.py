import logging

from flask import request, jsonify

import pandas as pd

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_optimized_portfolio():
    data = request.get_json()["inputs"]
    # data = data["inputs"]

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
    return hedge_ratio * portfolio_val / (futures_price * notional_val)


def optimized_portfolio(portfolio_value, spot_volatility, df):
    min_futures_idx = df["FuturePrcVol"].idxmin()

    df["OptimalHedgeRatio"] = hedge_ratio(df["CoRelationCoefficient"].values, spot_volatility,
                                          df["FuturePrcVol"].values)
    min_hedge_idx = df["OptimalHedgeRatio"].idxmin()

    # tie breaker
    row = df.loc[min_futures_idx, :]
    min_futures = num_futures_contract(row["OptimalHedgeRatio"], portfolio_value, row["IndexFuturePrice"],
                                       row["Notional"])
    futures_result = {
        "HedgePositionName": row["Name"],
        "OptimalHedgeRatio": round(row["OptimalHedgeRatio"], 3),
        "NumFuturesContract": round(min_futures)
    }

    if min_futures_idx == min_hedge_idx:
        return futures_result

    row = df.loc[min_hedge_idx, :]
    min_hedge = num_futures_contract(row["OptimalHedgeRatio"], portfolio_value, row["IndexFuturePrice"],
                                     row["Notional"])
    hedge_result = {
        "HedgePositionName": row["Name"],
        "OptimalHedgeRatio": round(row["OptimalHedgeRatio"], 3),
        "NumFuturesContract": round(min_hedge)
    }

    if min_hedge < min_futures:
        return hedge_result
    else:
        return futures_result
