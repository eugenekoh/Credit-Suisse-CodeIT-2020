import logging

from flask import request, jsonify
from ortools.linear_solver import pywraplp

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_olympiad_of_babylon():
    data = request.get_json()
    logging.info(f"olympiad-of-babylon data: {data}")

    num_books = data["numberOfBooks"]
    num_days = data["numberOfDays"]
    books = data["books"]
    days = data["days"]

    result = {
        "optimalNumberOfBooks": olympiad_of_babylon(num_books, num_days, books, days)
    }

    logging.info(f"olympiad-of-babylon result: {result}")
    return jsonify(result)


def olympiad_of_babylon(num_books, num_days, books, days):
    """
    https://cis2020-olympiad-of-babylon.herokuapp.com/

    Multiple 0-1 Knapsack Problem: https://developers.google.com/optimization/bin/multiple_knapsack
    """

    # create data model
    data = {
        "weights": books,
        "values": [1] * num_books,
        "items": list(range(num_books)),
        "num_items": num_books,
        "bins": list(range(num_days)),
        "bin_capacities": days
    }

    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('multiple_knapsack_mip', 'CBC')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print('Total packed value:', objective.Value())
        # total_weight = 0
        # for j in data['bins']:
        #     bin_weight = 0
        #     bin_value = 0
        #     print('Bin ', j, '\n')
        #     for i in data['items']:
        #         if x[i, j].solution_value() > 0:
        #             print('Item', i, '- weight:', data['weights'][i], ' value:',
        #                   data['values'][i])
        #             bin_weight += data['weights'][i]
        #             bin_value += data['values'][i]
        #     print('Packed bin weight:', bin_weight)
        #     print('Packed bin value:', bin_value)
        #     print()
        #     total_weight += bin_weight
        # print('Total packed weight:', total_weight)

        return int(objective.Value())
    else:
        logger.log("no optimal solution found.")
        return -1
