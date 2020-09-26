import enchant
import logging
import json
import nltk
nltk.download("wordnet")
from nltk.corpus import wordnet
from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/bored-scribe', methods=['POST'])
def evaluate_bored_scribe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for test_case in data:
        message, count = decrypt(test_case['encryptedText'])
        results.append({"id": test_case["id"], "encryptionCount": count, "originalText": message})
    logging.info("result :{}".format(results))
    return json.dumps(results)

def decrypt(message):
    start, end, count = getShift(message)
    candidates = {}
    output = [c for c in message]
    # generate candidates
    for i in range(25):
        output = [chr((ord(c)-97 + 1) % 26 + 97) for c in output]
        candidates[''.join(output)] = True
    # print(len(candidates),candidates)
    # for each candidate, see if can reach encrypted message
    candidates_filtered = {}
    for cand in candidates:
        reachable = {}
        tmp = cand
        while tmp not in reachable:
            reachable[tmp] = True
            shift = sum([ord(c) for c in tmp[start:end]]) + count
            tmp = ''.join([chr((ord(c)-97 + shift) % 26 + 97) for c in tmp])
        if message in reachable:
            candidates_filtered[cand] = True
    # print(len(candidates_filtered),candidates_filtered)
    wordDict = enchant.Dict("en_US")
    final_cand = None
    for cand, _ in candidates_filtered.items():
        if wordBreak2(cand):
            final_cand = cand
    tmp = final_cand
    final_count = 0
    while tmp != message:
        final_count += 1
        shift = sum([ord(c) for c in tmp[start:end]]) + count
        tmp = ''.join([chr((ord(c)-97 + shift) % 26 + 97) for c in tmp])
        if tmp == message:
            break
    if final_cand is None:
        return message, 0

    else:
        return final_cand, final_count

def getShift(s):
    centers = 2*len(s)-1
    best = 0
    bestIdx = (None,None)
    count = 0
    for i in range(centers):
        if i % 2 == 0:
            start = i // 2 - 1
            end = i // 2 + 1
            curr = 1
            while start >= 0 and end < len(s):
                if s[start] == s[end]:
                    curr += 2
                    count += 1
                else:
                    break
                start -= 1
                end += 1
            if curr > best:
                best = max(best, curr)
                bestIdx = (start+1, end)
                
        else:
            start = i // 2
            end = start + 1
            curr = 0
            while start >= 0 and end < len(s):
                if s[start] == s[end]:
                    curr += 2
                    count += 1
                else:
                    break
                start -= 1
                end += 1
            if curr > best:
                best = max(best, curr)
                bestIdx = (start+1, end)
    return bestIdx[0], bestIdx[1], count

def wordBreak(s, wordDict):
    dp = [[False]*len(s) for i in range(len(s))]
    for i in range(len(s)-1,-1,-1):
        for j in range(len(s)):
            if i == j:
                dp[i][j] = True if (s[i] == 'a' or s[i] == 'i') else False
            elif i > j:
                continue
            elif wordDict.check(s[i:j+1].capitalize()):
                dp[i][j] = True
            else:
                for k in range(i,j+1):
                    if dp[i][k] and dp[k+1][j]:
                        dp[i][j] = True
                        break
    return dp[0][-1]

def wordBreak2(s):
    dp = [[False]*len(s) for i in range(len(s))]
    for i in range(len(s)-1,-1,-1):
        for j in range(len(s)):
            if i == j:
                dp[i][j] = True if (s[i] == 'a' or s[i] == 'i') else False
            elif i > j:
                continue
            elif len(wordnet.synsets(s[i:j+1])) > 0:
                dp[i][j] = True
            else:
                for k in range(i,j+1):
                    if dp[i][k] and dp[k+1][j]:
                        dp[i][j] = True
                        break
    return dp[0][-1]

# d = enchant.Dict("en_US")
# print(decrypt("oxzbzxofpxkbkdifpemxifkaoljb"))