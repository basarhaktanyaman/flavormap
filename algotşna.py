def merge_sort(arr):
    """
    Custom implementation of merge sort algorithm
    Sorts array in ascending order
    """
    if len(arr) <= 1:
        return arr
    
    
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    
    return merge(left_half, right_half)


def merge(left, right):
    """
    Merge two sorted arrays into one sorted array
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def min_outer_boxes(boxes):
    
    
    sorted_boxes = merge_sort(boxes)
    
    from collections import Counter
    size_counts = Counter(sorted_boxes)
    
    
    return max(size_counts.values())


if __name__ == "__main__":
    example1 = [5, 4, 3, 6, 1, 2]
    result1 = min_outer_boxes(example1)
    print(f"Input: {[5, 4, 3, 6, 1, 2]}")
    print(f"After custom sorting: {merge_sort([5, 4, 3, 6, 1, 2])}")
    print(f"Minimum outer boxes: {result1}")
    print()
    
    example2 = [3, 3, 3, 1, 2]
    result2 = min_outer_boxes(example2)
    print(f"Input: {example2}")
    print(f"After custom sorting: {merge_sort(example2.copy())}")
    print(f"Minimum outer boxes: {result2}")
    print(f"Explanation: Three boxes of size 3 cannot nest, so minimum is 3")
    print()
    
    example3 = [10, 5, 15, 5, 20]
    result3 = min_outer_boxes(example3)
    print(f"Input: {example3}")
    print(f"After custom sorting: {merge_sort(example3.copy())}")
    print(f"Minimum outer boxes: {result3}")
    print(f"Explanation: Two boxes of size 5, so minimum is 2")
