import collections
import hashlib
import inspect
import os
import string
import sys
import re

if len(sys.argv) != 3:
    sys.exit('search orig_dir dup_dir')

orig_dir = sys.argv[1]
dup_dir = sys.argv[2]

def d(*args):
    print str(inspect.currentframe().f_back.f_lineno) + ':', \
        ' '.join(str(x) for x in args)

def hash_file(fname, only_head):
    f = open(fname, 'rb')
    h = hashlib.sha256()
    bs = 4096 if only_head else 1048576
    while True:
        b = f.read(bs)
        if len(b) <= 0 or only_head:
            break
        h.update(b)
    f.close()
    return h.digest()

def _move_dup(dup):
    new = os.path.join(dup_dir, re.sub(r'/', '_', dup))
    if os.path.isfile(new):
        print(new + ': exists')
        raise ValueError(dup)
    os.rename(dup, new)

def walk(topdir):
    partial = {}
    have_full = {}
    full = {}
    for root, dirs, files in os.walk(topdir):
        for fn in files:
            n = os.path.join(root, fn)
            h = hash_file(n, True)
            if h not in partial:
                partial[h] = n
                continue
            hf = hash_file(n, False)
            have_full[n] = hf
            o = partial[h]
            if o not in have_full:
                of = hash_file(o, False)
                have_full[o] = of
                full[of] = o
            if hf in full:
                _move_dup(n)
            else:
                full[hf] = n

walk(orig_dir)
