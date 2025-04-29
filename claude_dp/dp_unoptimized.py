def dp_partition(nums):
    """
    Dynamic Programming solution for the partition problem.
    Uses a 2D DP table to track possible sums.
    
    Args:
        nums: List of integers to partition
        
    Returns:
        A tuple ((subset1, subset2), difference, iterations) where difference is the 
        minimal difference between the two subset sums and iterations is the count of
        DP table cells filled (approximate iteration count)
    """
    n = len(nums)
    total = sum(nums)
    target = total // 2
    
    # Create DP table: dp[i][j] = True if a subset of nums[0...i-1] can sum to j
    dp = [[False for _ in range(target + 1)] for _ in range(n + 1)]
    
    # Empty subset sums to 0
    for i in range(n + 1):
        dp[i][0] = True
    
    # Count iterations as DP cells filled
    iterations = 0
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            iterations += 1
            # If we can form sum j without including nums[i-1]
            if dp[i-1][j]:
                dp[i][j] = True
            # If we can form sum j by including nums[i-1]
            elif j >= nums[i-1] and dp[i-1][j - nums[i-1]]:
                dp[i][j] = True
    
    # Find the largest sum closest to target
    closest_sum = 0
    for j in range(target, -1, -1):
        if dp[n][j]:
            closest_sum = j
            break
    
    diff = total - 2 * closest_sum
    
    # Reconstruct the subsets
    s1 = []
    s2 = []
    i, j = n, closest_sum
    
    # Backtrack to find elements in subset1
    while i > 0 and j > 0:
        if not dp[i-1][j]:  # This item must be included
            s1.append(nums[i-1])
            j -= nums[i-1]
        i -= 1
    
    # Remaining elements go to subset2
    s2 = [num for num in nums if num not in s1]
    
    return (s1, s2), diff, iterations
