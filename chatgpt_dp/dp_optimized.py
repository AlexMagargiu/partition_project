def solve(arr):
    total_sum = sum(arr)
    n = len(arr)
    iterations = 0

    if total_sum % 2 != 0:
        return [], arr, 0

    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True
    parent = [-1] * (target + 1)  # Tracks the last number added to reach sum j

    for num in arr:
        for j in range(target, num - 1, -1):
            iterations += 1
            if not dp[j] and dp[j - num]:
                dp[j] = True
                parent[j] = num  # Store the value used to achieve this sum

    if not dp[target]:
        return [], arr, iterations

    # Reconstruct subset1
    subset1 = []
    current_sum = target
    while current_sum > 0:
        num = parent[current_sum]
        if num == -1:
            break  # Safety check for invalid tracking
        subset1.append(num)
        current_sum -= num

    # Verify subset1 sum matches target
    if sum(subset1) != target:
        return [], arr, iterations

    # Build subset2 using frequency counts to handle duplicates
    from collections import defaultdict
    freq = defaultdict(int)
    for num in arr:
        freq[num] += 1

    for num in subset1:
        if freq[num] == 0:
            return [], arr, iterations  # Inconsistency detected
        freq[num] -= 1

    subset2 = []
    for num in arr:
        if freq[num] > 0:
            subset2.append(num)
            freq[num] -= 1

    return subset1, subset2, iterations