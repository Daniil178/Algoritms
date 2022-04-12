PROCESS = 4

def equal(hsh, adr, file):
    file.seek(adr)
    pat = file.read(1)
    pat_hsh = int.from_bytes(pat, "big")
    if pat_hsh == 1:
        return True
    else:
        return False

def find(first, text, len, pat_len, blum_file):
    strs_adr_hsh_offset = [] #[(str, adr, hsh, offset)...]
    for index in range(first, len - pat_len + 1, PROCESS):
        string = text[index:index + pat_len]
        hashs = bin(hash(string))[3:]
        adr = int(hashs[:11], 2)
        hsh = int(hashs[11:19], 2)
        if equal(hsh, adr, blum_file):
            strs_adr_hsh_offset.append((string, adr, hsh, index))
    return strs_adr_hsh_offset