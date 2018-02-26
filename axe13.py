"""
    新建axe13/py/axe13.py
    token 列表解析为 ast 的代码
    利用之前作业, 增加定义变量的功能
    def apply(code,vars):
        code 是代码字符串 支持定义变量的功能
        code = '''
            [set a 1]
            [set b 2]
            [+ a b]
        '''
        上面三行代码用 set 实现了变量定义
        本函数中, var 是一个字典, 包含了所有当前环境中定义的变量和值
        用这样的方式, 在全局变量中声明一个 {}
        每个 apply 都传入 vars
        在 set 的时候往里面添加变量的值
        在使用到变量的时候, 从 vars 中找变量的值 找不到就是未定义变量
        注意: 变量是作为一种新的 token 存在
        pass
"""
from token_type import Type
from lisp_parser import parsed_ast

def getVarName(string,index):
    spaces = '\t\n\r '
    s = ''
    while index < len(string):
        n = string[index]
        if n in spaces or n == ']':
            break
        else:
            s += n
        index += 1
    return s,index


def getKeywords(string,index):
    spaces = '\t\n\r '
    start = index
    s = ''
    while index < len(string):
        n = string[index]
        if n in spaces or n == ']':
            break
        else:
            s += n
        index += 1

    return s,index


def number_end(string,index):
    start = index
    num = ''
    while index < len(string):
        n = string[index]
        index += 1
        if n in ' ]':
            break
        else:
            num += n

    return int(num),index-1


def loads(code):
    digits = '1234567890'
    keywords = ["yes","no","null","if","log","set","function"]
    spaces = '\t\n\r '
    tokens = []
    i = 0
    while i < len(code):
        c = code[i]
        i += 1
        if c in spaces:
            continue
        elif c in digits:
            # 数字
            number,offset = number_end(code,i-1)
            # token = Token(Type.number,number)
            token = number
            i = offset
            tokens.append(token)
        elif c in 'ynlisf':
            # 关键字
            k,offset = getKeywords(code,i-1)
            if k in keywords:
                # token = Token(Type.keywords,k)
                token = k
                i = offset
                tokens.append(token)
        elif c in '+-*/%=!><':
            # token = Tokens(Type.auto,t)
            token = c
            tokens.append(token)
        elif c.isalpha():
            var,offset = getVarName(code,i-1)
            # token = Tokens(Type.var,var)
            token = var
            i = offset
            tokens.append(token)
        elif c in ':,[]{}':
            tokens.append(c)
        else:
            # error
            break
    return tokens


class GuaOp(object):
    def __init__(self,vars):
        super(GuaOp, self).__init__()
        self.vars = vars
        self.digits = [0,1,2,3,4,5,6,7,8,9]

    def set(self,args):
        var = args[0]
        value = args[1]
        self.vars[var] = value


    def mathOp(self,args):
        vs = []
        for k in args:
            if k in args:
                v = self.vars[k]
                vs.append(v)
            else:
                print('未声明')
        return vs

    def sum(self, args):
        vs = self.mathOp(args)
        r = vs[0]
        for v in vs[1:]:
            r += v
        return r

    def minus(self,args):
        vs = self.mathOp(args)
        r = vs[0]
        for v in vs[1:]:
            r -= v
        return r

    def multiply(self,args):
        vs = self.mathOp(args)
        r = 1
        for v in vs:
            r *= v
        return r

    def divide(self,args):
        vs = self.mathOp(args)
        r = vs[0]
        for v in vs[1:]:
            r /= v
        return r

    def modulo(self,args):
        vs = self.mathOp(args)
        r = vs[0]
        for v in vs[1:]:
            r %= v
        return r

    def equal(self,args):
        vs = self.mathOp(args)
        a = vs[0]
        b = vs[1]
        r = a == b
        return r

    def unequal(self,args):
        vs = self.mathOp(args)
        a = vs[0]
        b = vs[1]
        r = a != b
        return r

    def more(self,args):
        vs = self.mathOp(args)
        a = vs[0]
        b = vs[1]
        r = a > b
        return r

    def less(self,args):
        vs = self.mathOp(args)
        a = vs[0]
        b = vs[1]
        r = a < b
        return r

    def func(self,args):
        funcVar = args[0]
        funcname = funcVar[0]
        sen = args[1]
        self.vars[funcname] = [sen[0],len(sen[1:])]



def parse_ast(ast,vars):
    op,args = ast[0],ast[1:]
    myop = GuaOp(vars)
    d = {
        "function": myop.func,
        "set": myop.set,
        "+": myop.sum,
        "-": myop.minus,
        "*": myop.multiply,
        "/": myop.divide,
        "%": myop.modulo,
        "=": myop.equal,
        ">": myop.more,
        "<": myop.less,
        "!": myop.unequal,
    }
    if op not in d:
        l = vars[op]
        if len(args) != l[1]:
            print('参数不正确')
            return
        else:
            op = l[0]
            return d[op](args)
    else:
        return d[op](args)


def apply(code,vars):
    ts = loads(code)
    ast = parsed_ast(['['] + ts + [']'])
    for sentence in ast:
        v = parse_ast(sentence,vars)
        if v != None:
            r = v

    return r


def ensure(condition,message):
    if condition:
        print('测试成功！')
    else:
        print('测试失败！' + message)


def test_apply():
    code1 = '''
    [set a 1]
    [set b 2]
    [+ a b]
    '''
    vars = {}
    r1 = apply(code1,vars)
    ensure(r1 == 3,'test_apply fail 1')
    code2 = '''
    [set a 1]
    [set b 2]
    [- a b]
    '''
    vars = {}
    r2 = apply(code2,vars)
    ensure(r2 == -1,'test_apply fail 2')
    code3 = '''
    [set a 1]
    [set b 2]
    [* a b]
    '''
    vars = {}
    r3 = apply(code3,vars)
    ensure(r3 == 2,'test_apply fail 3')
    code4 = '''
    [set a 1]
    [set b 2]
    [/ a b]
    '''
    vars = {}
    r4 = apply(code4,vars)
    ensure(r4 == 0.5,'test_apply fail 4')
    vars = {}
    code5 = '''
    [function [add a b] [+ a b]]
    [set c 6]
    [set d 6]
    [add c d]
    '''
    r5 = apply(code5,vars)
    ensure(r5 == 12 ,'test_apply fail 5')


def main():
    test_apply()

if __name__ == '__main__':
    main()
