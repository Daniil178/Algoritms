A = 0x76543210
B = 0xfedcba98
C = 0x98abcdef
D = 0x01234567


def invert(x):
    res = (1 << 32) - x - 1
    return res


def F(x, y, z):
    return (x & y) | (invert(x) & z)


def G(x, y, z):
    return (x & y) | (x & z) | (y & z)


def H(x, y, z):
    return x ^ y ^ z


def addbits(bin_str):
    bin_str += '1'
    lenstr = len(bin_str)
    if lenstr % 512 <= 448:
        bin_str += '0' * (448 - lenstr % 512)
    else:
        bin_str += '0' * (448 + 512 - lenstr % 512)
    return bin_str


def addlen(bin_str, l):
    # l - length in bits
    res = bin_str
    lbin = bin(l)[2:]
    length = len(lbin)
    d = 64 - length
    if d < 0:
        d = 0
    lbin = '0' * d + lbin
    res += lbin[-32:] + lbin[-64:-32]
    return res


def splitbits(strbits):
    b = list()
    n = len(strbits) // 32
    j = 0
    for i in range(n):
        j = i * 32
        b.append(int('0b' + strbits[j:j + 32], 2))
    return b


def extend(x, bits):
    b = bin(x)[2:]
    if len(b) <= bits:
        res = '0' * (bits - len(b)) + b
    else:
        res = b[len(b) - bits:len(b)]
    return res


def rot_left(x, s):
        x = int(x, 2)
        l, r = (x << s) & 0xFFFFFFFF, x >> (32 - s)
        return l | r

def rot_right(x, s):
        x = int(x, 2)
        l, r = x >> s, (x << (32 - s)) & 0xFFFFFFFF
        return l | r

def func(a, b, c, d, R, xk, s):
    res = (a + R(b, c, d) + xk) % (1 << 32)
    res = extend(res, 32)
    res = rot_left(res, s)
    return res


def inv_func(y, b, c, d, R, xk, s):
    f = extend(y, 32)
    prev_y = (rot_right(f, s) - R(b, c, d) - xk) % (1 << 32)
    return prev_y


def round1(a, b, c, d, X):
    reg = X.copy()
    for i in range(4):
        a = func(a, b, c, d, F, reg[i * 4], 3)
        d = func(d, a, b, c, F, reg[i * 4 + 1], 7)
        c = func(c, d, a, b, F, reg[i * 4 + 2], 11)
        b = func(b, c, d, a, F, reg[i * 4 + 3], 19)
    return a, b, c, d

def round2(a, b, c, d, X):
    reg = X.copy()
    for i in range(16):
        reg[i] = (reg[i] + 0x5A827999) % (1 << 32)
    for i in range(4):
        a = func(a, b, c, d, G, reg[i], 3)
        d = func(d, a, b, c, G, reg[i + 4], 5)
        c = func(c, d, a, b, G, reg[i + 8], 9)
        b = func(b, c, d, a, G, reg[i + 12], 13)
    return a, b, c, d

def round3(a, b, c, d, X):
    reg = X.copy()
    for i in range(16):
        reg[i] = (reg[i] + 0x6ED9EBA1) % (1 << 32)
    for i in [0, 2, 1, 3]:
        a = func(a, b, c, d, H, reg[i], 3)
        d = func(d, a, b, c, H, reg[i + 8], 9)
        c = func(c, d, a, b, H, reg[i + 4], 11)
        b = func(b, c, d, a, H, reg[i + 12], 15)
    return a, b, c, d


def inv_round3(ra, rb, rc, rd, w):
    reg = w.copy()
    for i in range(16):
        reg[i] = (reg[i] + 0x6ED9EBA1) % (1 << 32)
    for i in [3, 1, 2, 0]:
        rb = inv_func(rb, rc, rd, ra, H, reg[i + 12], 15)
        rc = inv_func(rc, rd, ra, rb, H, reg[i + 4], 11)
        rd = inv_func(rd, ra, rb, rc, H, reg[i + 8], 9)
        if i != 0:
            ra = inv_func(ra, rb, rc, rd, H, reg[i], 3)
    return (ra, rb, rc, rd)


def md4(key, keylen=64):
    y = extend(key, keylen)
    x = addbits(y)
    x = addlen(x, keylen)
    m = splitbits(x)
    words = [0] * 16
    n = (int)(len(m) / 16)
    a = A  # a0
    b = B  # b0
    c = C  # c0
    d = D  # d0
    for i in range(n):
        for j in range(16):
            words[j] = m[i * 16 + j]
        aa = a  # ai-1
        bb = b  # bi-1
        cc = c  # ci-1
        dd = d  # di-1
        a, b, c, d = round1(a, b, c, d, words)
        a, b, c, d = round2(a, b, c, d, words)
        a, b, c, d = round3(a, b, c, d, words)
        a += aa  # a2 = a1bl + a0 (ai+1 = aibl + ai-1, i = 1,2,3,...)
        a = a % (1 << 32)
        b += bb  # b1bl + b0
        b = b % (1 << 32)
        c += cc  # c1bl + c0
        c = c % (1 << 32)
        d += dd  # d1bl + d0
        d = d % (1 << 32)
    return (a, b, c, d)


def get_hash_tuple(x):
    s = bin(x)[2:len(bin(x))]
    a = int('0b' + s[0:32])
    b = int('0b' + s[32:64])
    c = int('0b' + s[64:96])
    d = int('0b' + s[96:128])
    return (a, b, c, d)
