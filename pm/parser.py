from dataclasses import dataclass
from typing import Tuple
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
lcurly = lexeme(string("{"))
rcurly = lexeme(string("}"))

array = lbracket >> integer.sep_by(comma) << rbracket

@dataclass
class KeyValue:
    key: str
    value: str

keyvalue = seq(
    key=lexeme(id) << lexeme(string("=")),
    value=lexeme(id)
)

options = lcurly >> keyvalue.sep_by(comma) << rcurly

@dataclass
class Task:
    id: str
    desc: str
    duration: int
    resources: list[int]
    options: list[Tuple[str, str]]
    
task = seq(
    id=id << colon, 
    desc=desc,
    duration=lparen >> integer << comma,
    resources=array << rparen,
    options=options.optional(),
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
