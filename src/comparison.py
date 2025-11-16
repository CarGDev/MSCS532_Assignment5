"""
Performance Comparison Utilities

This module provides utilities for comparing different sorting algorithms
and analyzing their performance characteristics.
"""

import time
import random
from typing import List, Callable, Dict, Tuple, Any
from functools import wraps
import statistics


def time_function(func: Callable) -> Callable:
    """
    Decorator to measure the execution time of a function.
    
    Args:
        func: The function to time
    
    Returns:
        Wrapped function that returns (result, execution_time)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper


def generate_random_array(size: int, min_val: int = 0, max_val: int = 1000) -> List[int]:
    """Generate a random array of integers."""
    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_sorted_array(size: int, start: int = 0, step: int = 1) -> List[int]:
    """Generate a sorted array of integers."""
    return list(range(start, start + size * step, step))


def generate_reverse_sorted_array(size: int, start: int = 0, step: int = 1) -> List[int]:
    """Generate a reverse-sorted array of integers."""
    return list(range(start + (size - 1) * step, start - step, -step))


def generate_nearly_sorted_array(size: int, swap_count: int = 10) -> List[int]:
    """Generate a nearly sorted array with a few swaps."""
    arr = list(range(size))
    for _ in range(swap_count):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_array_with_duplicates(size: int, unique_count: int = 10) -> List[int]:
    """Generate an array with many duplicate values."""
    unique_values = list(range(unique_count))
    return [random.choice(unique_values) for _ in range(size)]


def benchmark_sorting_algorithm(
    sort_func: Callable[[List[Any]], Any],
    array: List[Any],
    iterations: int = 1
) -> Dict[str, float]:
    """
    Benchmark a sorting algorithm on a given array.
    
    Args:
        sort_func: The sorting function to benchmark
        array: The array to sort
        iterations: Number of iterations to run (for averaging)
    
    Returns:
        Dictionary with timing statistics
    """
    times = []
    
    for _ in range(iterations):
        # Create a fresh copy for each iteration
        arr_copy = array.copy()
        
        start_time = time.perf_counter()
        result = sort_func(arr_copy)
        end_time = time.perf_counter()
        
        # Verify the result is sorted
        sorted_arr = result if result is not None else arr_copy
        if sorted_arr != sorted(array):
            raise ValueError(f"Sorting function {sort_func.__name__} produced incorrect results")
        
        times.append(end_time - start_time)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0.0
    }


def compare_algorithms(
    algorithms: Dict[str, Callable[[List[Any]], Any]],
    array_generators: Dict[str, Callable[[int], List[Any]]],
    sizes: List[int],
    iterations: int = 3
) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Compare multiple sorting algorithms on different input distributions and sizes.
    
    Args:
        algorithms: Dictionary mapping algorithm names to sorting functions
        array_generators: Dictionary mapping distribution names to generator functions
        sizes: List of array sizes to test
        iterations: Number of iterations per test (for averaging)
    
    Returns:
        Nested dictionary: results[algorithm][distribution][size] = timing_stats
    """
    results = {}
    
    for algo_name, algo_func in algorithms.items():
        results[algo_name] = {}
        
        for dist_name, gen_func in array_generators.items():
            results[algo_name][dist_name] = {}
            
            for size in sizes:
                print(f"Testing {algo_name} on {dist_name} array of size {size}...")
                
                # Generate test array
                test_array = gen_func(size)
                
                # Benchmark
                try:
                    stats = benchmark_sorting_algorithm(algo_func, test_array, iterations)
                    results[algo_name][dist_name][size] = stats
                except Exception as e:
                    print(f"Error testing {algo_name} on {dist_name} size {size}: {e}")
                    results[algo_name][dist_name][size] = {
                        'mean': float('inf'),
                        'median': float('inf'),
                        'min': float('inf'),
                        'max': float('inf'),
                        'stdev': 0.0
                    }
    
    return results


def format_results_table(results: Dict[str, Dict[str, Dict[str, float]]]) -> str:
    """
    Format benchmark results as a readable table.
    
    Args:
        results: Results dictionary from compare_algorithms
    
    Returns:
        Formatted string table
    """
    lines = []
    lines.append("=" * 80)
    lines.append("SORTING ALGORITHM PERFORMANCE COMPARISON")
    lines.append("=" * 80)
    lines.append("")
    
    for algo_name in results:
        lines.append(f"\n{algo_name.upper()}")
        lines.append("-" * 80)
        
        for dist_name in results[algo_name]:
            lines.append(f"\n  {dist_name}:")
            lines.append(f"  {'Size':<10} {'Mean (s)':<15} {'Median (s)':<15} {'Min (s)':<15} {'Max (s)':<15}")
            lines.append("  " + "-" * 70)
            
            for size in sorted(results[algo_name][dist_name].keys()):
                stats = results[algo_name][dist_name][size]
                lines.append(
                    f"  {size:<10} {stats['mean']:<15.6f} {stats['median']:<15.6f} "
                    f"{stats['min']:<15.6f} {stats['max']:<15.6f}"
                )
    
    lines.append("\n" + "=" * 80)
    return "\n".join(lines)

