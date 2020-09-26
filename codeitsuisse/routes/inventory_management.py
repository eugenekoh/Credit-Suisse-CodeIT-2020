import logging
import json

from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory_management():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = []
    for test_case in data:
        results.append(manage_inventory(test_case['searchItemName'], test_case['items']))
    logging.info("result :{}".format(results))

    return json.dumps(results)

def manage_inventory(itemName, items):
    original = itemName
    # itemName = itemName.lower()
    m = len(itemName)
    outputs = []
    for item in items:
        output = []
        n = len(item)
        dp = [[0]*(n+1) for i in range(m+1)]
        dp2 = [[[None,""]]*(n+1) for i in range(m+1)]
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 and j == 0:
                    dp[i][j] = 0
                    dp2[i][j] = [None,'']
                elif i == 0:
                    dp[i][j] = j
                    dp2[i][j] = [None, dp2[i][j-1][1] + f'+{item[j-1]}']
                elif j == 0:
                    dp[i][j] = i
                    dp2[i][j] = [None, dp2[i-1][j][1] + f'-{itemName[i-1]}']
        for i in range(1, m+1):
            for j in range(1, n+1):
                if itemName[i-1] == item[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                    dp2[i][j] = [2,item[j-1]]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                    if dp[i-1][j] < dp[i][j-1] and dp[i-1][j] < dp[i-1][j-1]:
                        dp2[i][j] = [0,f'-{itemName[i-1]}']
                    elif dp[i][j-1] < dp[i-1][j] and dp[i][j-1] < dp[i-1][j-1]:
                        dp2[i][j] = [1,f'+{item[j-1]}']
                    else:
                        dp2[i][j] = [2,f'{item[j-1]}']

        row = m
        col = n
        curr = dp2[row][col]
        while curr[0] is not None:
            output.append(curr[1])
            if curr[0] == 0:
                row -= 1
            elif curr[0] == 1:
                col -=1
            else:
                row -= 1
                col -= 1
            curr = dp2[row][col]
        output.append(curr[1])
        outputs.append((''.join(output[::-1]),dp[-1][-1]))
    outputs.sort(key = lambda x: (x[1],x[0]))
    if len(outputs) > 10:
        outputs = outputs[:10]
    return {"searchItemName":original, "searchResult":[x[0] for x in outputs]}

# [{"searchItemName":"Samsung Aircon","items":["Smsng Auon","Amsungh Aircon","Samsunga Airon"]}]

# output = manage_inventory("Samsung Aircon",["Smsng Auon","Amsungh Aircon","Samsunga Airon"])
# print(output)