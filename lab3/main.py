import random
import argparse
import time

def mod_exp(a, b, n):
    c = 0
    d = 1
    s = bin(b)
    l = len(s)
    for i in range(2, l):
        c = 2 * c
        d = (d * d) % n
        if s[i] == '1':
            c = c + 1
            d = (d * a) % n
    return d


def witness(a, n):
    if n == 2:
        return False
    if n % 2 == 0:
        return True
    b = bin(n - 1)
    k = 0
    q = 1
    for i in range(len(b), 2):
        if b[i] == '0':
            k = k + 1
            q << 2
        else:
            break
    u = (int)((n - 1) / q)
    x = mod_exp(a, u, n)
    for i in range(0, k):
        prev = x
        x = (x ** 2) % n
        if x == 1 and prev != 1 and prev != n - 1:
            return True
    if x != 1:
        return True
    return False


def miller_rabin(n, s):
    for i in range(0, s):
        a = random.randint(1, n - 1)
        if witness(a, n):
            return False  # составное
    return True  # простое


def gcd(a, b):
    s = a
    r = b
    while r != 0:
        u = s % r
        s = r
        r = u
    return s


def pollard_rho(n):
    i = 1
    x = random.randint(0, n + 1)
    y = x
    cycle = []
    k = 2
    while True:
        i = i + 1
        if x % n in cycle:
            return n
        else:
            cycle.append(x % n)
        x = (x * x - 1) % n
        d = gcd(y - x, n)
        if d != 1 and d != n:
            return d
        if i == k:
            y = x
            k = 2 * k


def getprimedegree(p, n):
    s = p
    r = n % p
    k = 0
    while r == 0:
        k = k + 1
        s = s * p
        r = n % s
    return (k, (int)(s / p))


def factorize(n):
    primes = dict()
    N = n
    if N % 2 == 0:
        c = getprimedegree(2, N)
        primes[2] = c[0]
        N = (int)(N / c[1])
    while N > 1:
        if not miller_rabin(N, 3):
            d = pollard_rho(N)
            while not miller_rabin(d, 3):
                d = pollard_rho(d)
            if d not in primes.keys():
                c = getprimedegree(d, N)
                primes[d] = c[0]
                N = (int)(N / c[1])
        else:
            primes[N] = 1
            N = 1
    return primes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--dec', type=int,
                        help='a decimal integer')
    parser.add_argument('-e', '--hex', type=str,
                        help='a hexadecimal integer')
    args = vars(parser.parse_args())
    t = time.time_ns()
    if(args['hex']):
        num = int(args['hex'], 16)
    elif(args['dec']):
        num = args['dec']
    primes = factorize(num)
    t = time.time_ns() - t
    print(f'{num}: {primes}')
    print('Time: %0.9f' %((float)(t / 1000000000.0)))
