def dp_partition_optimized(nums):
    """
    Optimized Dynamic Programming solution that uses a 1D DP array.
    
    Args:
        nums: List of integers to partition
        
    Returns:
        A tuple ((subset1, subset2), difference, iterations) where difference is the 
        minimal difference between the two subset sums and iterations is the count of
        DP operations
    """
    n = len(nums)
    total = sum(nums)
    target = total // 2
    
    # 1D DP array
    dp = [False] * (target + 1)
    dp[0] = True
    
    # Track which item was last used to achieve each sum
    parent = [None] * (target + 1)
    
    # Count iterations
    iterations = 0
    
    # Fill the DP array
    for i in range(n):
        for j in range(target, nums[i] - 1, -1):
            iterations += 1
            if dp[j - nums[i]]:
                dp[j] = True
                parent[j] = i  # Store the item that helped achieve this sum
    
    # Find the largest possible sum
    closest_sum = 0
    for j in range(target, -1, -1):
        if dp[j]:
            closest_sum = j
            break
    
    # Reconstruct the subsets
    s1 = []
    marked = [False] * n
    
    # Simple reconstruction using parent array
    j = closest_sum
    while j > 0:
        item_idx = parent[j]
        if item_idx is not None:
            s1.append(nums[item_idx])
            marked[item_idx] = True
            j -= nums[item_idx]
    
    # Remaining elements go to s2
    s2 = [nums[i] for i in range(n) if not marked[i]]
    
    diff = total - 2 * closest_sum
    return (s1, s2), diff, iterations