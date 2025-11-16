"""
Test cases for Quicksort implementation.
"""

import unittest
import random
from typing import List

from src.quicksort import quicksort, randomized_quicksort, quicksort_3way


class TestQuicksort(unittest.TestCase):
    """Test cases for deterministic Quicksort."""
    
    def test_empty_array(self):
        """Test sorting an empty array."""
        arr = []
        quicksort(arr)
        self.assertEqual(arr, [])
        
        result = quicksort([], in_place=False)
        self.assertEqual(result, [])
    
    def test_single_element(self):
        """Test sorting an array with a single element."""
        arr = [42]
        quicksort(arr)
        self.assertEqual(arr, [42])
        
        result = quicksort([42], in_place=False)
        self.assertEqual(result, [42])
    
    def test_two_elements(self):
        """Test sorting an array with two elements."""
        arr = [2, 1]
        quicksort(arr)
        self.assertEqual(arr, [1, 2])
        
        arr = [1, 2]
        quicksort(arr)
        self.assertEqual(arr, [1, 2])
    
    def test_already_sorted(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5]
        quicksort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_reverse_sorted(self):
        """Test sorting a reverse-sorted array."""
        arr = [5, 4, 3, 2, 1]
        quicksort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_random_array(self):
        """Test sorting a random array."""
        arr = [3, 6, 8, 10, 1, 2, 1]
        quicksort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 6, 8, 10])
    
    def test_duplicate_elements(self):
        """Test sorting an array with duplicate elements."""
        arr = [5, 2, 8, 2, 9, 1, 5, 5]
        quicksort(arr)
        self.assertEqual(arr, [1, 2, 2, 5, 5, 5, 8, 9])
    
    def test_negative_numbers(self):
        """Test sorting an array with negative numbers."""
        arr = [-3, 5, -1, 0, -5, 2]
        quicksort(arr)
        self.assertEqual(arr, [-5, -3, -1, 0, 2, 5])
    
    def test_large_array(self):
        """Test sorting a large array."""
        import random
        # Use random array to avoid worst-case recursion depth
        arr = list(range(1, 501))
        random.shuffle(arr)
        quicksort(arr)
        self.assertEqual(arr, list(range(1, 501)))
    
    def test_in_place_sorting(self):
        """Test that in-place sorting modifies the original array."""
        arr = [5, 2, 8, 1, 9]
        original_id = id(arr)
        result = quicksort(arr, in_place=True)
        
        self.assertIsNone(result)
        self.assertEqual(id(arr), original_id)
        self.assertEqual(arr, [1, 2, 5, 8, 9])
    
    def test_non_in_place_sorting(self):
        """Test that non-in-place sorting doesn't modify the original."""
        arr = [5, 2, 8, 1, 9]
        original = arr.copy()
        result = quicksort(arr, in_place=False)
        
        self.assertEqual(arr, original)
        self.assertEqual(result, [1, 2, 5, 8, 9])
        self.assertIsNotNone(result)
    
    def test_custom_key_function(self):
        """Test sorting with a custom key function."""
        arr = [{'value': 3}, {'value': 1}, {'value': 2}]
        quicksort(arr, key=lambda x: x['value'])
        self.assertEqual([x['value'] for x in arr], [1, 2, 3])
        
        # Test with tuples
        arr = [(2, 'b'), (1, 'a'), (3, 'c')]
        quicksort(arr, key=lambda x: x[0])
        self.assertEqual([x[0] for x in arr], [1, 2, 3])


