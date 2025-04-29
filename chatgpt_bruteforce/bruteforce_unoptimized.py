# -*- coding: utf-8 -*-
"""
Brute-force simplu: O(2^n · n), returnează și numărul de iterații (măsurat ca numărul de subset‐uri testate).
"""
def brute_force_partition(nums):
    n = len(nums)
    best_diff = float('inf')
    best_parts = ([], [])
    iterations = 0

    # Enumerăm toate cele 2^n submulțimi
    for mask in range(1 << n):
        iterations += 1
        s1, s2 = [], []
        for i in range(n):
            if mask & (1 << i):
                s1.append(nums[i])
            else:
                s2.append(nums[i])
        diff = abs(sum(s1) - sum(s2))
        if diff < best_diff:
            best_diff = diff
            best_parts = (s1, s2)

    return best_parts, best_diff, iterations
