import logging
import json

from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_clean_floor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = {"answers":{}}
    for test_num in data['tests']:
        results['answers'][test_num] = clean_floor(data['tests'][test_num]["floor"])
    logging.info("result :{}".format(results))

    return json.dumps(results)


# # ## ZHIQI ANS GREEDY
def clean_floor(nums):
    moves = 0
    left = 0
    current = 0
    right = len(nums) - 1
    # find the last part of the array that needs to be mopped
    while right >= 0:
        if nums[right] != 0:
            break
        right-=1
    while left < right:
        value = nums[left]
        i = value
        if value % 2 == 0:
            moves += (value*2)
        else:
            moves += (value*2)+1
            i += 1
        while i != 0:
            if nums[left+1] != 0:
                nums[left+1]-=1
            else:
                nums[left+1]+=1
            i -= 1
        print(nums, moves, left)
        left += 1
    if nums[right] != 0:
        value = nums[left]
        if value % 2 == 0:
            moves += (value*2)
        else:
            moves += (value*2)+1
    return moves
            
                


# # ## ZHIQI ANS SLIDING WINDOW
# def clean_floor(arr):
#     moves = 0
#     left = 0
#     current = 0
#     right = len(arr) - 1
#     # find the last part of the array that needs to be mopped
#     while right >= 0:
#         if arr[right] != 0:
#             break
#         right-=1
    
#     dirt = 0
#     for num in arr:
#         dirt += num
#     increment = True
#     while dirt > 0 and left != right:            
#         if current == right:
#             increment = False
#             if arr[right] == 0 and right != 0:
#                 right -= 1
#         if current == left:
#             increment = True
#             if arr[left] == 0 and left != len(arr)-1:
#                 left += 1
#         if increment:
#             nextPos = current + 1
#             if arr[nextPos] == 0:
#                 arr[nextPos] = 1
#                 dirt += 1
#             else:
#                 arr[nextPos] -= 1
#                 dirt -= 1
#             current += 1
#         else:
#             nextPos = current - 1
#             if arr[nextPos] == 0:
#                 arr[nextPos] = 1
#                 dirt += 1
#             else:
#                 arr[nextPos] -= 1
#                 dirt -= 1
#             current -= 1
#         moves += 1
        
#     value = arr[left]
#     if value % 2 == 0:
#         moves += (value*2)
#     else:
#         moves += (value*2)+1

#     return moves




# ## HANZHE ANS
# def clean_floor(arr):
#     firstNonZero = 0
#     lastNonZero = len(arr)-1

#     while lastNonZero >= 0:
#         if arr[lastNonZero] != 0:
#             break
#         lastNonZero -= 1
#     moves = 0
#     currPos = 0
#     direction = 0
#     while firstNonZero != lastNonZero:
#         # print(direction,currPos,firstNonZero,lastNonZero)
#         # print(arr)
#         # print("=====")
#         if direction == 0:
#             moves += (lastNonZero-currPos)
#             for i in range(currPos+1,lastNonZero+1):
#                 if arr[i] > 0:
#                     arr[i] -= 1
#                 elif arr[i] == 0:
#                     arr[i] += 1
#             currPos = lastNonZero
#             while arr[firstNonZero] == 0 and firstNonZero < lastNonZero:
#                 firstNonZero += 1
#             direction = 1
#         elif direction == 1:
#             moves += (currPos - firstNonZero)
#             for i in range(currPos-1,firstNonZero-1,-1):
#                 if arr[i] > 0:
#                     arr[i] -= 1
#                 elif arr[i] == 0:
#                     arr[i] += 1
#             currPos = firstNonZero
#             while arr[lastNonZero] == 0 and firstNonZero < lastNonZero:
#                 lastNonZero -= 1
#             direction = 0
        

#     if arr[firstNonZero] % 2 == 0:
#         moves += 2*arr[firstNonZero]
#     else:
#         moves += 2*arr[firstNonZero]+1
#     # print(moves)
#     return moves

# arr = [1,2,0,1] == 6
# arr = [1,1,0,1] == 7
# clean_floor(arr)