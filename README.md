# MRJP_2026_Radionov

Tests: ```uv run python -m pytest -v test_compiler.py```

To check x86 output on a example code: ```uv run python run_compiler.py```

## Assignment 1
### 01 The language *Lqua*

The language *Lqua* (called $L^{mon}_{var}$ in Jeremy Siek's book)
is described by the following abstract syntax (we use a subset of Python abstract syntax defined in the standard module `ast`):

```
prog ::= Module(list[stmt])
stmt ::= Expr( Call(Name('print'), [atm]) ) | Assign([var], exp)
exp ::= atm
      | Call(Name='input_int', [])
      | UnaryOp(USuB(),atm)
      | BinOp(atm,Add(),atm)
      | BinOp(atm,Sub(),atm)
atm ::= Constant(int) | var
var ::= Name(str)
```