from token_list import token_list
from token_parser import parse
import pickle

def main():
    t0 = 'pass0.json'
    ts = token_list(t0)
    o = parse(ts)
    # print('log parse',o)
    for k, v in o.items():
        print('{} : {}'.format(k, v))

if __name__ == '__main__':
    main()
