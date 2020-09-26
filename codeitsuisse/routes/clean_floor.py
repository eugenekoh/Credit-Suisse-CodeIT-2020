def clean_floor(arr):
    firstNonZero = 0 if arr[0] != 0 else 1
    lastNonZero = len(arr)-1

    while lastNonZero >= 0:
        if arr[lastNonZero] != 0:
            break
        lastNonZero -= 1
    # print(firstNonZero,lastNonZero)
    moves = 0
    start = 0
    while firstNonZero < lastNonZero:
        moves += 1
        if arr[start+1] > 0:
            arr[start+1] -= 1
        elif arr[start+1] == 0:
            arr[start+1] += 1
        
    return moves

arr = [1,2,1,3,0,1]
clean_floor(arr)