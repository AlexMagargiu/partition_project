from bisect import insort

def solve(arr):
    if len(arr) > 1000:  # Limit input size
        return [], arr, 0
    
    pairs = [(num, i) for i, num in enumerate(arr)]
    pairs.sort(reverse=True)
    different_subsets = []
    iterations = 0
    
    while len(pairs) > 1:
        iterations += 1
        (a_val, a_idx), (b_val, b_idx) = pairs.pop(0), pairs.pop(0)
        different_subsets.append((a_idx, b_idx))
        diff = abs(a_val - b_val)
        new_idx = a_idx if a_val > b_val else b_idx
        insort(pairs, (diff, new_idx), key=lambda x: -x[0])
    
    subset = [0] * len(arr)
    stack = []
    for i in range(len(arr)):
        if subset[i] == 0:
            stack.append((i, 1))
    
    conflict = False
    while stack:
        idx, s = stack.pop()
        if subset[idx] != 0:
            if subset[idx] != s:
                conflict = True
                break
            continue
        subset[idx] = s
        for a, b in different_subsets:
            if a == idx:
                stack.append((b, -s))
            elif b == idx:
                stack.append((a, -s))
    
    if conflict:
        subset1, subset2 = [], []
        sum1, sum2 = 0, 0
        for num in sorted(arr, reverse=True):
            if sum1 <= sum2:
                subset1.append(num)
                sum1 += num
            else:
                subset2.append(num)
                sum2 += num
        return subset1, subset2, iterations
    
    subset1 = [arr[i] for i in range(len(arr)) if subset[i] == 1]
    subset2 = [arr[i] for i in range(len(arr)) if subset[i] == -1]
    return subset1, subset2, iterations