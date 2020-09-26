import logging
import json
# import nltk
# try:
#     nltk.download("wordnet")
# except:
#     pass
# from nltk.corpus import wordnet
import wordninja
from english_words import english_words_set
from flask import request, jsonify
from collections import deque
from codeitsuisse import app
import random

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
    return jsonify(results)

def decrypt(message):
    start, end, count = getShift(message)
    # print(start,end)
    if count == 0:
        return message, 0
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
        cand_count = 0
        dist_to_message = None
        while tmp not in reachable:
            reachable[tmp] = True
            cand_count += 1
            shift = sum([ord(c) for c in tmp[start:end]]) + count
            tmp = ''.join([chr((ord(c)-97 + shift) % 26 + 97) for c in tmp])
            if tmp == message:
                dist_to_message = cand_count
                break
        if dist_to_message is not None:
            candidates_filtered[cand] = dist_to_message
    # logging.info(f"{candidates_filtered}")
    # l = [cand for cand in candidates_filtered]
    # if len(l) == 0:
    #     return message, 0
    # rng = random.randint(0,len(l)-1)
    # return l[rng], candidates_filtered[l[rng]]
    # print(len(candidates_filtered),candidates_filtered)

    # get decrypted message
    best_count = 0
    best_cand = None
    THRESHOLD = 0.45
    for cand, count in candidates_filtered.items():
        n = len(cand)
        p = int(THRESHOLD*n)
        curr_count = wordBreak2(cand[:p])
        if curr_count > best_count:
            best_count = curr_count
            best_cand = cand
            
    # get word breaks
    if best_cand is not None:
        try:
            toReturn = ' '.join(wordninja.split(best_cand))
            return toReturn, candidates_filtered[best_cand]
        except:
            return best_cand, candidates_filtered[best_cand]
    try:
        toReturn = ' '.join(wordninja.split(message))
        return toReturn, 0
    except:
        return message, 0

    # best_cand = None
    # best_count = 0
    # enc_count = 0
    # for cand, count in candidates_filtered.items():
    #     try:
    #         cand_split = wordninja.split(cand)
    #         num_eng = 0
    #         for word in cand_split:
    #             if len(word) > 3:
    #                 num_eng += 1
    #         if num_eng > len(cand_split) // 2:
    #             return ' '.join(cand_split), count
    #         if num_eng > best_count:
    #             best_count = num_eng
    #             best_cand = ' '.join(cand_split)
    #             enc_count = count
    #     except:
    #         pass
    # if best_cand is not None:
    #     return best_cand, enc_count
    # try:
    #     toReturn = ' '.join(wordninja.split(message))
    #     return toReturn, 0
    # except:
    #     return message, 0


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
    count = 0
    for i in range(len(s)-1,-1,-1):
        for j in range(len(s)):
            if i == j:
                dp[i][j] = False
            elif i > j:
                continue
            elif s[i:j+1] in english_words_set:
                dp[i][j] = True
                count += 1
            else:
                for k in range(i,j+1):
                    if dp[i][k] and dp[k+1][j]:
                        dp[i][j] = True
                        count += 1
                        break
    return count

def breakMessage(fringe, fringes, s):
    print(s)
    if s == '':
        fringes.append(fringe)
        return
    
    for i in range(1,len(s)):
        if s[:i] in english_words_set:
            print(s[:i])
            breakMessage(fringe + [s[:i]], fringes, s[i:])
        else:
            break

    


# d = enchant.Dict("en_US")
# print(decrypt("oxzbzxofpxkbkdifpemxifkaoljb"))
# print(getShift('abcdefghh'))