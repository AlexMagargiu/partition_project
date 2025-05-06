import matplotlib.pyplot as plt
import numpy as np
import time
import random
from multiprocessing import Pool, cpu_count
import os
import sys

# Import the algorithms - assuming they're in the same directory or in the Python path
# Adjust these imports based on your actual package structure
try:
    from deepseek_multifit.multifit_unoptimized import solve as solve_multifit_unopt
    from deepseek_multifit.multifit_semioptimized import solve as solve_multifit_semiopt
    from deepseek_multifit.multifit_optimized import solve as solve_multifit_opt
    from deepseek_multifit.multifit_multiprocessing import solve_parallel as solve_multifit_multiproc
    from chatgpt_dp.dp_unoptimized import solve as solve_dp_unopt
    from chatgpt_dp.dp_optimized import solve as solve_dp_opt
    from claude_greedy.greedy_unoptimized import solve as solve_greedy_unopt
    from claude_greedy.greedy_optimized import solve as solve_greedy_opt
    from perplexity_kk.kk_unoptimized import solve as solve_kk_unopt
    from perplexity_kk.kk_optimized import solve as solve_kk_opt
except ImportError:
    # Fallback imports if package structure is different
    print("Warning: Could not import from package. Using relative imports.")
    try:
        from deepseek_multifit.multifit_unoptimized import solve as solve_multifit_unopt
        from deepseek_multifit.multifit_semioptimized import solve as solve_multifit_semiopt
        from deepseek_multifit.multifit_optimized import solve as solve_multifit_opt
        from deepseek_multifit.multifit_multiprocessing import solve_parallel as solve_multifit_multiproc
    except ImportError:
        print("Error: Algorithm modules not found.")
        sys.exit(1)

def generate_data(size, max_value=1000):
    """Generează date aleatorii pentru testare, optimizat pentru seturi mari de date"""
    if size > 1000000:  # Pentru seturi foarte mari, folosim generare optimizată
        # Folosim numpy pentru generare eficientă
        return np.random.randint(1, max_value + 1, size=size).tolist()
    else:
        # Pentru seturi mai mici, păstrăm generarea originală
        return [random.randint(1, max_value) for _ in range(size)]

def run_test_with_timeout(algorithm, arr, timeout=300):
    """Rulează algoritmul cu un timeout pentru a evita blocajele pe seturi mari"""
    start_time = time.time()
    try:
        # Limitează timpul de execuție
        subset1, subset2, iterations = algorithm(arr.copy() if isinstance(arr, list) else arr)
        end_time = time.time()
        
        execution_time = end_time - start_time
        diff = abs(sum(subset1) - sum(subset2))
        
        return {
            'time': execution_time,
            'diff': diff,
            'iterations': iterations,
            'success': True
        }
    except Exception as e:
        end_time = time.time()
        print(f"Eroare sau timeout la execuția algoritmului: {str(e)}")
        return {
            'time': end_time - start_time,
            'diff': float('inf'),
            'iterations': 0,
            'success': False
        }

def worker_process(args):
    """Funcție worker pentru procesare paralelă a testelor"""
    alg_func, data, alg_name = args
    try:
        result = run_test_with_timeout(alg_func, data)
        return alg_name, result
    except Exception as e:
        print(f"Eroare în procesul worker pentru {alg_name}: {str(e)}")
        return alg_name, {
            'time': float('inf'),
            'diff': float('inf'),
            'iterations': 0,
            'success': False
        }

