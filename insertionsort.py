import random
import time
import matplotlib.pyplot as plt
import heapq
import sys
sys.setrecursionlimit(1000000)

def insertion_sort(arr):
    n = len(arr)
    for a in range(1, n):
        for b in range(a, 0, -1):
            if arr[b - 1] > arr[b]:
                arr[b - 1], arr[b] = arr[b], arr[b - 1]
            else:
                break
    return arr

def merge_sort(array):
    if len(array) <= 1:
        return array
    m = len(array)//2
    l = merge_sort(array[:m])
    right = merge_sort(array[m:])
    return merge(l, right)

def merge(l, r):
    r = []
    i=j=0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            r.append(l[i]); i+=1
        else:
            r.append(r[j]); j+=1
    r.extend(l[i:]); r.extend(r[j:])
    return r

def heap_sort(array):
    heap = []
    for v in array:
        heapq.heappush(heap, v)
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
        if a[low] > a[mid]: a[low], a[mid] = a[mid], a[low]
        if a[mid] > a[high]: a[mid], a[high] = a[high], a[mid]
        if a[low] > a[mid]: a[low], a[mid] = a[mid], a[low]
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

sizes = [1000, 2000, 3000, 4000, 5000, 10000]
runs = 3
algorithms = {
    'Insertion': insertion_sort,
    'Merge': merge_sort,
    'Heap': heap_sort,
    'Quick': quick_sort,
    'Modified Quick': modified_quick_sort
}
results_random = {name: [] for name in algorithms}
results_sorted = {name: [] for name in algorithms}
results_reversed = {name: [] for name in algorithms}

for n in sizes:
    for name, func in algorithms.items():
        elapsed_random=elapsed_sorted=elapsed_reversed=0
        for _ in range(runs):
            arr_random = [random.randint(0,10**6) for _ in range(n)]
            start=time.perf_counter(); func(arr_random); end=time.perf_counter(); elapsed_random+=end-start
            arr_sorted = sorted(arr_random)
            start=time.perf_counter(); func(arr_sorted); end=time.perf_counter(); elapsed_sorted+=end-start
            arr_reversed = sorted(arr_random, reverse=True)
            start=time.perf_counter(); func(arr_reversed); end=time.perf_counter(); elapsed_reversed+=end-start
        results_random[name].append(elapsed_random/runs)
        results_sorted[name].append(elapsed_sorted/runs)
        results_reversed[name].append(elapsed_reversed/runs)
    print(f"Completed n={n}")

plt.figure(figsize=(12,7))
markers = ['o','s','^','D','*']
for i,(name, times) in enumerate(results_random.items()):
    plt.plot(sizes, times, marker=markers[i], label=f'{name} - Random')
    plt.plot(sizes, results_sorted[name], linestyle='--', marker=markers[i], label=f'{name} - Sorted')
    plt.plot(sizes, results_reversed[name], linestyle=':', marker=markers[i], label=f'{name} - Reversed')
plt.xlabel('Input Size (n)')
plt.ylabel('Average Execution Time (s)')
plt.title('Sorting Algorithm Performance Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("sorting_algorithms_performance.png")
print("sorting_algorithms_performance.png")
