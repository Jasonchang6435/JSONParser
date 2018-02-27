from token_type import Type
from token import Token


def load_file(path):
    with open(path) as f:
        return f.read()


def number_end(s1, offset):
    """
    现在只能解析普通数字
    小数 负数 都不能解析
    """
    digits = '1234567890'
    for i, c in enumerate(s1[offset:]):
        if c not in digits:
            return i
    print('** 错误, 数字解析错误')


def string_end(s1, offset):
    """
    bfnrt \ / "
    """
    bs = {
        'b': '\b',
        'f': '\f',
        'n': '\n',
        'r': '\r',
        't': '\t',
        '/': '/',
        '"': '"',
        '\\': '\\',
    }
    res = ''
    i = offset

    while i < len(s1):
        a = s1[i]
        if a == '"':
            return (res, i)
        elif a == '\\':
            b = s1[i+1]
            if b in bs:
                res += bs[b]
                i += 2
            else:
                print('** 错误, 不合法的转义字符: ', a + b )
                example = '\\b \\f \\n \\r \\t \\/ \\" \\\\'
                print('合法的转义字符是: ', example)
                return ('', -1)
        else:
            res += a
            i += 1
    # return s1[offset:].find('"')
    return (res, i)


def loads(code):
    s = 0
    i = 0
    length = len(code)
    tokens = []
    spaces = ' \b\f\n\r\t'
    digits = '0123456789'

    is_open = True
    while i < length:
        c = code[i]
        i += 1
        if c in spaces:
            continue
        elif c in ':,[]{}':
            t = Token(Type.auto, c)
            tokens.append(t)
        elif c == '"' and is_open:
            # 吃字符串
            # offset = string_end(code, i)
            result, index = string_end(code, i)
            if index != -1:
                t = Token(Type.string)
                # t.value = code[i:i+offset]
                t.value = result
                # i += offset + 1
                i = index
                tokens.append(t)
                is_open = not is_open
            else:
                return
        elif c == '"' and not is_open:
            is_open = not is_open
            continue
        elif c in digits:
            # 吃数字
            offset = number_end(code, i)
            t = Token(Type.number)
            # todo, 可能是 float, 要判断
            t.value = int(code[i-1:i+offset])
            i += offset
            tokens.append(t)
        elif c in 'tfn':
            # true false null
            kvs = dict(
                t='true',
                f='false',
                n='null',
            )
            # 要判断是否真的是 true false null
            t = Token(Type.keyword)
            t.value = kvs[c]
            tokens.append(t)
            i += len(kvs[c])
        else:
            print("*** 错误", c, code[i:i+10])
            return
    return tokens


def token_list(path):
    s = load_file(path)
    ts = loads(s)
    return ts
