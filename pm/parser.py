from dataclasses import dataclass
from parsy import string, regex, seq, eof

# utilities
whitespace = regex(r" *")
lexeme = lambda p: p << whitespace

comment = regex(r"#.+")
colon = lexeme(string(":"))
lparen = lexeme(string("("))
rparen = string(")")
lbracket = lexeme(string("["))
rbracket = lexeme(string("]"))
comma = lexeme(string(","))
integer = regex(r"[0-9]+").map(int)
id = regex(r"[a-zA-Z0-9]+").map(str)
desc = regex(r"[a-zA-Z0-9 ]+").map(str)
newline = regex(r"\n+")

array = lbracket >> integer.sep_by(comma) << rbracket

@dataclass
class Task:
    id: str
    desc: str
    duration: int
    resources: list[int]
    
task = seq(
    id=id << colon, 
    desc=desc,
    duration=lparen >> integer << comma,
    resources=array << rparen
).combine_dict(Task)

@dataclass
class Precedence:
    a: str
    b: str

precedence = seq(
    a=lexeme(id) << lexeme(string("->")),
    b=lexeme(id)
).combine_dict(Precedence)

statement = comment | task | precedence | eof
doc = statement.sep_by(newline)
