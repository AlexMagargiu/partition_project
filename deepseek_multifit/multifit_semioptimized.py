def solve(arr):
    # Copiem și sortăm descrescător în-place pentru eficiență
    sorted_arr = arr.copy()
    sorted_arr.sort(reverse=True)  # Sortare mai eficientă pe copie
    
    subset1, subset2 = [], []
    sum1 = sum2 = 0
    iterations = 0
    
    for num in sorted_arr:
        iterations += 1
        # Distribuim elementul în subsetul cu suma mai mică
        (subset1 if sum1 <= sum2 else subset2).append(num)
        # Actualizăm sumele direct pentru a evita recalcularea
        if sum1 <= sum2:
            sum1 += num
        else:
            sum2 += num
    
    return subset1, subset2, iterations