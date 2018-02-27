from token_type import Type


def parse(ts):
    t = ts[0]
    del ts[0]
    if t.type == Type.braceLeft:
        obj = {}
        while ts[0].type != Type.braceRight:
            k = ts[0]
            _colon = ts[1]
            # 确保 k.type 必须是 string
            # 确保 _colon 必须是 colon
            del ts[0]
            del ts[0]
            v = parse(ts)
            obj[k] = v
            # 吃一个 逗号
            _comma = ts[0]
            if _comma.type == Type.comma:
                del ts[0]
        # 结束 删除末尾的 '}'
        del ts[0]
        return obj
    elif t.type == Type.bracketLeft:
        l = []
        while ts[0].type != Type.bracketRight:
            v = parse(ts)
            # 吃一个 逗号
            _comma = ts[0]
            if _comma.type == Type.comma:
                del ts[0]
            l.append(v)
        # 删除末尾的 ']'
        del ts[0]
        return l
    else:
        # print('value: ', t)
        return t
