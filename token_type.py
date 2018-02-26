from enum import Enum


class Type(Enum):
    auto = 0                # auto 的时候, c 是 : , { } [] 其中之一, 要自己判断
    colon = 1               # :
    comma = 2               # ,
    braceLeft = 3           # {
    braceRight = 4          # }
    bracketLeft = 5         # [
    bracketRight = 6        # ]
    keyword = 7             # true false null
    number = 8              # 123
    string = 9              # "name"
