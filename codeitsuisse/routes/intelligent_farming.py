import json
import logging
from collections import Counter

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/intelligent-farming', methods=['POST'])
def evaluate_intelligent_farming():
    data = request.get_json()
    logging.info(f"intelligent-farming data: {data}")

    arr = data["list"]
    for item in arr:
        gene_seq = item["geneSequence"]
        item["geneSequence"] = intelligent_farming(gene_seq)

    logging.info(f"intelligent-farming result: {data}")
    return jsonify(data)


def intelligent_farming(gene_seq):
    """
    https://cis2020-intelligent-farming-2.herokuapp.com/

    :param gene_seq: string of charactersj
    :rtype: dict
    """

    count = Counter(gene_seq)

    result = []

    # greedy solution

    # greedily get all "ACGT" pairs which gives +10 points.
    # prefer ACGT over CC
    four_pair = "ACGT"
    num_four_pair = 0
    while all(count.get(ch, 0) > 0 for ch in four_pair):
        for ch in four_pair:
            count[ch] -= 1
        num_four_pair += 1
    result += ["ACGT"] * num_four_pair

    # if there is lone ACGT and one C extra, better to form CC,
    if len(result) % 2 != 0 and count.get("C", 0) % 2 != 0:
        result.pop()
        for ch in four_pair:
            count[ch] += 1

    # greedily get all "CC" pairs which gives +25 points.
    num_c = count.get("C", 0)
    quotient, remainder = divmod(num_c, 2)
    count["C"] = remainder
    result += ["CC"] * quotient


    for key, value in count.items():
        if value > 0 and key != "A":
            result += [key] * value

    # greedily disables all "AAA" if possible with the remaining letters
    for i, word in enumerate(result):
        num_a = count.get("A", 0)
        if num_a <= 0:
            break

        # can only use 1 "A"
        if word == "ACGT":
            to_be_used = 1
        else:
            to_be_used = min(2, num_a)

        result[i] = "A" * to_be_used + word
        count["A"] -= to_be_used

    # place remaining As at the back
    result += ["A"] * count.get("A", 0)

    return ''.join(result)


def get_dri_score(gene_seq):
    score = 0
    i = 0
    while i < len(gene_seq):
        if gene_seq[i:i + 3] == "AAA":
            score -= 10
            i += 3
        elif gene_seq[i:i + 4] == "ACGT":
            score += 15
            i += 4
        elif gene_seq[i:i + 2] == "CC":
            score += 25
            i += 2
        else:
            i += 1
    return score
