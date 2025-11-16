"""
Test cases for comparison utilities.
"""

import unittest
from src.comparison import (
    generate_random_array,
    generate_sorted_array,
    generate_reverse_sorted_array,
    generate_nearly_sorted_array,
    generate_array_with_duplicates,
    benchmark_sorting_algorithm
)
from src.quicksort import quicksort, randomized_quicksort


class TestArrayGenerators(unittest.TestCase):
    """Test array generator functions."""
    
    def test_generate_random_array(self):
        """Test random array generation."""
        arr = generate_random_array(100, 0, 100)
        self.assertEqual(len(arr), 100)
        self.assertTrue(all(0 <= x <= 100 for x in arr))
    
    def test_generate_sorted_array(self):
        """Test sorted array generation."""
        arr = generate_sorted_array(10, 0, 1)
        self.assertEqual(arr, list(range(10)))
        
        arr = generate_sorted_array(5, 10, 2)
        self.assertEqual(arr, [10, 12, 14, 16, 18])
    
    def test_generate_reverse_sorted_array(self):
        """Test reverse-sorted array generation."""
        arr = generate_reverse_sorted_array(10, 0, 1)
        self.assertEqual(arr, list(range(9, -1, -1)))
    
    def test_generate_nearly_sorted_array(self):
        """Test nearly sorted array generation."""
        arr = generate_nearly_sorted_array(100, 5)
        self.assertEqual(len(arr), 100)
        # Should be mostly sorted
        sorted_arr = sorted(arr)
        # Count inversions (should be small)
        inversions = sum(1 for i in range(len(arr)-1) if arr[i] > arr[i+1])
        self.assertLess(inversions, 20)  # Should have few inversions
    
    def test_generate_array_with_duplicates(self):
        """Test array with duplicates generation."""
        arr = generate_array_with_duplicates(100, 5)
        self.assertEqual(len(arr), 100)
        unique_values = set(arr)
        self.assertLessEqual(len(unique_values), 5)


class TestBenchmarking(unittest.TestCase):
    """Test benchmarking utilities."""
    
    def test_benchmark_quicksort(self):
        """Test benchmarking quicksort."""
        arr = generate_random_array(100)
        stats = benchmark_sorting_algorithm(quicksort, arr, iterations=3)
        
        self.assertIn('mean', stats)
        self.assertIn('median', stats)
        self.assertIn('min', stats)
        self.assertIn('max', stats)
        self.assertIn('stdev', stats)
        
        self.assertGreater(stats['mean'], 0)
        self.assertGreaterEqual(stats['min'], 0)
        self.assertGreaterEqual(stats['max'], stats['min'])
    
    def test_benchmark_randomized_quicksort(self):
        """Test benchmarking randomized quicksort."""
        arr = generate_random_array(100)
        stats = benchmark_sorting_algorithm(
            lambda a: randomized_quicksort(a, seed=42),
            arr,
            iterations=3
        )
        
        self.assertIn('mean', stats)
        self.assertGreater(stats['mean'], 0)
    
    def test_benchmark_verifies_sorting(self):
        """Test that benchmarking verifies correct sorting."""
        def bad_sort(arr):
            # Intentionally bad sort that doesn't actually sort
            return arr
        
        arr = generate_random_array(10)
        
        with self.assertRaises(ValueError):
            benchmark_sorting_algorithm(bad_sort, arr)


if __name__ == '__main__':
    unittest.main()

