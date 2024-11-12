def ex1(n):
    k = n/2
    return k

def ex2(n):
    sum = 0
    for i in range(1, n):
        sum += i
    return sum

def ex3(n):
    sum = 0
    for i in range(1, n):
        for j in range(1, n):
            sum += i*j
    return sum

print(ex3(6))