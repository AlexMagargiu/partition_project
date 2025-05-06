import heapq

def solve(arr):
    """
    Implementare greedy optimizată pentru Partition Problem folosind heap
    
    Algoritm:
    1. Folosim două heap-uri pentru a menține sumele și conținutul celor două subseturi
    2. Heap-urile sunt minim, așa că folosim negații pentru a transforma în max-heap
    3. La fiecare pas, extragem subset-ul cu suma mai mică și adăugăm elementul curent
    
    Args:
        arr: Lista de numere care trebuie împărțită
        
    Returns:
        subset1: Primul subset
        subset2: Al doilea subset
        iterations: Numărul de iterații efectuate
    """
    iterations = 0
    
    # Sortăm array-ul în ordine descrescătoare pentru a prelucra
    # întâi numerele mari (îmbunătățește calitatea soluției)
    sorted_arr = sorted(arr, reverse=True)
    
    # Inițializăm cele două heap-uri cu sumele negative pentru a avea max-heap
    heap1 = [0]  # (suma negativă, lista de elemente)
    heap2 = [0]  # (suma negativă, lista de elemente)
    elements1 = []
    elements2 = []
    
    for num in sorted_arr:
        iterations += 1
        
        # Extragem sumele actuale ale subseturilor (negate)
        sum1 = -heap1[0]
        sum2 = -heap2[0]
        
        # Adăugăm elementul în subset-ul cu suma mai mică
        if sum1 <= sum2:
            elements1.append(num)
            heapq.heapreplace(heap1, -(sum1 + num))
        else:
            elements2.append(num)
            heapq.heapreplace(heap2, -(sum2 + num))
    
    return elements1, elements2, iterations