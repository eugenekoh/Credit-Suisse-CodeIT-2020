from codeitsuisse.routes.optimized_portfolio import evaluate_optimized_portfolio


def test_optimized_portfolio():
    data = {
        "inputs": [
            {
                "Portfolio": {"Name": "Portfolio_Unhedged", "Value": 200000000, "SpotPrcVol": 0.75},
                "IndexFutures":
                    [
                        {"Name": "Index_Fut_A", "CoRelationCoefficient": 0.75, "FuturePrcVol": 0.95,
                         "IndexFuturePrice": 20.5, "Notional": 100000},
                        {"Name": "Index_Fut_B", "CoRelationCoefficient": 0.25, "FuturePrcVol": 0.85,
                         "IndexFuturePrice": 15.5, "Notional": 100000}
                    ]
            }
        ]
    }
    print(evaluate_optimized_portfolio(data))