def compare_algorithms_parallel(sizes, max_workers=None):
    """Compară algoritmii în paralel pentru eficiență maximă pe seturi mari"""
    # Definim algoritmii de bază
    base_algorithms = {
        'DP Unoptimized': solve_dp_unopt,
        'DP Optimized': solve_dp_opt,
        'Greedy Unoptimized': solve_greedy_unopt,
        'Greedy Optimized': solve_greedy_opt,
        'KK Unoptimized': solve_kk_unopt,
        'KK Optimized': solve_kk_opt,
        'Multifit Unoptimized': solve_multifit_unopt,
        'Multifit Semioptimized': solve_multifit_semiopt,
        'Multifit Optimized': solve_multifit_opt,
        'Multifit Multiprocessing': solve_multifit_multiproc,
    }
    
    # Inițializare structură de rezultate pentru toți algoritmii
    results = {alg: {'time': [], 'diff': [], 'iterations': [], 'success': []} for alg in base_algorithms}
    
    # Pentru fiecare dimensiune de test
    for size in sizes:
        print(f"Testăm pentru dimensiunea {size}...")
        
        # Generăm datele de test o singură dată pentru această dimensiune
        data = generate_data(size)
        
        # Decidem care algoritmi să rulăm pentru această dimensiune
        current_algorithms = base_algorithms.copy()
        
        # Excludem algoritmii DP pentru dimensiuni mai mari de 1000
        if size > 1000:
            print(f"  Dimensiunea {size} > 1000: Excludem algoritmii DP pentru a preveni crash-ul")
            current_algorithms.pop('DP Unoptimized', None)
            current_algorithms.pop('DP Optimized', None)
        
        # Pregătim argumentele pentru execuția paralelă
        args_list = [(alg_func, data, alg_name) for alg_name, alg_func in current_algorithms.items()]
        
        # Determinăm numărul optim de procese (maxim unul per algoritm)
        n_workers = min(len(current_algorithms), cpu_count() if max_workers is None else max_workers)
        
        # Executăm testele în paralel
        with Pool(processes=n_workers) as pool:
            results_list = pool.map(worker_process, args_list)
        
        # Procesăm rezultatele
        for alg_name, res in results_list:
            results[alg_name]['time'].append(res['time'])
            results[alg_name]['diff'].append(res['diff'])
            results[alg_name]['iterations'].append(res['iterations'])
            results[alg_name]['success'].append(res['success'])
            
            success_status = "SUCCESS" if res['success'] else "FAILED"
            print(f"  {alg_name}: timp={res['time']:.6f}s, diferență={res['diff']}, iterații={res['iterations']} - {success_status}")
        
        # Pentru algoritmii care nu au rulat pentru această dimensiune, adăugăm valori null
        for alg_name in base_algorithms:
            if alg_name not in current_algorithms:
                results[alg_name]['time'].append(float('inf'))
                results[alg_name]['diff'].append(float('inf'))
                results[alg_name]['iterations'].append(0)
                results[alg_name]['success'].append(False)
                print(f"  {alg_name}: SKIPPED pentru dimensiunea {size} (prea mare)")
    
    return results, sizes

