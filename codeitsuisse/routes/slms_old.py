import logging
from dataclasses import dataclass

import enum
from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


class JumpType(enum.Enum):
    Normal = 0
    Snake = 1
    Ladder = 2
    Smoke = 3
    Mirror = 4
    End = 5


class JumpNode:
    def __init__(self, t=None, n=None):
        self.type = t
        self.next = n

    def __repr__(self):
        return f"{self.type}"


class Roll:
    def __init__(self, from_jump=None, value=None, location=None):
        self.from_jump = from_jump
        self.value = value
        self.location = location

    def __repr__(self):
        return f"{self.value}"


@app.route('/slsm', methods=['POST'])
def evaluate_slsm():
    data = request.get_json()

    n = data["boardSize"]
    players = data["players"]
    jumps = data["jumps"]

    s = Solution(n, players, jumps)
    result = s.get_rolls()

    return jsonify(result)


def setup_board(n, jumps):
    board = [JumpNode(JumpType.Normal) for _ in range(n)]
    board[-1] = JumpNode(JumpType.End)

    # note this is 1 based indexing
    for jump in jumps:
        left, right = jump.split(":")

        left = int(left)
        right = int(right)

        if left > 0:
            left = left - 1
        if right > 0:
            right = right - 1

        if left == 0:
            board[right] = JumpNode(JumpType.Mirror)
        elif right == 0:
            board[left] = JumpNode(JumpType.Smoke)
        elif left < right:
            board[left] = JumpNode(JumpType.Ladder, right)
        elif left > right:
            board[left] = JumpNode(JumpType.Snake, right)
        else:
            raise Exception("unexpected jump parsing")

    return board


class Solution:
    def __init__(self, n, players, jumps):
        self.board = setup_board(n, jumps)
        self.last_idx = len(self.board) - 1
        self.players = players
        self.memo = {}

    def search(self, i, path, visited):
        # bounce back
        if i >= len(self.board):
            i = self.last_idx - i % len(self.board)

        # detect cycles and exit search space
        if i in visited:
            return []

        node = self.board[i]

        if node.type == JumpType.End:
            return path
        elif node.type in [JumpType.Ladder, JumpType.Snake]:
            return self.search(node.next, path, visited)

        # use memo
        if i in self.memo:
            return self.memo[i]

        min_way = []

        # one roll to the end
        if node.type in [JumpType.Mirror, JumpType.Normal] and i + 6 >= self.last_idx:
            from_jump = node.type == JumpType.Mirror
            value = self.last_idx - i
            roll = Roll(from_jump, value, i)
            return path + [roll]

        # random roll paths
        for j in range(1, 7):
            from_jump = False
            if node.type == JumpType.Smoke:
                from_jump = True
                j = -j
            elif node.type == JumpType.Mirror:
                from_jump = True

            roll = Roll(from_jump, abs(j), i)
            new_visited = visited.copy()
            new_visited.add(i)

            new_path = path + [roll]
            way = self.search(i + j, new_path, new_visited)

            # get the minimum rolls to reach target
            if (way and not min_way) or (way and len(min_way) > len(way)):
                min_way = way

        self.memo[i] = min_way
        return min_way
