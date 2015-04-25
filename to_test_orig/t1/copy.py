import sys
import hashlib
import os
import collections
import string

def hashfile(fname, onlyhead):
    f = open(fname, 'rb')
    h = hashlib.sha256()
    bs = 4096 if onlyhead else 1048576
    while True:
        b = f.read(bs)
        if b <= 0 or onlyhead:
            break
        h.update(b)
    f.close()
    return h.digest()

def walk(topdir):
    map = collections.defaultdict(list)
    for root, dirs, files in os.walk(topdir):
        for fn in files:
            n = os.path.join(root, fn)
            h = hashfile(n, True)
            map[h].append(n)
    return map

def listfull(files):
    map = collections.defaultdict(list)
    for f in files:
        map[hashfile(f, False)].append(f)
    return map

def compare(orig, check):
    res = list
    for k in check.keys():
        if k in orig:
            list.extend(check[k])
    return list

if len(sys.argv) != 2:
    print(__filename__, ": orig_dir dup_dir")
    sys.exit(1);

orig = walk(sys.argv[0])
check = walk(sys.argv[1])

dup = list
for k in check.keys():
    if k in orig:
        dup.extend(detect(listfull(orig[k]), listfull(check[k])))

for f in dup.sort():
    print(f)
