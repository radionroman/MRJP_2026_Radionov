# Adapted by permission from https://github.com/IUCompilerCourse/python-student-support-code
# See EOC-LICENSE for details
import ast
import x86_ast
from ast import (expr, stmt, Module, Name)
from x86_ast import (X86Program, instr, arg, Variable, Immediate, Instr, Callq, Reg, Deref)
import os
import sys

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
                        return Immediate(value)
                    case _:
                        raise Exception('Unsupported value type' + repr(e))
            case ast.Name(id):
                return Variable(id)
            case _:
                raise Exception('Unsupported expression class' + repr(e))

    def select_stmt(self, s: stmt) -> list[instr]:
        instructions: list[instr]=[]
        match s:
            case ast.Expr(ast.Call(ast.Name('print'), [exp])):
                instructions.extend([
                    Instr('movq', [self.select_arg(exp), Reg('rdi')]),
                    Callq('print_int', 1)
                ])
            case ast.Assign([ast.Name(id)], exp):
                destination = Variable(id)
                match exp:
                    case ast.Constant() | ast.Name():
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp), destination])
                        ])
                    case ast.Call(ast.Name('input_int'), []):
                        instructions.extend([
                            Callq('input_int', 0),
                            Instr('movq', [Reg('rax'), destination])
                        ])

                    case ast.UnaryOp(ast.USub(), exp):
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp), destination]),
                            Instr('negq', [destination]),
                            ])
                    case ast.BinOp(exp_left, ast.Add(), exp_right):
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp_left), destination]),
                            Instr('addq', [self.select_arg(exp_right), destination]),
                            ])                        
                    case ast.BinOp(exp_left, ast.Sub(), exp_right):     
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp_left), destination]),
                            Instr('subq', [self.select_arg(exp_right),destination]),
                            ])  
                    case _: 
                        raise Exception('error in select_stmt' + repr(s)) 
            case _:
                raise Exception('error in select_stmt' + repr(s)) 
        return instructions     


    def select_instructions(self, p: Module) -> X86Program:
        program_body: list[instr] = []
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
            case Variable() as var:
                if var in home.keys():
                    return home[var]
                else:
                    home[var]=Deref('rbp', -len(home)*8-8)
                    return home[var]

            case _:
                return a


    def assign_homes_instr(self, i: instr,
                           home: dict[Variable, arg]) -> instr:
        
        match i:
            case Instr(name, args):
                new_args = []
                for a in args:
                    new_args.append(self.assign_homes_arg(a, home))
                return Instr(name, new_args)
            case _:
                return i

    def assign_homes(self, p: X86Program) -> X86Program:
        
        new_body: list[instr] = []
        home: dict[Variable, arg] = {}
        if not isinstance(p.body, list):
            raise Exception("Expected list[instr]")
        if not isinstance(p, X86Program): 
            raise Exception('wrong type')

        for i in p.body:
            new_body.append(self.assign_homes_instr(i, home))

        stack_offset = ((len(home)*8 + 15) // 16) * 16
        stack_offset_instr  = Instr('subq', [ Immediate(stack_offset),Reg('rsp')])
        return X86Program([stack_offset_instr]+new_body)
   

    ############################################################################
    # Patch Instructions
    ############################################################################

    def patch_instr(self, i: instr) -> list[instr]:
        match i:
            case Instr(cmd, [Deref() as source, Deref() as destination]):
                return [
                    Instr('movq', [source, Reg('rax')]),
                    Instr(cmd, [Reg('rax'), destination])
                ]
        return [i]      

    def patch_instructions(self, p: X86Program) -> X86Program:
        new_body: list[instr] = []
        if not isinstance(p.body, list):
            raise Exception("Expected list[instr]")
        if not isinstance(p, X86Program): 
            raise Exception('wrong type')

        for i in p.body:
            new_body.extend(self.patch_instr(i))
        return X86Program(new_body)

    ############################################################################
    # Prelude & Conclusion
    ############################################################################

    def prelude_and_conclusion(self, p: X86Program) -> X86Program:
        instructions: list[instr] = []

        if not isinstance(p.body, list):
            raise Exception("Expected list[instr]")

        instructions.extend([
            Instr('pushq', [Reg('rbp')]),
            Instr('movq', [Reg('rsp'), Reg('rbp')]),
        ])

        instructions.extend(p.body)

        instructions.extend([
            Instr('movq', [Immediate(0), Reg('rax')]),
            Instr('movq',[Reg('rbp'), Reg('rsp')]),
            Instr('popq', [Reg('rbp')]),
            Instr('retq', []),

        ])
        return X86Program(instructions)

def main():
    if len(sys.argv) != 2:
        print("Usage: python compile.py <source_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    #open the file, parse it with ast and apply the compiler passes
    with open(filename, 'r') as f:
        source = f.read()
        tree = ast.parse(source)
        compiler = Compiler()
        program_step2 = compiler.select_instructions(tree)
        program_step3 = compiler.assign_homes(program_step2)
        program_step4 = compiler.patch_instructions(program_step3)
        program_step5 = compiler.prelude_and_conclusion(program_step4)
        print(program_step5)



if __name__ == "__main__":

    main()