import collections
import hashlib
import inspect
import os
import string
import sys

def d(*args):
    print str(inspect.currentframe().f_back.f_lineno) + ':', \
        ' '.join(str(x) for x in args)

def detect(orig, check):
    res = list()
    for k in check.keys():
        if k in orig:
            res.extend(check[k])
    return res

def full_hash(files):
    map = collections.defaultdict(list)
    for f in files:
        map[hash_file(f, False)].append(f)
    return map

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

def walk(topdir):
    map = collections.defaultdict(list)
    for root, dirs, files in os.walk(topdir):
        for fn in files:
            n = os.path.join(root, fn)
            h = hash_file(n, True)
            map[h].append(n)
    return map

if len(sys.argv) != 3:
    sys.exit('seach orig_dir dup_dir')

orig = walk(sys.argv[1])
check = walk(sys.argv[2])

dup = list()
for k in check.keys():
    if k in orig:
        dup.extend(detect(full_hash(orig[k]), full_hash(check[k])))

dup.sort();
for f in dup:
    print(f)
