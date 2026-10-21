# Adapted by permission from https://github.com/IUCompilerCourse/python-student-support-code
# See EOC-LICENSE for details
import ast
import x86_ast
from ast import (expr, stmt, Module, Name)
from x86_ast import (X86Program, instr, arg, Variable, Immediate, Instr, Callq, Reg, Deref)
import os
import sys
import x86_interp

Binding = tuple[Name, expr]
Temporaries = list[Binding]


class Compiler:
    def __init__(self) -> None:
        self.temp_counter = 1
        self.stack_offset = 0

    ############################################################################
    # Remove Complex Operands
    ############################################################################

    # The fresh method generates a new temporary variable name each time it is called.
    def fresh(self) -> Name:
        name = "%tmp"+str(self.temp_counter)
        self.temp_counter += 1
        return ast.Name(name)

    def rco_exp(self, e: expr, need_atomic : bool) -> tuple[expr, Temporaries]:
        match e:
            case ast.Constant() | ast.Name():
                return (e, [])
            case ast.Call(ast.Name('input_int'), []):
                e = ast.Call(ast.Name('input_int'), [])
                if need_atomic:
                    t = self.fresh()
                    return (t, [(t, e)])
                else:
                    return (e, [])
            
            case ast.UnaryOp(operation, exp):
                exp2, tmps = self.rco_exp(exp, True)
                e = ast.UnaryOp(operation, exp2)
                if need_atomic:
                    t = self.fresh()
                    return (t, tmps + [(t, e)])
                else:
                    return (e, tmps)
                    
            case ast.BinOp(exp_left, operation, exp_right):
                exp_left2, tmps_left = self.rco_exp(exp_left, True)
                exp_right2, tmps_right = self.rco_exp(exp_right, True)
                e = ast.BinOp(exp_left2, operation, exp_right2)
                if need_atomic:
                    t = self.fresh()
                    return (t, tmps_left + tmps_right + [(t, e)])
                else:
                    return (e, tmps_left + tmps_right)
            case _:
                raise Exception("Unsupported expression type in rco_exp " + repr(e))
            

    def rco_stmt(self, s: stmt) -> list[stmt]:
        result: stmt
        tmps: Temporaries
        
        match s:
            case ast.Assign(targets, exp):
                exp2, tmps = self.rco_exp(exp, False)
                result = ast.Assign(targets, exp2)
            case ast.Expr(ast.Call(ast.Name('print'), [exp])):
                exp2, tmps = self.rco_exp(exp, True)
                result = ast.Expr(ast.Call(ast.Name('print'), [exp2], []))
            case _:
                raise Exception("Unsupported statement in rco_stmt: " + repr(s))
        statements: list[stmt] = []
        for var, value in tmps:
            statements.append(ast.Assign([var], value))
        statements.append(result)
        return statements

    def remove_complex_operands(self, p: Module) -> Module:
        new_body:list[stmt] = []
        match p:
            case Module(body):
                for s in body:
                    new_body.extend(self.rco_stmt(s))
            case _:
                raise Exception('error in remove_complex_operands' + repr(p)) 

        return Module(new_body)         

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
                        raise Exception('select_arg(e) -> Unsupported value class: ' + repr(e))
            case ast.Name(id):
                return Variable(id)
            case _:
                raise Exception('select_arg(e) -> Unsupported expression class: ' + repr(e))

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
                            Instr('movq', [self.select_arg(exp_left), Reg('rax')]),
                            Instr('addq', [self.select_arg(exp_right), Reg('rax')]),
                            Instr('movq', [Reg('rax'), destination])
                        ])                        
                    case ast.BinOp(exp_left, ast.Sub(), exp_right):     
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp_left), Reg('rax')]),
                            Instr('subq', [self.select_arg(exp_right),Reg('rax')]),
                            Instr('movq', [Reg('rax'), destination]),
                        ])  
                    case ast.BinOp(exp_left, ast.Mult(), exp_right):     
                        instructions.extend([
                            Instr('movq', [self.select_arg(exp_left), Reg('rax')]),
                            Instr('imulq', [self.select_arg(exp_right),Reg('rax')]),
                            Instr('movq', [Reg('rax'), destination]),
                        ])                         
                    case _: 
                        raise Exception('select_stmt(s) -> Unsupported assignment statement: ' + repr(s)) 
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

        self.stack_offset = ((len(home)*8 + 15) // 16) * 16
        return X86Program(new_body)
   

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
            Instr('subq', [ Immediate(self.stack_offset),Reg('rsp')])
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
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    #open the file, parse it with ast and apply the compiler passes
    with open(filename, 'r') as f:
        source = f.read()
        tree = ast.parse(source)
        compiler = Compiler()
        program_step1 = compiler.remove_complex_operands(tree)
        program_step2 = compiler.select_instructions(program_step1)
        program_step3 = compiler.assign_homes(program_step2)
        program_step4 = compiler.patch_instructions(program_step3)
        program_step5 = compiler.prelude_and_conclusion(program_step4)
        print(program_step5)


if __name__ == "__main__":
    main()