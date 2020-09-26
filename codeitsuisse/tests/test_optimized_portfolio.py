from codeitsuisse.routes.optimized_portfolio import optimized_portfolio
import pandas as pd

def test_optimized_portfolio():
    data = {
        "inputs": [
            {
                "Portfolio": {"Name": "Portfolio_Unhedged", "Value": 200000000, "SpotPrcVol": 0.75},
                "IndexFutures":
                    [
                        {"Name": "Index_Fut_A", "CoRelationCoefficient": 0.1, "FuturePrcVol": 0.95,
                         "IndexFuturePrice": 20.5, "Notional": 100000},
                        {"Name": "Index_Fut_B", "CoRelationCoefficient": 0.25, "FuturePrcVol": 0.85,
                         "IndexFuturePrice": 15.5, "Notional": 1000},
                        {"Name": "Index_Fut_C", "CoRelationCoefficient": 0.25, "FuturePrcVol": 0.85,
                         "IndexFuturePrice": 15.5, "Notional": 100000}
                    ]
            }
        ]
    }
    d = data["inputs"][0]
    portfolio_value = d["Portfolio"]["Value"]
    spot_volatility = d["Portfolio"]["SpotPrcVol"]
    df = pd.DataFrame(d["IndexFutures"])

    result = optimized_portfolio(portfolio_value, spot_volatility, df)

    print(print(result))
