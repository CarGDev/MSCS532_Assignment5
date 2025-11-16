"""
Demonstration of Quicksort algorithm usage.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quicksort import quicksort, randomized_quicksort, quicksort_3way


def demo_basic_quicksort():
    """Demonstrate basic Quicksort usage."""
    print("=" * 60)
    print("BASIC QUICKSORT DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Simple integer array
    print("\n1. Sorting a simple integer array:")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Original: {arr}")
    quicksort(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 2: Already sorted array
    print("\n2. Sorting an already sorted array:")
    arr = [1, 2, 3, 4, 5]
    print(f"   Original: {arr}")
    quicksort(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 3: Reverse sorted array
    print("\n3. Sorting a reverse-sorted array:")
    arr = [5, 4, 3, 2, 1]
    print(f"   Original: {arr}")
    quicksort(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 4: Array with duplicates
    print("\n4. Sorting an array with duplicate elements:")
    arr = [5, 2, 8, 2, 9, 1, 5, 5]
    print(f"   Original: {arr}")
    quicksort(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 5: Non-in-place sorting
    print("\n5. Non-in-place sorting (preserves original):")
    arr = [3, 1, 4, 1, 5, 9, 2, 6]
    original = arr.copy()
    sorted_arr = quicksort(arr, in_place=False)
    print(f"   Original: {original}")
    print(f"   Sorted:   {sorted_arr}")
    print(f"   Original unchanged: {arr == original}")


def demo_randomized_quicksort():
    """Demonstrate Randomized Quicksort usage."""
    print("\n" + "=" * 60)
    print("RANDOMIZED QUICKSORT DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Random array
    print("\n1. Sorting a random array:")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Original: {arr}")
    randomized_quicksort(arr, seed=42)
    print(f"   Sorted:   {arr}")
    
    # Example 2: Sorted array (randomized should handle better)
    print("\n2. Sorting a sorted array (worst case for deterministic):")
    arr = list(range(1, 11))
    print(f"   Original: {arr}")
    randomized_quicksort(arr, seed=42)
    print(f"   Sorted:   {arr}")
    
    # Example 3: Reproducibility with seed
    print("\n3. Reproducibility with same seed:")
    arr1 = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    arr2 = arr1.copy()
    randomized_quicksort(arr1, seed=42)
    randomized_quicksort(arr2, seed=42)
    print(f"   Array 1: {arr1}")
    print(f"   Array 2: {arr2}")
    print(f"   Results match: {arr1 == arr2}")


def demo_3way_quicksort():
    """Demonstrate Three-way Quicksort usage."""
    print("\n" + "=" * 60)
    print("THREE-WAY QUICKSORT DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Array with many duplicates
    print("\n1. Sorting array with many duplicate elements:")
    arr = [3, 2, 3, 1, 3, 2, 1, 3, 2, 1]
    print(f"   Original: {arr}")
    quicksort_3way(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 2: All same elements
    print("\n2. Sorting array with all same elements:")
    arr = [5, 5, 5, 5, 5]
    print(f"   Original: {arr}")
    quicksort_3way(arr)
    print(f"   Sorted:   {arr}")
    
    # Example 3: Random array
    print("\n3. Sorting a random array:")
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Original: {arr}")
    quicksort_3way(arr)
    print(f"   Sorted:   {arr}")


def demo_custom_key():
    """Demonstrate sorting with custom key function."""
    print("\n" + "=" * 60)
    print("CUSTOM KEY FUNCTION DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Sorting dictionaries
    print("\n1. Sorting list of dictionaries by value:")
    arr = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    ]
    print(f"   Original: {arr}")
    quicksort(arr, key=lambda x: x['age'])
    print(f"   Sorted by age: {arr}")
    
    # Example 2: Sorting tuples
    print("\n2. Sorting list of tuples by second element:")
    arr = [('apple', 3), ('banana', 1), ('cherry', 2)]
    print(f"   Original: {arr}")
    quicksort(arr, key=lambda x: x[1])
    print(f"   Sorted by count: {arr}")


if __name__ == '__main__':
    demo_basic_quicksort()
    demo_randomized_quicksort()
    demo_3way_quicksort()
    demo_custom_key()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

