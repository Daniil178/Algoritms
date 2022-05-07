import os
import sys

import mmd4 as md4
from multiprocessing import Pool


def fun(hsh):
    pa, pb, pc, pd, i, hash = hsh
    t = 0
    while t < (1 << 32):
        first = bin(t)[2:].rjust(32, "0")
        second = bin(i)[2:].rjust(32, "0")
        str1 = str = first + second
        str = md4.add_len(str)
        X = md4.init_m(str)
        aa, bb, cc, dd = md4.md4_half_hash(md4.A, md4.B, md4.C, md4.D, X, md4.M, md4.N)
        if aa == pa and bb == pb and cc == pc and dd == pd:
            if hex(int(md4.md4_hash(str, md4.A, md4.B, md4.C, md4.D), 2)) == hex(hash):

                print('found password', first + second)

                return True
        t += 1


def main():
    if (len(sys.argv) > 1):
        hash = sys.argv[1]
        hash = (int(hash, 16))
    else:
        print("usage\npython main.py hash")
        return None
    print("given hash:", hex(hash))
    num = os.cpu_count() - 1
    
    i = 0
    end_flag = False
    args = [None] * num
    while i < (1 << 32) and not end_flag:
        
        with Pool(processes=num ) as pool:
            
            for j in range(num):
                
                t = 0
                first = bin(t)[2:].rjust(32, "0")
                second = bin(j)[2:].rjust(32, "0")
                str1 = str = first + second
                str = md4.add_len(str)
                X = md4.init_m(str)
                
                pa, pb, pc, pd = md4.reverse_steps(hash, X, md4.N, md4.A, md4.B, md4.C, md4.D)
                
                args[j] = pa, pb, pc, pd, j, hash
            
            for r in pool.imap_unordered(fun, args):
                if r:
                    pool.terminate()
                    end_flag = True
                    break
        i += 1
    if not end_flag:
        print('Nothing found')


if __name__ == '__main__':
    main()
