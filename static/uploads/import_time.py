import time
from copy import deepcopy



list1 = list(i for i in range(10000))
import random
random.shuffle(list1)


#Insertion sorting
def insertionSort(list):
    for i in range(1,len(list)):
        key = list[i]
        
        j =i-1
        while j>=0 and key < list[j]:
            list[j+1] = list[j]
            j -= 1
            
        list[j+1] = key

list= deepcopy(list1)
start = time.time()
insertionSort(list)
insert = time.time()
print("insertsort 수행시간 : %f"%(insert - start))

#Bubble sorting
def bubbleSort(list):
    n = len(list)
    
    for i in range(n):
        for j in range(n-i-1):
            if list[j] >  list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]

list= deepcopy(list1)
start = time.time()
bubbleSort(list)
bubble = time.time()
print("bubblesort 수행시간 : %f"%(bubble - start))

#Selection sorting (최)소값 중심 정리)

def selectionSort(list):
    for i in range(len(list)):
        min_idx = i
        for j in range(i+1,len(list)):
            if list[min_idx] > list[j]:
                min_idx = j
                
        list[i],list[min_idx] = list[min_idx],list[i]

list= deepcopy(list1)
start = time.time()
selectionSort(list)
select = time.time()
print("selectsort 수행시간 : %f"%(select - start))

#MergeSort
def mergeSort(list):
    if len(list)>1:
        mid = len(list)//2
        L = list[:mid]
        R = list[mid:]
        
        mergeSort(L)
        mergeSort(R)
        
        list.clear()
        while len(L)>0 and len(R) >0:
            if L[0] <= R[0]:
                list.append(L[0])
                L.pop(0)
            else:
                list.append(R[0])
                R.pop(0)
        
        for i in L:
            list.append(i)
        for i in R:
            list.append(i)

list= deepcopy(list1)
start = time.time()
mergeSort(list)
merge = time.time()
print("mergesort 수행시간 : %f"%(merge -start))
  
#Quick sorting
def partition(list,low,high):
    i = low-1
    pivot = list[high]
    
    for j in range(low,high):
        if list[j] <pivot:
            i+=1
            list[i],list[j] = list[j],list[i]
    
    list[i+1],list[high] = list[high],list[i+1]
    return (i+1)

def quicksort(list,low,high):
    if low < high:
        pi = partition(list,low,high)
        quicksort(list,low,pi-1)
        quicksort(list,pi+1,high)
        
list= deepcopy(list1)
n=len(list)
start = time.time()
quicksort(list,0,n-1)        
quick = time.time()
print("quicksort 수행시간 : %f"%(quick - start))

#Heap sorting
def heapify(list,n,i):
    largest = i
    l = 2*i +1
    r = 2*i +2
    
    if l<n and list[i]<list[l]:
        largest = l
    
    if r<n and list[largest]<list[r]:
        largest = r
        
    if largest != i:
        list[i],list[largest] = list[largest],list[i]
        heapify(list,n,largest)
        
def heapsort(list):
    n = len(list)
    for i in range(n//2 - 1,-1,-1):
        heapify(list,n,i)
        
    for i in range(n-1,0,-1):
        list[i],list[0] = list[0],list[i]
        heapify(list,i,0)

list= deepcopy(list1)
start = time.time()
heapsort(list)
heap = time.time()
print("heapsort 수행시간 : %f"%(heap-start))

#특별 정렬 함수 list.sort()
def sorting(list):
    list.sort()

list= deepcopy(list1)
start = time.time()
sorting(list)
sort = time.time()

print("sorting 수행시간 : %f"%(sort-start))