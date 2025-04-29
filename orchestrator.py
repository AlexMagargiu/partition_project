#!/usr/bin/env python3
import argparse
import random
import time
import matplotlib.pyplot as plt

# importuri brute-force
from chatgpt_bruteforce.bruteforce_unoptimized import brute_force_partition
from chatgpt_bruteforce.bruteforce_optimized   import optimized_brute_force_partition
# importuri DP
from claude_dp.dp_unoptimized  import dp_partition
from claude_dp.dp_optimized    import dp_partition_optimized
# importuri greedy
from deepseek_greedy.greedy_unoptimized import greedy_partition
from deepseek_greedy.greedy_optimized   import greedy_partition_optimized
# importuri meet-in-the-middle
from gemini_meet_middle.meetmiddle_unoptimized import mitm_partition
from gemini_meet_middle.meetmiddle_optimized   import mitm_partition_optimized

""" ("Brute_Unopt",   brute_force_partition),
("Brute_Opt",     optimized_brute_force_partition), """
""" ("DP_Unopt",      dp_partition),
("DP_Opt",        dp_partition_optimized), """
""" ("Greedy_Unopt",  greedy_partition),
("Greedy_Opt",    greedy_partition_optimized), """
""" ("MITM_Unopt",    mitm_partition),
("MITM_Opt",      mitm_partition_optimized) """

ALL_ALGOS = [
("Brute_Unopt",   brute_force_partition),
("Brute_Opt",     optimized_brute_force_partition),
("DP_Unopt",      dp_partition),
("DP_Opt",        dp_partition_optimized),
("Greedy_Unopt",  greedy_partition),
("Greedy_Opt",    greedy_partition_optimized),
("MITM_Unopt",    mitm_partition),
("MITM_Opt",      mitm_partition_optimized),
]

def run_all(interactive):
    # Using hardcoded list instead of generating random numbers
    nums = [19, 51, 69, 61, 37, 42, 79, 95, 100, 7, 65, 43, 29, 75, 41, 89, 33, 83, 61, 11, 37, 55, 47, 1, 74]
    n = len(nums)
    print(f"\nInstanță ({n} elem): {nums}\n")

    names, iters, times = [], [], []

    if interactive:
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,6))
        ax1.set_title("Număr iterații până la soluție")
        ax2.set_title("Timp de execuție (s)")
        plt.tight_layout()
        plt.show()

    for name, func in ALL_ALGOS:
        print(f"→ Rulez {name}...")
        t0 = time.time()
        partition, diff, iteration_count = func(nums)
        dt = time.time() - t0
        print(f"   Solution: S1={partition[0]}, S2={partition[1]}")
        print(f"   Diff={diff}, Iterations={iteration_count}, Time={dt:.4f}s\n")

        # stocăm pentru grafic
        names.append(name)
        iters.append(iteration_count)
        times.append(dt)

        if interactive:
            ax1.clear(); ax2.clear()
            ax1.bar(names, iters)
            ax1.set_title("Număr iterații până la soluție")
            ax2.bar(names, times)
            ax2.set_title("Timp de execuție (s)")
            plt.draw()
            plt.pause(0.1)

    # sumar tabelar
    print("=== SUMMARY ===")
    print(f"{'Algo':<15}{'Iters':<10}{'Time(s)':<10}")
    for nm, itc, tm in zip(names, iters, times):
        print(f"{nm:<15}{itc:<10}{tm:<10.4f}")

    if interactive:
        plt.ioff()
        plt.show()
    else:
        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(8,6))
        ax1.bar(names, iters); ax1.set_title("Număr iterații până la soluție")
        ax2.bar(names, times); ax2.set_title("Timp de execuție (s)")
        plt.tight_layout()
        plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Chart live pe măsură ce rulează fiecare algoritm"
    )
    args = p.parse_args()
    run_all(args.interactive)

if __name__ == "__main__":
    main()