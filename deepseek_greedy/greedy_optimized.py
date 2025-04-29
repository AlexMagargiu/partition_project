def greedy_partition_optimized(nums):
    """
    Optimized greedy approach that starts with a simple partition
    then improves it through pairwise swaps.
    
    Args:
        nums: List of integers to partition
        
    Returns:
        A tuple ((subset1, subset2), difference, iterations) where iterations
        counts the number of operations performed including initial assignments
        and swap evaluations
    """
    # Initial greedy partition
    nums_sorted = sorted(nums, reverse=True)
    s1, s2 = [], []
    sum1, sum2 = 0, 0
    iterations = 0  # Count operations
    
    # Initial assignment phase
    for num in nums_sorted:
        iterations += 1
        if sum1 <= sum2:
            s1.append(num)
            sum1 += num
        else:
            s2.append(num)
            sum2 += num
    current_diff = abs(sum1 - sum2)
    
    # Pairwise swap improvement
    improved = True
    while improved:
        improved = False
        best_diff = current_diff
        best_swap = None
        
        # Check all possible swaps
        for i in range(len(s1)):
            a = s1[i]
            for j in range(len(s2)):
                iterations += 1  # Count each swap evaluation
                b = s2[j]
                new_sum1 = sum1 - a + b
                new_sum2 = sum2 - b + a
                new_diff = abs(new_sum1 - new_sum2)
                if new_diff < best_diff:
                    best_diff = new_diff
                    best_swap = (i, j)
                    
        # Apply the best swap
        if best_swap:
            iterations += 1  # Count the swap operation
            i, j = best_swap
            a, b = s1[i], s2[j]
            s1[i], s2[j] = b, a
            sum1 = sum1 - a + b
            sum2 = sum2 - b + a
            current_diff = best_diff
            improved = True
            
    return (s1, s2), current_diff, iterations