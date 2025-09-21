import random
import time
import matplotlib.pyplot as plt
import heapq
import sys
import pandas as pd

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

def quick_sort(a):
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

def modified_quick_sort(a, cutoff=10):
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

    stack = [(0, len(a)-1)]
    while stack:
        low, high = stack.pop()
        if high-low+1 <= cutoff:
            insertion_sort_subarray(a, low, high)
        elif low < high:
            pivot_index = median_of_three(a, low, high)
            a[pivot_index], a[high] = a[high], a[pivot_index]
            pivot = a[high]
            i = low - 1
            for j in range(low, high):
                if a[j] <= pivot:
                    i +=1
                    a[i], a[j] = a[j], a[i]
            a[i+1], a[high] = a[high], a[i+1]
            p = i+1
            if p-1-low > high-(p+1):
                stack.append((low, p-1))
                stack.append((p+1, high))
            else:
                stack.append((p+1, high))
                stack.append((low, p-1))
    return a

def time_algorithm(func, arr):
    arr_copy = arr[:] 
    start = time.perf_counter()
    func(arr_copy)
    return time.perf_counter() - start

# --- configuration ---
sizes = [1000, 2000, 3000, 4000, 5000, 10000, 20000, 40000, 50000, 60000, 80000, 90000, 100000]
runs = 3
algorithms = {
    'Insertion': insertion_sort,
    'Merge': merge_sort,
    'Heap': heap_sort,
    'Quick': quick_sort,
    'Modified Quick': modified_quick_sort
}
results_unsorted = {name: [] for name in algorithms}
results_sorted = {name: [] for name in algorithms}
results_reversed = {name: [] for name in algorithms}
all_rows = []

for n in sizes:
    arr_unsorted = [random.randint(0, 10**6) for _ in range(n)]
    arr_sorted = sorted(arr_unsorted)
    arr_reversed = sorted(arr_unsorted, reverse=True)

    for name, func in algorithms.items():
        if n > 10000 and name == 'Insertion':
            unsorted_time = sorted_time = reversed_time = float('nan')
        else:
            f = func
            eu = es = er = 0.0
            a_u, a_s, a_r = arr_unsorted, arr_sorted, arr_reversed
            for _ in range(runs):
                eu += time_algorithm(f, a_u)
                es += time_algorithm(f, a_s)
                er += time_algorithm(f, a_r)
            unsorted_time = eu / runs
            sorted_time = es / runs
            reversed_time = er / runs

        results_unsorted[name].append(unsorted_time)
        results_sorted[name].append(sorted_time)
        results_reversed[name].append(reversed_time)

        all_rows.append({
            'Size': n,
            'Algorithm': name + ' Sort',
            'Unsorted Time(s)': unsorted_time,
            'Sorted Time(s)': sorted_time,
            'Reversed Time(s)': reversed_time
        })
    print(f"Completed n={n}")

print("\n All sizes completed.\n")
df = pd.DataFrame(all_rows)
print(df.to_string(index=False))

plt.figure(figsize=(12, 7))
markers = ['o', 's', '^', 'D', '*']
for i, (name, times) in enumerate(results_unsorted.items()):
    plt.plot(sizes[:len(times)], times, marker=markers[i], label=f'{name} - Unsorted')
plt.ylabel('Average Execution Time (s)')
plt.xlabel('Input Size')
plt.title('Sorting Algorithm Performance Comparison (Unsorted Input)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("sorting_algorithms_performance.png")
print("\n sorting_algorithms_performance.png")