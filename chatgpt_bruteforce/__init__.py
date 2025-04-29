# Package init — expunem direct cele două funcții
from .bruteforce_unoptimized import brute_force_partition
from .bruteforce_optimized   import optimized_brute_force_partition

__all__ = [
    "brute_force_partition",
    "optimized_brute_force_partition",
]
