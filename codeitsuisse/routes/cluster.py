from collections import deque
import logging
import json

from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = {"answers":{cluster(data)}}
    logging.info("result :{}".format(results))

    return json.dumps(results)

def cluster(grid):
    m = len(grid)
    n = len(grid[0])
    count = 0
    visited = [[False]*n for i in range(m)]
    for i in range(m):
        for j in range(n):
            if not visited[i][j] and grid[i][j] == '1':
                count += 1
                visited[i][j] = True
                queue = deque([(i,j)])
                while len(queue) > 0:
                    curr = queue.popleft()
                    for neighbor in getNeighbors(curr[0],curr[1],m,n):
                        if not visited[neighbor[0]][neighbor[1]]:
                            if grid[neighbor[0]][neighbor[1]] != '*':
                                print(neighbor)
                                visited[neighbor[0]][neighbor[1]] = True
                                queue.append((neighbor[0],neighbor[1]))
    return count

def getNeighbors(i,j,m,n):
    neighbors = []
    if i > 0 and j > 0:
        neighbors.append((i-1,j-1))
    if i > 0:
        neighbors.append((i-1,j))
    if i > 0 and j < n-1:
        neighbors.append((i-1,j+1))
    if j < n-1:
        neighbors.append((i,j+1))
    if i < m-1 and j < n-1:
        neighbors.append((i+1,j+1))
    if i < m-1:
        neighbors.append((i+1,j))
    if i < m-1 and j > 0:
        neighbors.append((i+1,j-1))
    if j > 0:
        neighbors.append((i,j-1))
    return neighbors

# grid =    [
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "0", "0", "0", "*", "*", "*", "*", "*"],
#     ["*", "*", "1", "*", "*", "*", "*", "*", "*"],
#     ["*", "0", "0", "0", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "0", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "0", "0", "*", "*"],
#     ["*", "*", "*", "*", "1", "*", "*", "*", "0"],
#     ["*", "*", "*", "*", "0", "*", "*", "0", "0"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"],
#     ["*", "*", "1", "0", "0", "*", "*", "*", "*"],
#     ["*", "*", "*", "*", "*", "*", "*", "*", "*"]
#   ]

# count = cluster(grid)
# print(count)