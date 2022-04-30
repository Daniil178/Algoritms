import manage as m
import mmd4
import argparse

def get_hash_tuple(x):
    s = mmd4.extend(x, 128)
    a = int('0b' + s[0:32], 2)
    b = int('0b' + s[32:64], 2)
    c = int('0b' + s[64:96], 2)
    d = int('0b' + s[96:128], 2)
    return (a, b, c, d)


def read_hash_by_file(name):
    with open(name, "r") as f:
        s = f.readline().strip('\n')
        x = int(s, 16)
    return x


def get_hash(v):
    a, b, c, d = v
    s1 = mmd4.extend(a, 32)
    s2 = mmd4.extend(b, 32)
    s3 = mmd4.extend(c, 32)
    s4 = mmd4.extend(d, 32)
    return int('0b' + s1 + s2 + s3 + s4, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", type=str, default=None, help="Enter hash by command prompt")
    parser.add_argument("--f", type=str, default=None, help="Enter hash by file")
    args = parser.parse_args()
    if args.c != None:
        y = int(args.c, 16)
        v = get_hash_tuple(y)
        m.check_variants(v)
        return
    if args.f != None:
        x = read_hash_by_file(args.f)
        v = get_hash_tuple(x)
        m.check_variants(v)
        return
    print("Хеш не определён")
    return


if __name__ == '__main__':
    main()
