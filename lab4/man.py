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
    byte = [0] * 2**11
    for adr in dict_hashes:
        # gen_hsh = 0
        # for patt in dict_hashes[adr]:
        #     gen_hsh |= patt[1]
        byte[adr] = 1#gen_hsh
    with open(filename, "wb") as f:
        f.write(bytes(byte))
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
    parser.add_argument('-t', '--text', type=str,
                        help='text file')
    parser.add_argument('-p', '--pat', type=str,
                        help='pattern file')
    args = vars(parser.parse_args())

    if(args['text']):
        text_file = args['text']

    if(args['pat']):
        file_name = args['pat']



def main():
    file_name = './patterns.txt'
    text_file = './text.txt'
    dict_hashes = {}
    #dict hash: {adress: (str, hash)}
    # parse_args(text_file, file_name)
    patt_len = create_patt_hashes(file_name, dict_hashes)
    blum_file = create_blum(dict_hashes)
    
    with open(text_file, "r") as file:
        text = file.read()

    with open(blum_file, "rb") as file:
        #prc = []
        processing(0, len(text), patt_len, text, file, dict_hashes)

        for j in range(0, PROCESS):
            prc.append(0)
            prc[j] = Process(target=processing, args=(j, len(text),
                           patt_len, text, file, dict_hashes))

        for j in range(0, PROCESS):
            prc[j].start()

        for j in range(0, PROCESS):
            prc[j].join()
    

if __name__ == '__main__':
    main()