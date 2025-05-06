def solve(arr):
    """
    Implementare greedy neoptimizată pentru Partition Problem
    
    Algoritm:
    1. Sortează array-ul în ordine descrescătoare
    2. Ia elementele unul câte unul și adaugă-le în subset-ul cu suma mai mică
    
    Args:
        arr: Lista de numere care trebuie împărțită
        
    Returns:
        subset1: Primul subset
        subset2: Al doilea subset
        iterations: Numărul de iterații efectuate
    """
    iterations = 0
    subset1 = []
    subset2 = []
    sum1 = 0
    sum2 = 0
    
    # Sortăm array-ul în ordine descrescătoare
    sorted_arr = sorted(arr, reverse=True)
    
    # Parcurgem fiecare element și îl adăugăm în subset-ul cu suma mai mică
    for num in sorted_arr:
        iterations += 1
        if sum1 <= sum2:
            subset1.append(num)
            sum1 += num
        else:
            subset2.append(num)
            sum2 += num
    
    return subset1, subset2, iterations