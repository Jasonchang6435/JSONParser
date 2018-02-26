"""
2 个函数
分别用递归和栈的方式从 token 列表解析为 ast
"""


def parsed_ast(token_list):
    """
    递归解析 ast
    """
    ts = token_list
    token = ts[0]
    del ts[0]
    if token == '[':
        exp = []
        while ts[0] != ']':
            t = parsed_ast(ts)
            exp.append(t)
        # 循环结束, 删除末尾的 ']'
        del ts[0]
        return exp
    else:
        # token 需要 process_token / parsed_token
        return token


def pop_list(stack):
    l = []
    while stack[-1] != '[':
        l.append(stack.pop(-1))
    stack.pop(-1)
    l.reverse()
    return l


def parsed_ast_stack(token_list):
    """
    用栈解析 ast
    """
    l = []
    i = 0
    while i < len(token_list):
        token = token_list[i]
        i += 1
        if token == ']':
            list_token = pop_list(l)
            l.append(list_token)
        else:
            l.append(token)
    return l


def main():
    tokens1 = ['[', '+', 12, '[', '-', 23, 45, ']', ']']
    tokens2 = ['[', '+', 12, '[', '-', 23, 45, ']', ']']
    print('stack parse', parsed_ast_stack(tokens1 + tokens2))

    tokens = ['[', '+', 12, '[', '-', 23, 45, ']', ']']
    expected_ast = ['+', 12, ['-', 23, 45]]
    ast = parsed_ast(tokens)
    print('recursive parse', ast)
    assert ast == expected_ast


if __name__ == '__main__':
    main()
