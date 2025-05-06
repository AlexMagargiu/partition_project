def solve(arr):
    # 1. Sortare descrescătoare in-place cu Timsort optimizat
    arr_sorted = sorted(arr, reverse=True)  # O(n log n)
    
    subset1, subset2 = [], []
    sum1 = sum2 = 0
    diff_cache = {}  # Memoizare diferențe parțiale (opțională)
    
    # 2. Distribuire strategică cu minimizare diferență
    for num in arr_sorted:  # O(n)
        # Calculează diferența potențială pentru ambele opțiuni
        temp_diff1 = abs((sum1 + num) - sum2)
        temp_diff2 = abs(sum1 - (sum2 + num))
        
        # Alege opțiunea cu diferența minimă
        if temp_diff1 <= temp_diff2:
            subset1.append(num)
            sum1 += num
        else:
            subset2.append(num)
            sum2 += num
    
    return subset1, subset2, len(arr_sorted)