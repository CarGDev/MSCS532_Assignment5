"""
Quicksort Implementation

This module provides both deterministic and randomized versions of the Quicksort algorithm.
"""

from typing import List, Callable, Optional, Any
import random


def partition(
    arr: List[Any],
    low: int,
    high: int,
    pivot_index: int,
    key: Optional[Callable[[Any], Any]] = None
) -> int:
    """
    Partition the array around a pivot element.
    
    After partitioning, all elements less than the pivot are on the left,
    and all elements greater than or equal to the pivot are on the right.
    
    Args:
        arr: The array to partition
        low: Starting index of the subarray
        high: Ending index of the subarray (inclusive)
        pivot_index: Index of the pivot element
        key: Optional function to extract comparison key from elements
    
    Returns:
        The final position of the pivot element after partitioning
    
    Time Complexity: O(n) where n = high - low + 1
    Space Complexity: O(1)
    """
    # Move pivot to the end
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    
    # Get pivot value
    pivot_value = key(arr[high]) if key else arr[high]
    
    # Index of smaller element (indicates right position of pivot)
    i = low - 1
    
    for j in range(low, high):
        # Compare current element with pivot
        current_value = key(arr[j]) if key else arr[j]
        if current_value < pivot_value:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quicksort_recursive(
    arr: List[Any],
    low: int,
    high: int,
    pivot_selector: Callable[[int, int], int],
    key: Optional[Callable[[Any], Any]] = None
) -> None:
    """
    Recursive helper function for Quicksort.
    
    Args:
        arr: The array to sort
        low: Starting index
        high: Ending index (inclusive)
        pivot_selector: Function that takes (low, high) and returns pivot index
        key: Optional function to extract comparison key from elements
    """
    if low < high:
        # Select pivot using the provided selector function
        pivot_index = pivot_selector(low, high)
        
        # Partition the array and get the pivot's final position
        pivot_pos = partition(arr, low, high, pivot_index, key)
        
        # Recursively sort elements before and after partition
        _quicksort_recursive(arr, low, pivot_pos - 1, pivot_selector, key)
        _quicksort_recursive(arr, pivot_pos + 1, high, pivot_selector, key)


def quicksort(
    arr: List[Any],
    in_place: bool = True,
    key: Optional[Callable[[Any], Any]] = None
) -> Optional[List[Any]]:
    """
    Deterministic Quicksort algorithm.
    
    Uses the last element as the pivot (Lomuto partition scheme).
    
    Args:
        arr: The array to sort
        in_place: If True, sorts the array in place and returns None.
                  If False, returns a new sorted array without modifying the original.
        key: Optional function to extract comparison key from elements.
             If provided, elements are compared using key(element).
    
    Returns:
        None if in_place=True, otherwise a new sorted list
    
    Time Complexity:
        - Best case: O(n log n) - balanced partitions
        - Average case: O(n log n) - expected balanced partitions
        - Worst case: O(n²) - highly unbalanced partitions (e.g., sorted array)
    
    Space Complexity:
        - Best case: O(log n) - balanced recursion stack
        - Average case: O(log n) - expected balanced recursion stack
        - Worst case: O(n) - highly unbalanced recursion stack
    
    Example:
        >>> arr = [3, 6, 8, 10, 1, 2, 1]
        >>> quicksort(arr)
        >>> arr
        [1, 1, 2, 3, 6, 8, 10]
        
        >>> arr = [3, 6, 8, 10, 1, 2, 1]
        >>> sorted_arr = quicksort(arr, in_place=False)
        >>> sorted_arr
        [1, 1, 2, 3, 6, 8, 10]
        >>> arr  # Original unchanged
        [3, 6, 8, 10, 1, 2, 1]
    """
    if not arr:
        return None if in_place else []
    
    if in_place:
        # Use last element as pivot (deterministic)
        pivot_selector = lambda low, high: high
        _quicksort_recursive(arr, 0, len(arr) - 1, pivot_selector, key)
        return None
    else:
        # Create a copy to avoid modifying the original
        arr_copy = arr.copy()
        pivot_selector = lambda low, high: high
        _quicksort_recursive(arr_copy, 0, len(arr_copy) - 1, pivot_selector, key)
        return arr_copy


