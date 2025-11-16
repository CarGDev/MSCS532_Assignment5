"""
Demonstration of Quicksort performance comparison.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.comparison import (
    generate_random_array,
    generate_sorted_array,
    generate_reverse_sorted_array,
    generate_nearly_sorted_array,
    generate_array_with_duplicates,
    compare_algorithms,
    format_results_table
)
from src.quicksort import quicksort, randomized_quicksort


def demo_performance_comparison():
    """Demonstrate performance comparison between algorithms."""
    print("=" * 80)
    print("QUICKSORT PERFORMANCE COMPARISON")
    print("=" * 80)
    
    # Define algorithms to compare
    algorithms = {
        'Deterministic Quicksort': lambda arr: quicksort(arr),
        'Randomized Quicksort': lambda arr: randomized_quicksort(arr, seed=42)
    }
    
    # Define array generators
    array_generators = {
        'Random': generate_random_array,
        'Sorted': generate_sorted_array,
        'Reverse Sorted': generate_reverse_sorted_array,
        'Nearly Sorted': lambda size: generate_nearly_sorted_array(size, swap_count=10),
        'Many Duplicates': lambda size: generate_array_with_duplicates(size, unique_count=10)
    }
    
    # Test sizes
    sizes = [100, 500, 1000, 5000]
    
    print("\nRunning performance benchmarks...")
    print("This may take a few moments...\n")
    
    # Run comparison
    results = compare_algorithms(
        algorithms=algorithms,
        array_generators=array_generators,
        sizes=sizes,
        iterations=3
    )
    
    # Print formatted results
    print(format_results_table(results))
    
    return results


def demo_specific_scenarios():
    """Demonstrate performance on specific scenarios."""
    print("\n" + "=" * 80)
    print("SPECIFIC SCENARIO ANALYSIS")
    print("=" * 80)
    
    from src.comparison import benchmark_sorting_algorithm
    
    scenarios = {
        'Small Random (100)': generate_random_array(100),
        'Medium Random (1000)': generate_random_array(1000),
        'Large Random (10000)': generate_random_array(10000),
        'Sorted (1000)': generate_sorted_array(1000),
        'Reverse Sorted (1000)': generate_reverse_sorted_array(1000),
        'Nearly Sorted (1000)': generate_nearly_sorted_array(1000, 10),
        'Many Duplicates (1000)': generate_array_with_duplicates(1000, 10)
    }
    
    algorithms = {
        'Deterministic': quicksort,
        'Randomized': lambda arr: randomized_quicksort(arr, seed=42)
    }
    
    print(f"\n{'Scenario':<30} {'Algorithm':<20} {'Mean Time (s)':<15} {'Median Time (s)':<15}")
    print("-" * 80)
    
    for scenario_name, test_array in scenarios.items():
        for algo_name, algo_func in algorithms.items():
            stats = benchmark_sorting_algorithm(algo_func, test_array, iterations=5)
            print(f"{scenario_name:<30} {algo_name:<20} {stats['mean']:<15.6f} {stats['median']:<15.6f}")


if __name__ == '__main__':
    results = demo_performance_comparison()
    demo_specific_scenarios()
    
    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE")
    print("=" * 80)

