def greedy_partition(nums):
    """
    Simple greedy approach for partition problem.
    Sorts elements and assigns them to the subset with smaller sum.
    
    Args:
        nums: List of integers to partition
        
    Returns:
        A tuple ((subset1, subset2), difference, iterations) where iterations
        counts the number of assignment decisions made
    """
    nums_sorted = sorted(nums, reverse=True)
    s1, s2 = [], []
    sum1, sum2 = 0, 0
    iterations = 0  # Count assignment decisions
    
    for num in nums_sorted:
        iterations += 1
        if sum1 <= sum2:
            s1.append(num)
            sum1 += num
        else:
            s2.append(num)
            sum2 += num
            
    return (s1, s2), abs(sum1 - sum2), iterations