def randomized_quicksort(
    arr: List[Any],
    in_place: bool = True,
    key: Optional[Callable[[Any], Any]] = None,
    seed: Optional[int] = None
) -> Optional[List[Any]]:
    """
    Randomized Quicksort algorithm.
    
    Uses a randomly selected element as the pivot, which helps avoid worst-case
    performance on sorted or nearly sorted inputs.
    
    Args:
        arr: The array to sort
        in_place: If True, sorts the array in place and returns None.
                  If False, returns a new sorted array without modifying the original.
        key: Optional function to extract comparison key from elements.
             If provided, elements are compared using key(element).
        seed: Optional random seed for reproducibility
    
    Returns:
        None if in_place=True, otherwise a new sorted list
    
    Time Complexity:
        - Best case: O(n log n) - balanced partitions
        - Average case: O(n log n) - expected balanced partitions with high probability
        - Worst case: O(n²) - still possible but extremely unlikely with randomization
    
    Space Complexity:
        - Best case: O(log n) - balanced recursion stack
        - Average case: O(log n) - expected balanced recursion stack
        - Worst case: O(n) - highly unbalanced recursion stack (very unlikely)
    
    Example:
        >>> arr = [3, 6, 8, 10, 1, 2, 1]
        >>> randomized_quicksort(arr, seed=42)
        >>> arr
        [1, 1, 2, 3, 6, 8, 10]
        
        >>> arr = [3, 6, 8, 10, 1, 2, 1]
        >>> sorted_arr = randomized_quicksort(arr, in_place=False, seed=42)
        >>> sorted_arr
        [1, 1, 2, 3, 6, 8, 10]
    """
    if not arr:
        return None if in_place else []
    
    if seed is not None:
        random.seed(seed)
    
    if in_place:
        # Use random element as pivot
        pivot_selector = lambda low, high: random.randint(low, high)
        _quicksort_recursive(arr, 0, len(arr) - 1, pivot_selector, key)
        return None
    else:
        # Create a copy to avoid modifying the original
        arr_copy = arr.copy()
        pivot_selector = lambda low, high: random.randint(low, high)
        _quicksort_recursive(arr_copy, 0, len(arr_copy) - 1, pivot_selector, key)
        return arr_copy


def quicksort_3way(
    arr: List[Any],
    in_place: bool = True,
    key: Optional[Callable[[Any], Any]] = None
) -> Optional[List[Any]]:
    """
    Three-way Quicksort (Dutch National Flag algorithm variant).
    
    Efficiently handles arrays with many duplicate elements by partitioning
    into three parts: elements less than, equal to, and greater than the pivot.
    
    Args:
        arr: The array to sort
        in_place: If True, sorts the array in place and returns None.
                  If False, returns a new sorted array without modifying the original.
        key: Optional function to extract comparison key from elements.
    
    Returns:
        None if in_place=True, otherwise a new sorted list
    
    Time Complexity:
        - Best case: O(n) - when all elements are equal
        - Average case: O(n log n)
        - Worst case: O(n²) - but rare with good pivot selection
    
    Example:
        >>> arr = [3, 2, 3, 1, 3, 2, 1]
        >>> quicksort_3way(arr)
        >>> arr
        [1, 1, 2, 2, 3, 3, 3]
    """
    if not arr:
        return None if in_place else []
    
    def _3way_partition(low: int, high: int) -> tuple[int, int]:
        """Three-way partition: returns (lt, gt) indices."""
        if low >= high:
            return low, high
        
        pivot_value = key(arr[high]) if key else arr[high]
        lt = low  # arr[low..lt-1] < pivot
        i = low   # arr[lt..i-1] == pivot
        gt = high # arr[gt+1..high] > pivot
        
        while i <= gt:
            current_value = key(arr[i]) if key else arr[i]
            if current_value < pivot_value:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif current_value > pivot_value:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1
        
        return lt, gt
    
    def _3way_quicksort_recursive(low: int, high: int) -> None:
        if low < high:
            lt, gt = _3way_partition(low, high)
            _3way_quicksort_recursive(low, lt - 1)
            _3way_quicksort_recursive(gt + 1, high)
    
    if in_place:
        _3way_quicksort_recursive(0, len(arr) - 1)
        return None
    else:
        arr_copy = arr.copy()
        # Temporarily replace arr to use in recursive function
        original_arr = arr
        arr = arr_copy
        _3way_quicksort_recursive(0, len(arr) - 1)
        arr = original_arr
        return arr_copy

