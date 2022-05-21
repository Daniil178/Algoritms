import count as cnt
from multiprocessing import Process
import argparse

PROCESS = 4

def processing(first, len_txt, patt_len, text, blum_file, dict_hashes):
    strs_adr_hsh_offset = cnt.find(first, text, len_txt, patt_len, blum_file)
    for candidate in strs_adr_hsh_offset:
        for pat in dict_hashes[candidate[1]]:
            if pat[1] == candidate[2] and pat[0] == candidate[0]:
                print(pat[0], candidate[3])
    return

def create_blum(dict_hashes):
    filename = "blum.bin"
    byte = [0] * 2**14
    bt = [0] * 2**11
    for adr in dict_hashes:
        byte[adr] = 1
    for i in range(2**11):
        b = 0
        for j in range(8):
            b += byte[i * 8 + j] * 2**(7 - j)
        bt[i] = b
    with open(filename, "wb") as f:
        f.write(bytes(bt))
    return filename

def create_patt_hashes(filename, dict_hashes):
    with open(filename, "r") as f:
            for line in f:
                patt_len = len(line[:-1])
                hash_patt = bin(hash(line[:-1]))[3:]
                adr = int(hash_patt[:11], 2)
                hsh = int(hash_patt[11:19], 2)
                if adr in dict_hashes:
                    dict_hashes[adr].append((line[:-1], hsh))
                else:
                    dict_hashes[adr] = []
                    dict_hashes[adr].append((line[:-1], hsh))
    return patt_len

def parse_args(text_file, file_name):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str, help='text file')
    parser.add_argument('-p', '--pat', type=str, help='pattern file')
    parser.add_argument('-k', '--kmp', action='store_true', help='set kmp algoritm', required=False)
    args = parser.parse_args()
    types = 'b'

    if args.text:
        text_file[0] = args.text

    if args.pat:
        file_name[0] = args.pat
    
    if args.kmp:
        types = 'k'

    return text_file[0], file_name[0], types



def main():
    file_name = "./patterns.txt"
    text_file = "./text.txt"
    dict_hashes = {}
    #dict hash: {adress: (str, hash)}
    text_file, file_name, types = parse_args([text_file], [file_name])
    patt_len = create_patt_hashes(file_name, dict_hashes)
    blum_file = create_blum(dict_hashes)
    
    with open(text_file, "r") as file:
        text = file.read()

    if types == 'b':
        with open(blum_file, "rb") as file:
            prc = []
            processing(0, len(text), patt_len, text, file, dict_hashes)

            for j in range(0, PROCESS):
                prc.append(0)
                prc[j] = Process(target=processing, args=(j, len(text),
                            patt_len, text, file, dict_hashes))

            for j in range(0, PROCESS):
                prc[j].start()

            for j in range(0, PROCESS):
                prc[j].join()
    else:
        with open(file_name, 'r') as f:
            patts = f.read()
        patts = patts.split()
        for patt in patts:
            offsets = cnt.kmp(patt, text)
            for offset in offsets:
                print(patt, offset)

if __name__ == '__main__':
    main()
