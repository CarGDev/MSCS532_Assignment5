"""
Generate performance comparison plots for Quicksort algorithms.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import numpy as np
from src.comparison import (
    generate_random_array,
    generate_sorted_array,
    generate_reverse_sorted_array,
    generate_nearly_sorted_array,
    generate_array_with_duplicates,
    compare_algorithms
)
from src.quicksort import quicksort, randomized_quicksort
import os


def generate_performance_plots():
    """Generate comprehensive performance comparison plots."""
    print("Generating performance plots...")
    
    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)
    
    # Define algorithms
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
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    print("Running benchmarks (this may take a few minutes)...")
    results = compare_algorithms(
        algorithms=algorithms,
        array_generators=array_generators,
        sizes=sizes,
        iterations=3
    )
    
    # Plot 1: Line plot comparing algorithms across distributions
    print("Generating line plot...")
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Quicksort Performance Comparison', fontsize=16, fontweight='bold')
    
    distributions = ['Random', 'Sorted', 'Reverse Sorted', 'Nearly Sorted', 'Many Duplicates']
    algo_names = list(algorithms.keys())
    colors = ['#1f77b4', '#ff7f0e']
    
    for idx, dist in enumerate(distributions):
        ax = axes[idx // 3, idx % 3]
        
        for algo_idx, algo_name in enumerate(algo_names):
            if dist in results[algo_name]:
                sizes_list = sorted(results[algo_name][dist].keys())
                # Filter out infinite values
                valid_data = [(s, results[algo_name][dist][s]['mean']) 
                             for s in sizes_list 
                             if np.isfinite(results[algo_name][dist][s]['mean'])]
                if valid_data:
                    valid_sizes, valid_times = zip(*valid_data)
                    ax.plot(valid_sizes, valid_times, marker='o', label=algo_name, 
                           color=colors[algo_idx], linewidth=2, markersize=6)
        
        ax.set_xlabel('Array Size', fontsize=10)
        ax.set_ylabel('Time (seconds)', fontsize=10)
        ax.set_title(f'{dist} Distribution', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
    
    # Hide the last subplot
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('docs/quicksort_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: docs/quicksort_comparison.png")
    plt.close()
    
    # Plot 2: Bar chart comparing algorithms on sorted vs random
    print("Generating bar chart...")
    fig, ax = plt.subplots(figsize=(14, 8))
    
    distributions_to_plot = ['Random', 'Sorted', 'Reverse Sorted']
    x = np.arange(len(distributions_to_plot))
    width = 0.35
    
    # Use size 5000 for comparison
    size = 5000
    
    det_times = []
    rand_times = []
    
    for dist in distributions_to_plot:
        # Check if data exists and is finite (not inf or nan)
        det_val = None
        if (dist in results['Deterministic Quicksort'] and 
            size in results['Deterministic Quicksort'][dist]):
            mean_val = results['Deterministic Quicksort'][dist][size]['mean']
            if np.isfinite(mean_val):
                det_val = mean_val
        
        det_times.append(det_val if det_val is not None else np.nan)
        
        rand_val = None
        if (dist in results['Randomized Quicksort'] and 
            size in results['Randomized Quicksort'][dist]):
            mean_val = results['Randomized Quicksort'][dist][size]['mean']
            if np.isfinite(mean_val):
                rand_val = mean_val
        
        rand_times.append(rand_val if rand_val is not None else np.nan)
    
    bars1 = ax.bar(x - width/2, det_times, width, label='Deterministic Quicksort', 
                   color='#1f77b4', alpha=0.8)
    bars2 = ax.bar(x + width/2, rand_times, width, label='Randomized Quicksort', 
                   color='#ff7f0e', alpha=0.8)
    
    ax.set_xlabel('Input Distribution', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title(f'Quicksort Performance Comparison (Array Size: {size})', 
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(distributions_to_plot)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0 and np.isfinite(height):
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.4f}s',
                       ha='center', va='bottom', fontsize=9)
    
    # Add annotation for missing data
    missing_det = [i for i, (dist, val) in enumerate(zip(distributions_to_plot, det_times)) 
                   if not np.isfinite(val) or np.isnan(val)]
    if missing_det:
        missing_dists = [distributions_to_plot[i] for i in missing_det]
        note_text = f"Note: Deterministic Quicksort failed on {', '.join(missing_dists)}\n"
        note_text += "due to worst-case O(n²) performance (see README for details)"
        ax.text(0.5, 0.02, note_text, transform=ax.transAxes, 
               fontsize=9, ha='center', va='bottom', 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('docs/quicksort_comparison_bar.png', dpi=300, bbox_inches='tight')
    print("Saved: docs/quicksort_comparison_bar.png")
    plt.close()
    
    # Plot 3: Scalability analysis
    print("Generating scalability plot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Focus on random distribution for scalability
    dist = 'Random'
    # Filter out infinite values
    valid_sizes_det = [s for s in sizes 
                      if (s in results['Deterministic Quicksort'][dist] and 
                          np.isfinite(results['Deterministic Quicksort'][dist][s]['mean']))]
    valid_sizes_rand = [s for s in sizes 
                       if (s in results['Randomized Quicksort'][dist] and 
                           np.isfinite(results['Randomized Quicksort'][dist][s]['mean']))]
    
    sizes_list = sorted(set(valid_sizes_det + valid_sizes_rand))
    
    det_times = [results['Deterministic Quicksort'][dist][s]['mean'] 
                for s in sizes_list if s in valid_sizes_det]
    det_sizes = [s for s in sizes_list if s in valid_sizes_det]
    rand_times = [results['Randomized Quicksort'][dist][s]['mean'] 
                 for s in sizes_list if s in valid_sizes_rand]
    rand_sizes = [s for s in sizes_list if s in valid_sizes_rand]
    
    if det_sizes:
        ax.plot(det_sizes, det_times, marker='o', label='Deterministic Quicksort', 
               color='#1f77b4', linewidth=2.5, markersize=8)
    if rand_sizes:
        ax.plot(rand_sizes, rand_times, marker='s', label='Randomized Quicksort', 
               color='#ff7f0e', linewidth=2.5, markersize=8)
    
    # Add theoretical O(n log n) reference line
    if det_sizes and det_times:
        # Normalize to match first data point
        n_log_n = [s * np.log2(s) for s in det_sizes]
        scale_factor = det_times[0] / n_log_n[0] if n_log_n[0] > 0 else 1
        n_log_n_scaled = [x * scale_factor for x in n_log_n]
        ax.plot(det_sizes, n_log_n_scaled, '--', label='O(n log n) reference', 
               color='gray', linewidth=2, alpha=0.7)
    
    ax.set_xlabel('Array Size', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Quicksort Scalability Analysis (Random Distribution)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('docs/quicksort_scalability.png', dpi=300, bbox_inches='tight')
    print("Saved: docs/quicksort_scalability.png")
    plt.close()
    
    # Plot 4: Worst-case comparison (sorted vs reverse sorted)
    print("Generating worst-case comparison plot...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    worst_case_dists = ['Sorted', 'Reverse Sorted']
    # Use all sizes, not just those from Random distribution
    all_sizes = sorted(sizes)
    x = np.arange(len(all_sizes))
    width = 0.35
    
    for dist_idx, dist in enumerate(worst_case_dists):
        det_times = []
        rand_times = []
        
        for size in all_sizes:
            # Check if data exists and is finite (not inf or nan)
            det_val = None
            if (dist in results['Deterministic Quicksort'] and 
                size in results['Deterministic Quicksort'][dist]):
                mean_val = results['Deterministic Quicksort'][dist][size]['mean']
                if np.isfinite(mean_val):
                    det_val = mean_val
            
            det_times.append(det_val if det_val is not None else np.nan)
            
            rand_val = None
            if (dist in results['Randomized Quicksort'] and 
                size in results['Randomized Quicksort'][dist]):
                mean_val = results['Randomized Quicksort'][dist][size]['mean']
                if np.isfinite(mean_val):
                    rand_val = mean_val
            
            rand_times.append(rand_val if rand_val is not None else np.nan)
        
        offset = (dist_idx - 0.5) * width
        ax.bar(x + offset, det_times, width/2, label=f'Deterministic ({dist})', 
              alpha=0.7, color=['#1f77b4', '#2ca02c'][dist_idx])
        ax.bar(x + offset + width/2, rand_times, width/2, 
              label=f'Randomized ({dist})', alpha=0.7, 
              color=['#ff7f0e', '#d62728'][dist_idx])
    
    ax.set_xlabel('Array Size', fontsize=12, fontweight='bold')
    ax.set_ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_title('Worst-Case Performance: Sorted vs Reverse Sorted', 
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([str(s) for s in all_sizes], rotation=45)
    ax.legend(fontsize=10, ncol=2)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')
    
    # Add annotation for missing data
    missing_sizes = []
    for size_idx, size in enumerate(all_sizes):
        has_det_data = False
        for dist in worst_case_dists:
            if (dist in results['Deterministic Quicksort'] and 
                size in results['Deterministic Quicksort'][dist]):
                mean_val = results['Deterministic Quicksort'][dist][size]['mean']
                if np.isfinite(mean_val):
                    has_det_data = True
                    break
        if not has_det_data:
            missing_sizes.append(size)
    
    if missing_sizes:
        note_text = f"Note: Missing bars for Deterministic Quicksort at sizes ≥{min(missing_sizes)}\n"
        note_text += "indicate execution failures due to recursion limits and O(n²) complexity"
        ax.text(0.5, 0.02, note_text, transform=ax.transAxes, 
               fontsize=9, ha='center', va='bottom', 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('docs/quicksort_worst_case.png', dpi=300, bbox_inches='tight')
    print("Saved: docs/quicksort_worst_case.png")
    plt.close()
    
    print("\nAll plots generated successfully!")
    print("Plots saved in the 'docs' directory.")


if __name__ == '__main__':
    generate_performance_plots()

