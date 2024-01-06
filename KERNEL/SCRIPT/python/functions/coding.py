import json
import hashlib
from random import choice
from string import ascii_uppercase

md5 = lambda s: hashlib.md5(s).hexdigest()
sha1 = lambda s: hashlib.sha1(s.encode('utf-8')).hexdigest()
sha256 = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
obj2str = lambda o: sha1(json.dumps(o, sort_keys=True))
sha1_strlist = lambda sl: sha1('|'.join(sorted(sl)))
random_string = lambda L=32: ''.join(choice(ascii_uppercase) for i in range(L))

if __name__ == '__main__':
    # TEST 0
    s = random_string()
    print(f's={s}')
    print(sha1(s))
    print('obj2str 1)', obj2str(dict(s=s, sha1=sha1(s))))
    print('obj2str 2)', obj2str(dict(s=s, sha1=sha1(s))))

    # TEST 1
    L1 = ['ali', 'sasan', 'nazi']
    L2 = ['ali', 'sasan', 'nazi']
    # L2 = ['nazi', 'ali', 'sasan']
    print('L1', L1)
    print('L2', L2)
    print('-'*30)
    print('01)', sha1('|'.join(L1)))
    print('02)', sha1('|'.join(L1)))
    print('03)', sha1('|'.join(L2)))
    print('04)', sha1('|'.join(L2)))
    print('-'*30) # mesale naghz natonestam peida konam vali motmanem set bug dare.
    print('05)', sha1('|'.join(set(L1))))
    print('06)', sha1('|'.join(set(L1))))
    print('07)', sha1('|'.join(set(L2))))
    print('08)', sha1('|'.join(set(L2))))
    print('-'*30) # dar har sorat sorted doeost kar mikone.
    print('09)', sha1('|'.join(sorted(L1))))
    print('10)', sha1('|'.join(sorted(L1))))
    print('11)', sha1('|'.join(sorted(L2))))
    print('12)', sha1('|'.join(sorted(L2))))
    print('13)', sha1_strlist(L1))
    print('14)', sha1_strlist(L1))
    print('15)', sha1_strlist(L2))
    print('16)', sha1_strlist(L2))