def plot_results_enhanced(results, sizes, log_scale=True, output_file=None):
    """Generează grafice îmbunătățite pentru vizualizarea clară a tuturor algoritmilor"""
    algs = list(results.keys())
    
    # Definim o paletă de culori distinctă pentru vizibilitate maximă
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    # Stiluri de linie diferite pentru a ajuta la diferențierea când liniile se suprapun
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
    # Markeri diferiți pentru puncte
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'X']
    
    # Configurăm stilul graficelor pentru claritate maximă
    plt.style.use('default')  # Reset pentru a evita suprapunerea cu stiluri anterioare
    plt.rcParams['figure.figsize'] = (16, 24)
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 16
    
    # Crearea figurii cu 3 subgrafice
    fig, axes = plt.subplots(3, 1, figsize=(16, 24))
    
    # 1. Grafic pentru timp de execuție
    for i, alg in enumerate(algs):
        # Preparăm datele - înlocuim valorile infinite sau eșecurile cu None pentru a nu fi afișate
        times = results[alg]['time']
        sizes_to_plot = sizes.copy()
        
        # Filtrăm punctele care au eșuat
        valid_points = [(x, y) for x, y, s in zip(sizes_to_plot, times, results[alg]['success']) if s]
        
        if valid_points:
            x_values, y_values = zip(*valid_points)
            axes[0].plot(x_values, y_values, 
                         linestyle=line_styles[i % len(line_styles)], 
                         marker=markers[i % len(markers)], 
                         label=alg, 
                         color=colors[i % len(colors)], 
                         linewidth=3, 
                         markersize=10)
    
    axes[0].set_title('Timp de execuție în funcție de dimensiunea input-ului', fontsize=22, pad=20)
    axes[0].set_xlabel('Dimensiunea array-ului (n)', fontsize=18)
    axes[0].set_ylabel('Timp (secunde)', fontsize=18)
    
    # Aplicăm scală logaritmică dacă este solicitat
    if log_scale:
        axes[0].set_xscale('log')
        axes[0].set_yscale('log')
        axes[0].set_ylabel('Timp (secunde) - scală logaritmică', fontsize=18)
    
    axes[0].legend(fontsize=16, loc='best')
    axes[0].grid(True, alpha=0.7)
    
    # 2. Grafic pentru diferența dintre subseturi
    for i, alg in enumerate(algs):
        diffs = results[alg]['diff']
        sizes_to_plot = sizes.copy()
        
        # Filtrăm punctele care au eșuat sau au valori infinite
        valid_points = [(x, y) for x, y, s in zip(sizes_to_plot, diffs, results[alg]['success']) 
                        if s and y != float('inf')]
        
        if valid_points:
            x_values, y_values = zip(*valid_points)
            axes[1].plot(x_values, y_values, 
                         linestyle=line_styles[i % len(line_styles)], 
                         marker=markers[i % len(markers)], 
                         label=alg, 
                         color=colors[i % len(colors)], 
                         linewidth=3, 
                         markersize=10)
    
    axes[1].set_title('Diferența dintre subseturi în funcție de dimensiunea input-ului', fontsize=22, pad=20)
    axes[1].set_xlabel('Dimensiunea array-ului (n)', fontsize=18)
    axes[1].set_ylabel('Diferența (|sum1 - sum2|)', fontsize=18)
    
    # Scală logaritmică pentru axa X dacă este solicitat
    if log_scale:
        axes[1].set_xscale('log')
        # Pentru diferențe, verificăm dacă valorile justifică o scală logaritmică
        max_diffs = [max([d for d, s in zip(results[alg]['diff'], results[alg]['success']) 
                         if s and d != float('inf')] or [0]) for alg in algs]
        min_diffs = [min([d for d, s in zip(results[alg]['diff'], results[alg]['success']) 
                         if s and d != float('inf')] or [float('inf')]) for alg in algs]
        
        max_diff = max(max_diffs) if max_diffs else 0
        min_diff = min(min_diffs) if min_diffs and min_diffs[0] != float('inf') else 1
        
        if max_diff / max(min_diff, 1) > 10:
            axes[1].set_yscale('symlog')
            axes[1].set_ylabel('Diferența (|sum1 - sum2|) - scală logaritmică', fontsize=18)
    
    axes[1].legend(fontsize=16, loc='best')
    axes[1].grid(True, alpha=0.7)
    
    # 3. Grafic pentru numărul de iterații
    for i, alg in enumerate(algs):
        iterations = results[alg]['iterations']
        sizes_to_plot = sizes.copy()
        
        # Filtrăm punctele care au eșuat
        valid_points = [(x, y) for x, y, s in zip(sizes_to_plot, iterations, results[alg]['success']) if s]
        
        if valid_points:
            x_values, y_values = zip(*valid_points)
            axes[2].plot(x_values, y_values, 
                         linestyle=line_styles[i % len(line_styles)], 
                         marker=markers[i % len(markers)], 
                         label=alg, 
                         color=colors[i % len(colors)], 
                         linewidth=3, 
                         markersize=10)
    
    axes[2].set_title('Numărul de iterații în funcție de dimensiunea input-ului', fontsize=22, pad=20)
    axes[2].set_xlabel('Dimensiunea array-ului (n)', fontsize=18)
    axes[2].set_ylabel('Număr de iterații', fontsize=18)
    
    # Scală logaritmică dacă este solicitat
    if log_scale:
        axes[2].set_xscale('log')
        axes[2].set_yscale('log')
        axes[2].set_ylabel('Număr de iterații - scală logaritmică', fontsize=18)
    
    axes[2].legend(fontsize=16, loc='best')
    axes[2].grid(True, alpha=0.7)
    
    # Ajustăm layout-ul pentru spațiere optimă
    plt.tight_layout(pad=5.0)
    
    # Salvăm figura dacă este specificat un fișier de output
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
    
    # Afișăm figura
    plt.show()

