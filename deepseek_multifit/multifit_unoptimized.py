def solve(arr):
    # Sortăm elementele în ordine descrescătoare
    sorted_arr = sorted(arr, reverse=True)
    subset1 = []
    subset2 = []
    sum1 = 0
    sum2 = 0
    iterations = 0  # Contor pentru iterații (opțional)
    
    # Distribuim elementele în cele două subseturi
    for num in sorted_arr:
        iterations += 1
        if sum1 <= sum2:
            subset1.append(num)
            sum1 += num
        else:
            subset2.append(num)
            sum2 += num
    
    return subset1, subset2, iterations