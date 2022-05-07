from operator import le

A = bin(0x67452301)[2:]
B = bin(0xEFCDAB89)[2:]
C = bin(0x98BADCFE)[2:]
D = bin(0x10325476)[2:]

def invert(X):
    return X ^ 0b11111111111111111111111111111111

def F(X, Y, Z):
    r1 = int(X, 2) & int(Y, 2)
    r2 = invert(int(X, 2)) & int(Z, 2)
    res = r1 | r2
    return res

def G(X, Y, Z):
    r1 = int(X, 2) & int(Y, 2)
    r2 = int(X, 2) & int(Z, 2)
    r3 = int(Z, 2) & int(Y, 2)
    res = r1 | r2 | r3
    return res

def H(X, Y, Z):
    res = int(X, 2) ^ int(Y, 2) ^ int(Z, 2)
    return res


def add_bits(message):
    if message == "0":
        message = ""
    lmes = len(message)
    message = (message) + '1'
    mod = lmes % 512
    if 448 < mod:
        mod = abs(512 - mod) + 448
    else:
        mod = abs(448 - mod)
    message = message.ljust(lmes + mod, "0")
    return(message)


def add_len(message):
    length = bin(len(message))[2:]
    message = add_bits(message)
    if len(length) > 64:
        length = length[:64]
    else:
        length = length.rjust(64, "0")
    message = message + length[56:] + length[48:56] + length[40:48] + length[32:40] + length[16:32] + length[8:16] + length[:8]
    return message


def bitting(message):
    if isinstance(message, int):
        b = bin(message)[2:]

    else:
        b = bin(int.from_bytes(message.encode(), 'big'))[2:]
    if b == '0':
        b = ''
    m = len(b) % 3
    if m != 0:
        b = b.rjust(len(b) + m, "0")
    length = bin(len(b))[2:]
    message = add_bits(b)
    if len(length) > 64:
        length = length[:64]
    else:
        length = length.rjust(64, "0")
    print(length)
    message = message + length[56:] + length[48:56] + length[40:48] + length[32:40] + length[16:32] + length[8:16] + length[:8]
    return message

def init_m(str):
    m = []
    for i in range(0, 16):
        t = (str[i * 32: (i + 1) * 32])
        m.append(t[24:] + t[16:24] + t[8:16] + t[:8])
    return m

def set_md4(func, a, b, c, d, x, k, s, p):
    a = ((int(a, 2) + func(b, c, d) + int(x[k], 2) + p)) % (2 ** 32)
    a = bin(a)[2:]
    a = a.rjust(32, '0')
    a = a[-32:]
    a = a[s:] + a[:s]

    return a, b, c, d

def set_md4_rev(func, a, b, c, d, x, k, s, p):
    a = a[-s:] + a[:-s]
    a1 = a
    a = ((int(a, 2) - func(b, c, d) - int(x[k], 2) - p)) % (2 ** 32)
    while(a < 0):
        a1 += '1' + a1
        a = ((int(a1, 2) - func(b, c, d) - int(x[k], 2) - p)) % (2 ** 32)

    a = bin(a)[2:]
    a = a.rjust(32, '0')
    a = a[-32:]
    return a, b, c, d

def reverse_steps(hash, X, n, a, b, c, d):

    hash = bin(hash)[2:]
    hash = hash.rjust(128, "0")

    aa = (hash[:32])
    bb = (hash[32:64])
    cc = (hash[64:96])
    dd = (hash[96:])

    aa = aa[24:] + aa[16:24] + aa[8:16] + aa[:8]
    bb = bb[24:] + bb[16:24] + bb[8:16] + bb[:8]
    cc = cc[24:] + cc[16:24] + cc[8:16] + cc[:8]
    dd = dd[24:] + dd[16:24] + dd[8:16] + dd[:8]

    a = bin((int(aa, 2) - int(a, 2)) % 2 ** 32)[2:].rjust(32, "0")
    b = bin((int(bb, 2) - int(b, 2)) % 2 ** 32)[2:].rjust(32, "0")
    c = bin((int(cc, 2) - int(c, 2)) % 2 ** 32)[2:].rjust(32, "0")
    d = bin((int(dd, 2) - int(d, 2)) % 2 ** 32)[2:].rjust(32, "0")

    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 15, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 7, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 11, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 3, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 13, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 5, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 9, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 1, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 14, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 6, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 10, 9, n)
    a, b, c, d = set_md4_rev(H, a, b, c, d, X, 2, 3, n)
    b, c, d, a = set_md4_rev(H, b, c, d, a, X, 12, 15, n)
    c, d, a, b = set_md4_rev(H, c, d, a, b, X, 4, 11, n)
    d, a, b, c = set_md4_rev(H, d, a, b, c, X, 8, 9, n)

    return a, b, c, d

