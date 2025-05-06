from concurrent.futures import ProcessPoolExecutor
import time
from multiprocessing import cpu_count

def assign_elements(chunk):
    """Distribute elements into subsets without nested multiprocessing."""
    subset1, subset2 = [], []
    sum1, sum2 = 0, 0
    for num in sorted(chunk, reverse=True):  # Process chunks independently
        if sum1 <= sum2:
            subset1.append(num)
            sum1 += num
        else:
            subset2.append(num)
            sum2 += num
    return (subset1, subset2, sum1, sum2)

def solve_parallel(arr):
    start_time = time.time()
    arr_sorted = sorted(arr, reverse=True)
    n = len(arr_sorted)
    
    # Avoid excessive processes for small datasets
    optimal_processes = min(cpu_count(), max(1, n // 1000))
    chunk_size = max(1, n // optimal_processes)
    chunks = [arr_sorted[i*chunk_size : (i+1)*chunk_size] for i in range(optimal_processes)]
    
    with ProcessPoolExecutor(max_workers=optimal_processes) as executor:
        results = list(executor.map(assign_elements, chunks))
    
    # Combine results iteratively to minimize difference
    final_subset1, final_subset2 = [], []
    total_sum1, total_sum2 = 0, 0
    
    for subset1, subset2, sum1, sum2 in results:
        option1_diff = abs((total_sum1 + sum1) - (total_sum2 + sum2))
        option2_diff = abs((total_sum1 + sum2) - (total_sum2 + sum1))
        
        if option1_diff <= option2_diff:
            final_subset1.extend(subset1)
            final_subset2.extend(subset2)
            total_sum1 += sum1
            total_sum2 += sum2
        else:
            final_subset1.extend(subset2)
            final_subset2.extend(subset1)
            total_sum1 += sum2
            total_sum2 += sum1
    
    iterations = n
    return final_subset1, final_subset2, iterations