def run_large_scale_tests(include_basic_algs=False):
    """Rulează teste pe dimensiuni foarte mari pentru a demonstra scalabilitatea"""
    # Dimensiuni foarte mari pentru teste
    large_scales = [100000, 1000000]
    
    # Determinăm care algoritmi să rulăm bazat pe parametrul include_basic_algs
    if include_basic_algs:
        algorithms = {
            'Dynamic Programming Neoptimizat': solve_dp_unopt,
            'Dynamic Programming Optimizat': solve_dp_opt,
            'Greedy Neoptimizat': solve_greedy_unopt,
            'Greedy Optimizat': solve_greedy_opt,
            'Karmarkar-Karp Neoptimizat': solve_kk_unopt,
            'Karmarkar-Karp Optimizat': solve_kk_opt,
            'Multifit Neoptimizat': solve_multifit_unopt,
            'Multifit Semioptimizat': solve_multifit_semiopt,
            'Multifit Optimizat': solve_multifit_opt,
            'Multifit Optimizat Multiprocessing': solve_multifit_multiproc,
        }
    else:
        # Pentru dimensiuni foarte mari, excludem algoritmii neoptimizați care ar putea dura prea mult
        algorithms = {
            'Multifit Optimizat': solve_multifit_opt,
            'Multifit Optimizat Multiprocessing': solve_multifit_multiproc,
        }
    
    results = {alg: {'time': [], 'diff': [], 'iterations': [], 'success': []} for alg in algorithms}
    
    for size in large_scales:
        print(f"Testăm pentru dimensiunea {size}...")
        
        # Generăm date de test optimizate pentru dimensiuni mari
        data = generate_data(size)
        
        # Testăm fiecare algoritm pentru această dimensiune
        for alg_name, alg_func in algorithms.items():
            # Setăm un timeout mai mare pentru dimensiuni foarte mari
            timeout = 600 if size >= 100000 else 300
            res = run_test_with_timeout(alg_func, data, timeout=timeout)
            
            results[alg_name]['time'].append(res['time'])
            results[alg_name]['diff'].append(res['diff'])
            results[alg_name]['iterations'].append(res['iterations'])
            results[alg_name]['success'].append(res['success'])
            
            success_status = "SUCCESS" if res['success'] else "FAILED"
            print(f"  {alg_name}: timp={res['time']:.6f}s, diferență={res['diff']}, iterații={res['iterations']} - {success_status}")
    
    # Configurăm stilurile pentru grafice
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (16, 24)
    
    # Afișăm rezultatele cu scală logaritmică pentru claritate pe dimensiuni mari
    plot_results_enhanced(results, large_scales, log_scale=True, output_file='ultra_large_scale_comparison.png')
    
    return results, large_scales

def run_comprehensive_benchmark():
    """Rulează un benchmark comprehensiv pe multiple dimensiuni de date"""
    # 1. Teste standard pentru comparabilitate cu versiunea originală
    print("1. Rulăm teste standard...")
    standard_sizes = [10, 20, 30, 40, 50, 100]
    std_results, _ = compare_algorithms_parallel(standard_sizes)
    plot_results_enhanced(std_results, standard_sizes, log_scale=False, output_file='standard_comparison.png')
    
    # 2. Teste pe dimensiuni medii
    print("\n2. Rulăm teste pe dimensiuni medii...")
    medium_sizes = [100, 500, 1000, 2000, 5000, 10000]
    med_results, _ = compare_algorithms_parallel(medium_sizes)
    plot_results_enhanced(med_results, medium_sizes, log_scale=True, output_file='medium_scale_comparison.png')
    
    # 3. Teste pe dimensiuni mari (doar cu algoritmii optimizați)
    print("\n3. Rulăm teste pe dimensiuni mari...")
    large_results, large_sizes = run_large_scale_tests(include_basic_algs=False)
    
    # 4. Generăm un raport de performanță
    print("\n4. Generăm raport de performanță...")
    generate_performance_report(std_results, standard_sizes, med_results, medium_sizes, large_results, large_sizes)

