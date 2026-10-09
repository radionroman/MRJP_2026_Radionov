# Adapted by permission from https://github.com/IUCompilerCourse/python-student-support-code
# See EOC-LICENSE for details
import ast
import x86_ast
from ast import (expr, stmt, Module, Name)
from x86_ast import (X86Program, instr, arg, Variable)
import os

Binding = tuple[Name, expr]
Temporaries = list[Binding]


class Compiler:
    ############################################################################
    # Remove Complex Operands
    ############################################################################

    def rco_exp(self, e: expr, need_atomic : bool) -> tuple[expr, Temporaries]:
        return (e, [])

    def rco_stmt(self, s: stmt) -> list[stmt]:
        return [s]        

    def remove_complex_operands(self, p: Module) -> Module:
        return p               

    ############################################################################
    # Select Instructions
    ############################################################################

    # The expression e passed to select_arg should furthermore be an atom.
    # (But there is no type for atoms, so the type of e is given as expr.)
    def select_arg(self, e: expr) -> arg:
        match e:
            case ast.Constant(value):
                match value:
                    case int():
                        return x86_ast.Immediate(value)
                    case _:
                        raise Exception('Unsupported value type' + repr(e))
            case ast.Name(id):
                return x86_ast.Variable(id)
            case _:
                raise Exception('Unsupported expression class' + repr(e))

    def select_stmt(self, s: stmt) -> list[instr]:
        instructions: list[x86_ast.instr]=[]
        match s:
            case ast.Expr(ast.Call(ast.Name('print'), [exp])):
                instructions.extend([
                    x86_ast.Instr('movq', [self.select_arg(exp), x86_ast.Reg('rdi')]),
                    x86_ast.Callq('print_int', 1)
                    
                ])
            case ast.Assign([ast.Name(id)], exp):
                destination = x86_ast.Variable(id)
                match exp:
                    case ast.Constant() | ast.Name():
                        instructions.extend([
                            x86_ast.Instr('movq', [self.select_arg(exp), destination])
                        ])
                    case ast.Call(ast.Name('input_int'), args):
                        instructions.extend([
                            x86_ast.Callq('input_int', 0),
                            x86_ast.Instr('movq', [x86_ast.Reg('rax'), destination])
                        ])

                    case ast.UnaryOp(ast.USub(), exp):
                        instructions.extend([
                            x86_ast.Instr('movq', [self.select_arg(exp), x86_ast.Reg('rax')]),
                            x86_ast.Instr('negq', [x86_ast.Reg('rax')]),
                            x86_ast.Instr('movq', [x86_ast.Reg('rax'), destination])
                            ])
                    case ast.BinOp(exp_left, ast.Add(), exp_right):
                        instructions.extend([
                            x86_ast.Instr('movq', [self.select_arg(exp_left), x86_ast.Reg('rax')]),
                            x86_ast.Instr('addq', [self.select_arg(exp_right), x86_ast.Reg('rax')]),
                            x86_ast.Instr('movq', [x86_ast.Reg('rax'), destination])
                            ])                        
                    case ast.BinOp(exp_left, ast.Sub(), exp_right):     
                        instructions.extend([
                            x86_ast.Instr('movq', [self.select_arg(exp_left), x86_ast.Reg('rax')]),
                            x86_ast.Instr('subq', [self.select_arg(exp_right), x86_ast.Reg('rax')]),
                            x86_ast.Instr('movq', [x86_ast.Reg('rax'), destination])
                            ])  
            case _:
                raise Exception('error in select_stmt' + repr(s)) 
        return instructions     


    def select_instructions(self, p: Module) -> X86Program:
        program_body: list[x86_ast.instr] = []
        match p:
            case Module(body):
                for s in body:
                    program_body.extend(self.select_stmt(s))
                return X86Program(program_body)
            case _:
                raise Exception('error in select_instructions' + repr(p))    

    ############################################################################
    # Assign Homes
    ############################################################################

    def assign_homes_arg(self, a: arg, home: dict[Variable, arg]) -> arg:
        match a:
            case Variable(id):
                if id in home.keys():
                    return home[id]
                else:
                    home[id]=x86_ast.Deref('rsp', -len(home)*8-8)
                    return home[id]

            case _:
                return a


    def assign_homes_instr(self, i: instr,
                           home: dict[Variable, arg]) -> instr:
        
        match i:
            case x86_ast.Instr(name, args):
                new_args = []
                for a in args:
                    new_args.append(self.assign_homes_arg(a, home))
                return x86_ast.Instr(name, new_args)
            case _:
                return i

    def assign_homes(self, p: X86Program) -> X86Program:
        
        new_body: list[instr] = []
        home: dict[Variable, arg] = {}

        if not isinstance(p, X86Program): 
            raise Exception('wrong type')

        for i in p.body:
            new_body.append(self.assign_homes_instr(i, home))

        stack_offset = ((len(home)*8 + 15) // 16) * 16
        stack_offset_instr  = x86_ast.Instr('subq', [x86_ast.Reg('rsp'), x86_ast.Immediate(stack_offset)])
        return X86Program([stack_offset_instr]+new_body)
   

    ############################################################################
    # Patch Instructions
    ############################################################################

    def patch_instr(self, i: instr) -> list[instr]:
        return [i]      

    def patch_instructions(self, p: X86Program) -> X86Program:
        return p    

    ############################################################################
    # Prelude & Conclusion
    ############################################################################

    def prelude_and_conclusion(self, p: X86Program) -> X86Program:
        instructions: list[x86_ast.instr] = []
        instructions.extend([
            x86_ast.Instr('pushq', [x86_ast.Reg('rbp')]),
            x86_ast.Instr('movq', [x86_ast.Reg('rsp'), x86_ast.Reg('rbp')]),
        ])
        instructions.extend(p.body)
        instructions.extend([
            x86_ast.Instr('movq',[x86_ast.Reg('rbp'), x86_ast.Reg('rsp')]),
            x86_ast.Instr('popq', [x86_ast.Reg('rbp')]),
            x86_ast.Instr('ret', []),

        ])
        return X86Program(instructions)
