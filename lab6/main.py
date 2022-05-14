from time import time
from random import randint
import argparse
from multiprocessing import Process, Pool

def genMatrix(n):
    A = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = randint(0, 100)
    return A

def log(x):
    x -= 1
    res = 0
    while(x != 0):
        x >>= 1
        res += 1
    return res

def newDem(x):
    return 1 << log(x)

def addZero(A):
    leng = len(A[0])
    dem = newDem(leng)
    size = dem - leng
    for i in range(leng):
        A[i] += [0] * size
    for i in range(size):
        A.append([0] * dem)

def arrayCopy(src, srcPos, dest, destPos, length):
    for i in range(length):
        dest[i + destPos] = src[i + srcPos]

def splitMatrix(A):
    n = len(A) >> 1
    a11 = [[0] * n for i in range(n)]
    a12 = [[0] * n for i in range(n)]
    a21 = [[0] * n for i in range(n)]
    a22 = [[0] * n for i in range(n)]
    for i in range(n):
        arrayCopy(A[i], 0, a11[i], 0, n)
        arrayCopy(A[i], n, a12[i], 0, n)
        arrayCopy(A[i + n], 0, a21[i], 0, n)
        arrayCopy(A[i + n], n, a22[i], 0, n)
    return a11, a12, a21, a22

def collectMatrix(a11, a12, a21, a22):
    n = len(a11)
    n1 = n << 1
    A = [[0] * n1 for i in range(n1)]
    for i in range(n):
        arrayCopy(a11[i], 0, A[i], 0, n)
        arrayCopy(a12[i], 0, A[i], n, n)
        arrayCopy(a21[i], 0, A[i + n], 0, n)
        arrayCopy(a22[i], 0, A[i + n], n, n)
    return A

def sqMultiply(A, B, n):
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k]*B[k][j]
    return C

def summ(A, B, n):
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def sub(A, B, n):
    C = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def Strassen(A, B, n):
    if n <= 64:
        return sqMultiply(A, B, n)
    n = n >> 1
    
    a11, a12, a21, a22 = splitMatrix(A)
    b11, b12, b21, b22 = splitMatrix(B)

    p1 = Strassen(summ(a11, a22, n), summ(b11, b22, n), n)
    p2 = Strassen(summ(a21, a22, n), b11, n)
    p3 = Strassen(a11, sub(b12, b22, n), n)
    p4 = Strassen(a22, sub(b21, b11, n), n)
    p5 = Strassen(summ(a11, a12, n), b22, n)
    p6 = Strassen(sub(a21, a11, n), summ(b11, b12, n), n)
    p7 = Strassen(sub(a12, a22, n), summ(b21, b22, n), n)
    
    c11 = summ(summ(p1, p4, n), sub(p7, p5, n), n)
    c12 = summ(p3, p5, n)
    c21 = summ(p2, p4, n)
    c22 = summ(sub(p1, p2, n), summ(p3, p6, n), n)
    C = collectMatrix(c11, c12, c21, c22)
    return C

def multiStrassen(A, B, n):
    if n <= 64:
        return sqMultiply(A, B, n)
    n = n >> 1
    
    a11, a12, a21, a22 = splitMatrix(A)
    b11, b12, b21, b22 = splitMatrix(B)

    #p1 = Process(target=Strassen, args=(summ(a11, a22, n), summ(b11, b22, n), n))
    #p2 = Process(target=Strassen, args=(summ(a21, a22, n), b11, n))    
    #p3 = Process(target=Strassen, args=(a11, sub(b12, b22, n), n))
    #p4 = Process(target=Strassen, args=(a22, sub(b21, b11, n), n))
    #p5 = Process(target=Strassen, args=(summ(a11, a12, n), b22, n))
    #p6 = Process(target=Strassen, args=(sub(a21, a11, n), summ(b11, b12, n), n))
    #p7 = Process(target=Strassen, args=(sub(a12, a22, n), summ(b21, b22, n), n))

    #p1.start(), p2.start(), p3.start(), p4.start(), p5.start(), p6.start(), p7.start()
    #p1.join(),p2.join(), p3.join(), p4.join(), p5.join(), p6.join(), p7.join()
    p = list()
    with Pool(processes=7) as pool:
        tasks = [(summ(a11, a22, n), summ(b11, b22, n), n), (summ(a21, a22, n), b11, n), (a11, sub(b12, b22, n), n), (a22, sub(b21, b11, n), n), (summ(a11, a12, n), b22, n), (sub(a21, a11, n), summ(b11, b12, n), n), (sub(a12, a22, n), summ(b21, b22, n), n)]
        for i in pool.map(Strassen, [k for k in tasks]):
            p.append(i)
    c11 = summ(summ(p[1], p[4], n), sub(p[7], p[5], n), n)
    c12 = summ(p[3], p[5], n)
    c21 = summ(p[2], p[4], n)
    c22 = summ(sub(p[1], p[2], n), summ(p[3], p[6], n), n)
    C = collectMatrix(c11, c12, c21, c22)
    return C

        

def main():
    parser = argparse.ArgumentParser(description='Strassen Algoritm')
    parser.add_argument('-n', '--dimension', type=int, help='dimension of matrix`s for generate')
    args = parser.parse_args()

    n = args.dimension
    A = genMatrix(n)
    B = genMatrix(n)
    addZero(A)
    addZero(B)	
    t0 = time()
    C = multiStrassen(A, B, len(A))
    t0 = time() - t0
    
    t = time()
    C = Strassen(A, A, len(A))
    t = time() - t
    for i in range(n):
        C[i] = C[i][:n]
    C = C[:n]
    
    t1 = time()
    C1 = sqMultiply(A, A, n)
    t1 = time() - t1
    with open("tests", "a") as f:
        f.write(f"{n}, {t0}, {t}, {t1}, {C==C1}\n")

if __name__ == '__main__':
    main()
