import mmd4


def md4_strip(key):
    y = mmd4.extend(key, 64)
    x = mmd4.addbits(y)
    x = mmd4.addlen(x, 64)
    m = mmd4.splitbits(x)
    words = [0] * 16
    a = mmd4.A
    b = mmd4.B
    c = mmd4.C
    d = mmd4.D
    for j in range(16):
        words[j] = m[j]
    a, b, c, d = mmd4.round1(a, b, c, d, words)
    a, b, c, d = mmd4.round2(a, b, c, d, words)
    a = mmd4.func(a, b, c, d, mmd4.H, (words[0] + 0x6ED9EBA1) % (1 << 32), 3)
    return (a, b, c, d)


def isequal(prev_hash_vec, key, img_hash_cort):
    a, b, c, d = md4_strip(key)
    v1 = (a, b, c, d)
    if v1 != prev_hash_vec:
        return False
    y = mmd4.extend(key, 64)
    x = mmd4.addbits(y)
    x = mmd4.addlen(x, 64)
    m = mmd4.splitbits(x)
    words = [0] * 16
    for i in range(16):
        words[i] = m[i]
    a = mmd4.inv_func(a, b, c, d, mmd4.H, (words[0] + 0x6ED9EBA1) % (1 << 32), 3)
    a, b, c, d = mmd4.block_h(a, b, c, d, words)
    a += mmd4.A
    a = a % (1 << 32)
    b += mmd4.B
    b = b % (1 << 32)
    c += mmd4.C
    c = c % (1 << 32)
    d += mmd4.D
    d = d % (1 << 32)
    v1 = (a, b, c, d)
    if v1 == img_hash_cort:
        return True
    else:
        return False


def enumerate(const_32b, prev_hash, image_hash):
    N = 1 << 32
    i = 0
    c = mmd4.extend(const_32b, 32)
    while i < N:
        j = mmd4.extend(i, 32)
        key = int('0b' + j + c, 2)
        flag = isequal(prev_hash, key, image_hash)
        if flag:
            print("Прообраз найден: " + bin(key))
            return True
        i += 1
    return False
