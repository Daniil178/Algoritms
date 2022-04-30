import mmd4
import count as co
from multiprocessing import Pool

CORES_NUMBER = 4


def md4_part_inv(img_hash, key):
    resa, resb, resc, resd = img_hash
    y = mmd4.extend(key, 64)
    x = mmd4.addbits(y)
    x = mmd4.addlen(x, 64)
    m = mmd4.splitbits(x)
    words = [0] * 16
    N = 1 << 32
    for i in range(16):
        words[i] = m[i]
    resd = (resd - mmd4.D) % N
    resc = (resc - mmd4.C) % N
    resb = (resb - mmd4.B) % N
    resa = (resa - mmd4.A) % N
    resa, resb, resc, resd = mmd4.inv_round3(resa, resb, resc, resd, words)
    return (resa, resb, resc, resd)


def work(v):
    i, prev_hash, image_hash = v
    f = co.enumerate(i, prev_hash, image_hash)
    return f


def check_variants(image_hash):
    N = 1 << 32
    i = 0
    end_flag = False
    args = [None] * CORES_NUMBER
    while i < N and not end_flag:
        with Pool(processes=CORES_NUMBER) as pool:
            for j in range(CORES_NUMBER):
                prev_hash = md4_part_inv(image_hash, i)
                args[j] = (i, prev_hash, image_hash)
                i += 1
            for r in pool.imap_unordered(work, args):
                if r:
                    pool.terminate()
                    end_flag = True
                    break
    if not end_flag:
        print('Прообраз не найден')
    return 0
