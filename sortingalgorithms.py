import random
import time
import matplotlib.pyplot as plt
import heapq
import sys
sys.setrecursionlimit(1000000)

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(array):
    if len(array) <= 1:
        return array
    m = len(array)//2
    left = merge_sort(array[:m])
    right = merge_sort(array[m:])
    return merge(left, right)

def merge(left, right):
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

def heap_sort(array):
    heap = array[:]
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]

def quick_sort(arr):
    a = arr[:]
    s = [(0, len(a)-1)]
    while s:
        low, high = s.pop()
        if low < high:
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                if a[j] <= pivot:
                    i += 1
                    a[i], a[j] = a[j], a[i]
            a[i+1], a[high] = a[high], a[i+1]
            p = i+1
            if p-1-low > high-(p+1):
                s.append((low, p-1))
                s.append((p+1, high))
            else:
                s.append((p+1, high))
                s.append((low, p-1))
    return a

def modified_quick_sort(arr, cutoff=10):
    arr_copy = arr[:]
    def insertion_sort_subarray(a, low, high):
        for i in range(low+1, high+1):
            key = a[i]
            j = i-1
            while j>=low and a[j]>key:
                a[j+1] = a[j]
                j-=1
            a[j+1] = key
    
    def median_of_three(a, low, high):
        mid = (low+high)//2
        if a[low] <= a[mid]:
            if a[mid] <= a[high]:
                return mid
            elif a[low] <= a[high]:
                return high
            else:
                return low
        else:
            if a[low] <= a[high]:
                return low
            elif a[mid] <= a[high]:
                return high
            else:
                return mid
    
    stack = [(0, len(arr_copy)-1)]
    while stack:
        low, high = stack.pop()
        if high-low+1 <= cutoff:
            insertion_sort_subarray(arr_copy, low, high)
        elif low < high:
            pivot_index = median_of_three(arr_copy, low, high)
            arr_copy[pivot_index], arr_copy[high] = arr_copy[high], arr_copy[pivot_index]
            pivot = arr_copy[high]
            i = low - 1
            for j in range(low, high):
                if arr_copy[j] <= pivot:
                    i +=1
                    arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
            arr_copy[i+1], arr_copy[high] = arr_copy[high], arr_copy[i+1]
            p = i+1
            if p-1-low > high-(p+1):
                stack.append((low, p-1))
                stack.append((p+1, high))
            else:
                stack.append((p+1, high))
                stack.append((low, p-1))
    return arr_copy

def time_algorithm(func, arr):
    arr_copy = arr[:]
    start = time.perf_counter()
    func(arr_copy)
    return time.perf_counter() - start

sizes = [1000, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 50000, 60000, 80000, 90000, 100000]
runs = 5
algorithms = {
    'Insertion': insertion_sort,
    'Merge': merge_sort,
    'Heap': heap_sort,
    'Quick': quick_sort,
    'Modified Quick': modified_quick_sort
}
results_random = {name: [] for name in algorithms}


for n in sizes:
    arr_random = [random.randint(0, 10**6) for _ in range(n)]
    
    for name, func in algorithms.items():
        if n > 10000 and name == 'Insertion':
            results_random[name].append(float('nan'))
            continue  
        elapsed_random = 0
        
        for _ in range(runs):
            elapsed_random += time_algorithm(func, arr_random)
        
        results_random[name].append(elapsed_random / runs)
    print(f"Completed n={n}")

plt.figure(figsize=(12, 7))
markers = ['o', 's', '^', 'D', '*']
for i, (name, times) in enumerate(results_random.items()):
    plt.plot(sizes[:len(times)], times, marker=markers[i], label=f'{name} - Random')
plt.ylabel('Average Execution Time (s)')
plt.title('Sorting Algorithm Performance Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("sorting_algorithms_performance.png")
print("sorting_algorithms_performance.png")