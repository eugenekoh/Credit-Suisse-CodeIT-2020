import logging
import networkx as nx

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
    logger.info(data)
    n = data["boardSize"]
    players = data["players"]
    jumps = data["jumps"]

    s = Solution(n, players, jumps)
    result = s.get_rolls()

    logger.info(result)
    return jsonify(result)


def setup_board(n, jumps):
    board = [JumpNode(JumpType.Normal) for _ in range(n)]
    board[-1] = JumpNode(JumpType.End)

    # note this is 1 based indexing
    for jump in jumps:
        left, right = jump.split(":")

        left = int(left)
        right = int(right)

        if left == 0:
            board[right - 1] = JumpNode(JumpType.Mirror)
        elif right == 0:
            board[left - 1] = JumpNode(JumpType.Smoke)
        elif left < right:
            board[left - 1] = JumpNode(JumpType.Ladder, right)
        elif left > right:
            board[left - 1] = JumpNode(JumpType.Snake, right)
        else:
            raise Exception("unexpected jump parsing")

    return board


class Solution:
    def __init__(self, n, players, jumps):
        self.board = setup_board(n, jumps)
        self.players = players
        self.G = self.setup_graph()

    def setup_graph(self):
        G = nx.DiGraph()

        for i in range(1, len(self.board) + 1):
            G.add_node(i)

        for u, node in enumerate(self.board):
            u += 1
            if node.type in [JumpType.Normal, JumpType.Mirror]:
                end = min(len(self.board), u + 6)
                for v in range(u + 1, end + 1):
                    G.add_edge(u, v, weight=1)

            elif node.type in [JumpType.Ladder, JumpType.Snake]:
                G.add_edge(u, node.next, weight=0)

            elif node.type == JumpType.Smoke:
                start = max(0, u - 6)
                for v in range(start, u):
                    G.add_edge(u, v, weight=2)

        return G

    def get_rolls(self):
        win_rolls = self.get_win_rolls()
        lose_rolls = self.get_lose_rolls(len(win_rolls))

        if len(win_rolls) >= len(lose_rolls):
            logger.error("found shortest path for lose rolls")

        result = []
        for i in range(len(win_rolls)):
            result += (self.players - 1) * lose_rolls[i] + win_rolls[i]

        # final result
        return result

    def get_lose_rolls(self, win_length):
        path = []
        i = 0
        while len(path) < win_length * 2:
            path.append(i + 1)
            cur = self.board[i]
            if cur.type == JumpType.End:
                break
            elif cur.type in [JumpType.Ladder, JumpType.Snake]:
                i = cur.next - 1
            elif cur.type == JumpType.Smoke:
                i -= 1
            else:
                i += 1

        return self.convert_path_to_rolls(path)

    def get_win_rolls(self):
        path = nx.shortest_path(self.G, 1, len(self.board), weight="weight")
        return self.convert_path_to_rolls(path)

    def convert_path_to_rolls(self, path):
        turns = []

        i = 1
        current_roll = []
        while i < len(path):
            prev_node = self.board[path[i - 1] - 1]
            if prev_node.type == JumpType.Normal:
                turns.append(current_roll)
                current_roll = [path[i] - path[i - 1]]
            elif prev_node.type in [JumpType.Ladder, JumpType.Snake]:
                pass
            elif prev_node.type in [JumpType.Smoke, JumpType.Mirror]:
                current_roll.append(path[i] - path[i - 1])

            i += 1
        turns.append(current_roll)

        return [t for t in turns if t]
