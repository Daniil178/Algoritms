PROCESS = 4

def prefix(s):
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k > 0 and s[k] != s[i]:
            k = pi[k - 1]
        if s[k] == s[i]:
            k += 1
        pi[i] = k
    return pi

def kmp(patt, s):
    offsets = []
    pi = prefix(patt)
    k = 0
    for i in range(len(s)):
        while k > 0 and s[i] != patt[k]:
            k = pi[k - 1]
        if patt[k] == s[i]:
            k += 1
        if k == len(patt):
            offsets.append(i - len(patt) + 1)
            k = pi[k - 1]
    return offsets

def equal(hsh, adr, file):
    file.seek(adr//8)
    pat = file.read(1)
    pat_hsh = bin(int.from_bytes(pat, "big"))[2:]
    pat_hsh = '0' * (8 - len(pat_hsh)) + pat_hsh
    if pat_hsh[adr % 8] == '1':
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
