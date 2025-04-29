# -*- coding: utf-8 -*-
"""
Brute-force optimizat cu backtracking + pruning.
Returnează și numărul de apeluri recursive (aprox. numărul de noduri vizitate în arborele de backtrack).
"""
def optimized_brute_force_partition(nums):
    n = len(nums)
    total = sum(nums)
    target = total // 2
    best_diff = float('inf')
    best_parts = ([], [])
    iterations = 0

    def backtrack(i, s1, s2, sum1, sum2):
        nonlocal best_diff, best_parts, iterations
        iterations += 1

        # Pruning: dacă oricare sumă depășește target, tăiem
        if sum1 > target or sum2 > target:
            return

        # Dacă am alocat toate elementele
        if i == n:
            diff = abs(sum1 - sum2)
            if diff < best_diff:
                best_diff = diff
                best_parts = (s1[:], s2[:])
            return

        # Atribuie nums[i] în s1
        s1.append(nums[i])
        backtrack(i + 1, s1, s2, sum1 + nums[i], sum2)
        s1.pop()

        # Atribuie nums[i] în s2
        s2.append(nums[i])
        backtrack(i + 1, s1, s2, sum1, sum2 + nums[i])
        s2.pop()

    backtrack(0, [], [], 0, 0)
    return best_parts, best_diff, iterations
