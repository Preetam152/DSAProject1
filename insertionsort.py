
A = [1000, 2000, 3000, 4000, 10000, 6000, 20000, 40000, 50000, 70000, 60000, 80000, 90000, 100000]

def ins_sort(array):
    n = len(array)
    for a in range(1,n):
        for b in range(a, 0, -1):
            if array[b-1] > array[b]:
                array[b-1], array[b] = array[b], array[b-1]
            else:
                break
    return array

array_A = A[:]
print("Original array:", array_A)

insertion_sort_A = ins_sort(A)
print("Insertion sort array:", insertion_sort_A)


