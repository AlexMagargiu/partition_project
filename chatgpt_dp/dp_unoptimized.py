def solve(arr):
    total_sum = sum(arr)
    n = len(arr)
    iterations = 0

    if total_sum % 2 != 0:
        return [], arr, 0

    target = total_sum // 2
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    parent = [[-1] * (target + 1) for _ in range(n + 1)]  # Tracks indices

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        current_num = arr[i - 1]
        for j in range(1, target + 1):
            iterations += 1
            if j < current_num:
                dp[i][j] = dp[i - 1][j]
                parent[i][j] = parent[i - 1][j]
            else:
                if dp[i - 1][j] or dp[i - 1][j - current_num]:
                    dp[i][j] = True
                    if dp[i - 1][j - current_num]:
                        parent[i][j] = i - 1  # Mark inclusion of current_num
                    else:
                        parent[i][j] = parent[i - 1][j]

    if not dp[n][target]:
        return [], arr, iterations

    # Reconstruct subset1
    subset1 = []
    i, j = n, target
    while i > 0 and j > 0:
        if parent[i][j] == i - 1:
            subset1.append(arr[i - 1])
            j -= arr[i - 1]
        i -= 1

    # Verify subset1 sum
    if sum(subset1) != target:
        return [], arr, iterations

    # Build subset2 using frequency counts
    from collections import defaultdict
    freq = defaultdict(int)
    for num in arr:
        freq[num] += 1

    for num in subset1:
        if freq[num] == 0:
            return [], arr, iterations
        freq[num] -= 1

    subset2 = []
    for num in arr:
        if freq[num] > 0:
            subset2.append(num)
            freq[num] -= 1

    return subset1, subset2, iterations