def md4_half_hash(a, b, c, d, X, m, n):
    a, b, c, d = set_md4(F, a, b, c, d, X, 0, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 1, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 2, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 3, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 4, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 5, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 6, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 7, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 8, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 9, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 10, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 11, 19, 0)
    a, b, c, d = set_md4(F, a, b, c, d, X, 12, 3, 0)
    d, a, b, c = set_md4(F, d, a, b, c, X, 13, 7, 0)
    c, d, a, b = set_md4(F, c, d, a, b, X, 14, 11, 0)
    b, c, d, a = set_md4(F, b, c, d, a, X, 15, 19, 0)

    a, b, c, d = set_md4(G, a, b, c, d, X, 0, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 4, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 8, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 12, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 1, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 5, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 9, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 13, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 2, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 6, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 10, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 14, 13, m)
    a, b, c, d = set_md4(G, a, b, c, d, X, 3, 3, m)
    d, a, b, c = set_md4(G, d, a, b, c, X, 7, 5, m)
    c, d, a, b = set_md4(G, c, d, a, b, X, 11, 9, m)
    b, c, d, a = set_md4(G, b, c, d, a, X, 15, 13, m)

    a, b, c, d = set_md4(H, a, b, c, d, X, 0, 3, n)

    return a, b, c, d

N = 0x6ED9EBA1
M = 0x5A827999


def md4_hash(str, a, b, c, d):
    N = len(str)
    for i in range(0, N // (16 * 32)):
        X = init_m(str[i * 512: (i + 1) * 512])

        aa = a
        bb = b
        cc = c
        dd = d

        m = 0x5A827999
        n = 0x6ED9EBA1

        a, b, c, d = set_md4(F, a, b, c, d, X, 0, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 1, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 2, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 3, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 4, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 5, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 6, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 7, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 8, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 9, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 10, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 11, 19, 0)
        a, b, c, d = set_md4(F, a, b, c, d, X, 12, 3, 0)
        d, a, b, c = set_md4(F, d, a, b, c, X, 13, 7, 0)
        c, d, a, b = set_md4(F, c, d, a, b, X, 14, 11, 0)
        b, c, d, a = set_md4(F, b, c, d, a, X, 15, 19, 0)

        a, b, c, d = set_md4(G, a, b, c, d, X, 0, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 4, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 8, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 12, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 1, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 5, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 9, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 13, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 2, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 6, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 10, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 14, 13, m)
        a, b, c, d = set_md4(G, a, b, c, d, X, 3, 3, m)
        d, a, b, c = set_md4(G, d, a, b, c, X, 7, 5, m)
        c, d, a, b = set_md4(G, c, d, a, b, X, 11, 9, m)
        b, c, d, a = set_md4(G, b, c, d, a, X, 15, 13, m)

        a, b, c, d = set_md4(H, a, b, c, d, X, 0, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 8, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 4, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 12, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 2, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 10, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 6, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 14, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 1, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 9, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 5, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 13, 15, n)
        a, b, c, d = set_md4(H, a, b, c, d, X, 3, 3, n)
        d, a, b, c = set_md4(H, d, a, b, c, X, 11, 9, n)
        c, d, a, b = set_md4(H, c, d, a, b, X, 7, 11, n)
        b, c, d, a = set_md4(H, b, c, d, a, X, 15, 15, n)
        
        a = bin((int(a, 2) + int(aa, 2)) % 2 ** 32)[2:].rjust(32, "0")
        b = bin((int(b, 2) + int(bb, 2)) % 2 ** 32)[2:].rjust(32, "0")
        c = bin((int(c, 2) + int(cc, 2)) % 2 ** 32)[2:].rjust(32, "0")
        d = bin((int(d, 2) + int(dd, 2)) % 2 ** 32)[2:].rjust(32, "0")

        a = a[24:] + a[16:24] + a[8:16] + a[:8]
        b = b[24:] + b[16:24] + b[8:16] + b[:8]
        c = c[24:] + c[16:24] + c[8:16] + c[:8]
        d = d[24:] + d[16:24] + d[8:16] + d[:8]
        
    return(a + b + c + d)

def hsh(passw):
    k = bitting(passw)
    print(k)
    hash = md4_hash(k, A, B, C, D)
    hash = hex(int(hash, 2))
    print("hash", hash)

#print("Input pass")
#hsh(input())