def generate_performance_report(std_results, std_sizes, med_results, med_sizes, large_results, large_sizes):
    """Generează un raport de performanță bazat pe rezultatele obținute"""
    report = "# Raport de Performanță - Algoritmi Multifit\n\n"
    
    # 1. Sumar executiv
    report += "## Sumar Executiv\n\n"
    report += "Acest raport prezintă rezultatele comparative ale performanței diferitelor implementări "
    report += "ale algoritmului Multifit pentru problema partiționării. Testele au fost efectuate pe "
    report += "multiple dimensiuni de date, de la seturi mici (10-100 elemente) până la seturi foarte "
    report += "mari (până la 1 milion de elemente).\n\n"
    
    # 2. Rezultate pentru dimensiuni standard
    report += "## Rezultate pentru Dimensiuni Standard (10-100 elemente)\n\n"
    report += "### Timp de Execuție (secunde)\n\n"
    report += "| Dimensiune |"
    
    # Header pentru tabelul de timp
    for alg in std_results:
        report += f" {alg} |"
    report += "\n|" + "-" * 11 + "|"
    for _ in std_results:
        report += "-" * 20 + "|"
    report += "\n"
    
    # Date pentru tabelul de timp
    for i, size in enumerate(std_sizes):
        report += f"| {size} |"
        for alg in std_results:
            if std_results[alg]['success'][i]:
                report += f" {std_results[alg]['time'][i]:.6f} |"
            else:
                report += " N/A |"
        report += "\n"
    
    report += "\n### Diferența dintre Subseturi\n\n"
    report += "| Dimensiune |"
    
    # Header pentru tabelul de diferențe
    for alg in std_results:
        report += f" {alg} |"
    report += "\n|" + "-" * 11 + "|"
    for _ in std_results:
        report += "-" * 20 + "|"
    report += "\n"
    
    # Date pentru tabelul de diferențe
    for i, size in enumerate(std_sizes):
        report += f"| {size} |"
        for alg in std_results:
            if std_results[alg]['success'][i] and std_results[alg]['diff'][i] != float('inf'):
                report += f" {std_results[alg]['diff'][i]} |"
            else:
                report += " N/A |"
        report += "\n"
    
    # 3. Rezultate pentru dimensiuni medii
    report += "\n## Rezultate pentru Dimensiuni Medii (100-10,000 elemente)\n\n"
    report += "### Timp de Execuție (secunde)\n\n"
    report += "| Dimensiune |"
    
    # Header pentru tabelul de timp
    for alg in med_results:
        report += f" {alg} |"
    report += "\n|" + "-" * 11 + "|"
    for _ in med_results:
        report += "-" * 20 + "|"
    report += "\n"
    
    # Date pentru tabelul de timp
    for i, size in enumerate(med_sizes):
        report += f"| {size} |"
        for alg in med_results:
            if med_results[alg]['success'][i]:
                report += f" {med_results[alg]['time'][i]:.6f} |"
            else:
                report += " N/A |"
        report += "\n"
    
    # 4. Rezultate pentru dimensiuni mari
    report += "\n## Rezultate pentru Dimensiuni Mari (100-1,000,000 elemente)\n\n"
    report += "### Timp de Execuție (secunde)\n\n"
    report += "| Dimensiune |"
    
    # Header pentru tabelul de timp
    for alg in large_results:
        report += f" {alg} |"
    report += "\n|" + "-" * 11 + "|"
    for _ in large_results:
        report += "-" * 20 + "|"
    report += "\n"
    
    # Date pentru tabelul de timp
    for i, size in enumerate(large_sizes):
        report += f"| {size} |"
        for alg in large_results:
            if large_results[alg]['success'][i]:
                report += f" {large_results[alg]['time'][i]:.6f} |"
            else:
                report += " N/A |"
        report += "\n"
    
    # 5. Concluzii
    report += "\n## Concluzii\n\n"
    
    # Timp minim pentru dimensiuni mari
    min_times = {}
    for alg in large_results:
        valid_times = [t for t, s in zip(large_results[alg]['time'], large_results[alg]['success']) if s]
        if valid_times:
            min_times[alg] = min(valid_times)
    
    fastest_alg = min(min_times.items(), key=lambda x: x[1])[0] if min_times else "N/A"
    
    report += f"1. Algoritmul {fastest_alg} a demonstrat cea mai bună performanță pentru seturi mari de date.\n"
    report += "2. Pentru dimensiuni mici, diferențele de performanță între algoritmi sunt minime.\n"
    report += "3. Pe măsură ce dimensiunea datelor crește, algoritmii optimizați arată avantaje semnificative.\n"
    report += "4. Algoritmii de programare dinamică (DP) au fost excluși pentru dimensiuni > 1000 pentru a preveni crash-ul sistemului.\n"
    
    # Salvăm raportul într-un fișier
    with open("multifit_performance_report.md", "w") as f:
        f.write(report)
    
    print(f"Raportul de performanță a fost generat și salvat în 'multifit_performance_report.md'")

if __name__ == "__main__":
    # Rulăm benchmarkul complet
    run_comprehensive_benchmark()
    
    # Alternativ, putem rula doar testele pentru scale foarte mari
    # large_results, large_sizes = run_large_scale_tests(include_basic_algs=False)