class TestRandomizedQuicksort(unittest.TestCase):
    """Test cases for Randomized Quicksort."""
    
    def test_empty_array(self):
        """Test sorting an empty array."""
        arr = []
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [])
    
    def test_single_element(self):
        """Test sorting an array with a single element."""
        arr = [42]
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [42])
    
    def test_random_array(self):
        """Test sorting a random array."""
        arr = [3, 6, 8, 10, 1, 2, 1]
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [1, 1, 2, 3, 6, 8, 10])
    
    def test_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5]
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_reverse_sorted_array(self):
        """Test sorting a reverse-sorted array."""
        arr = [5, 4, 3, 2, 1]
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        arr1 = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        arr2 = arr1.copy()
        
        randomized_quicksort(arr1, seed=42)
        randomized_quicksort(arr2, seed=42)
        
        self.assertEqual(arr1, arr2)
        self.assertEqual(arr1, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_large_array(self):
        """Test sorting a large array."""
        import random
        # Use random array to avoid worst-case recursion depth
        arr = list(range(1, 501))
        random.shuffle(arr)
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, list(range(1, 501)))
    
    def test_in_place_sorting(self):
        """Test that in-place sorting modifies the original array."""
        arr = [5, 2, 8, 1, 9]
        original_id = id(arr)
        result = randomized_quicksort(arr, in_place=True, seed=42)
        
        self.assertIsNone(result)
        self.assertEqual(id(arr), original_id)
        self.assertEqual(arr, [1, 2, 5, 8, 9])
    
    def test_non_in_place_sorting(self):
        """Test that non-in-place sorting doesn't modify the original."""
        arr = [5, 2, 8, 1, 9]
        original = arr.copy()
        result = randomized_quicksort(arr, in_place=False, seed=42)
        
        self.assertEqual(arr, original)
        self.assertEqual(result, [1, 2, 5, 8, 9])


class TestQuicksort3Way(unittest.TestCase):
    """Test cases for Three-way Quicksort."""
    
    def test_empty_array(self):
        """Test sorting an empty array."""
        arr = []
        quicksort_3way(arr)
        self.assertEqual(arr, [])
    
    def test_single_element(self):
        """Test sorting an array with a single element."""
        arr = [42]
        quicksort_3way(arr)
        self.assertEqual(arr, [42])
    
    def test_all_duplicates(self):
        """Test sorting an array with all duplicate elements."""
        arr = [5, 5, 5, 5, 5]
        quicksort_3way(arr)
        self.assertEqual(arr, [5, 5, 5, 5, 5])
    
    def test_many_duplicates(self):
        """Test sorting an array with many duplicate elements."""
        arr = [3, 2, 3, 1, 3, 2, 1, 3, 2]
        quicksort_3way(arr)
        self.assertEqual(arr, [1, 1, 2, 2, 2, 3, 3, 3, 3])
    
    def test_random_array(self):
        """Test sorting a random array."""
        arr = [3, 6, 8, 10, 1, 2, 1]
        quicksort_3way(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 6, 8, 10])
    
    def test_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5]
        quicksort_3way(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_large_array_with_duplicates(self):
        """Test sorting a large array with many duplicates."""
        arr = [random.randint(0, 10) for _ in range(1000)]
        expected = sorted(arr)
        quicksort_3way(arr)
        self.assertEqual(arr, expected)


class TestQuicksortEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_all_same_elements(self):
        """Test sorting an array where all elements are the same."""
        arr = [7, 7, 7, 7, 7]
        quicksort(arr)
        self.assertEqual(arr, [7, 7, 7, 7, 7])
        
        randomized_quicksort(arr, seed=42)
        self.assertEqual(arr, [7, 7, 7, 7, 7])
    
    def test_alternating_pattern(self):
        """Test sorting an array with alternating pattern."""
        arr = [1, 5, 2, 4, 3]
        quicksort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_floating_point_numbers(self):
        """Test sorting an array with floating point numbers."""
        arr = [3.5, 1.2, 4.8, 2.1, 5.9]
        quicksort(arr)
        self.assertEqual(arr, [1.2, 2.1, 3.5, 4.8, 5.9])
    
    def test_strings(self):
        """Test sorting an array of strings."""
        arr = ['banana', 'apple', 'cherry', 'date']
        quicksort(arr)
        self.assertEqual(arr, ['apple', 'banana', 'cherry', 'date'])
    
    def test_mixed_types_with_key(self):
        """Test sorting with key function to handle mixed types."""
        arr = [('b', 2), ('a', 1), ('c', 3)]
        quicksort(arr, key=lambda x: x[1])
        self.assertEqual([x[1] for x in arr], [1, 2, 3])


if __name__ == '__main__':
    unittest.main()

