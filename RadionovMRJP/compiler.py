# Adapted by permission from https://github.com/IUCompilerCourse/python-student-support-code
# See EOC-LICENSE for details
import ast
from ast import (expr, stmt, Module, Name)
from x86_ast import (X86Program, instr, arg, Variable, Immediate, Instr, Callq, Reg, Deref)
import sys
from graph import UndirectedAdjList

Binding = tuple[Name, expr]
Temporaries = list[Binding]

caller_saved_registers = [
    Reg('rax'), Reg('rcx'), Reg('rdx'), Reg('rsi'), Reg('rdi'),
    Reg('r8'), Reg('r9'), Reg('r10'), Reg('r11'),
]

argument_registers = [
    Reg('rdi'), Reg('rsi'), Reg('rdx'), Reg('rcx'), Reg('r8'), Reg('r9'),
]

allocatable_registers = [
    Reg('rcx'), Reg('rdx'), Reg('rsi'), Reg('rdi'),
    Reg('r8'), Reg('r9'), Reg('r10'),
    Reg('rbx'), Reg('r12'), Reg('r13'), Reg('r14'),
]

callee_saved_registers = [Reg('rbx'), Reg('r12'), Reg('r13'), Reg('r14')]
reserved_registers = [Reg('rax'), Reg('rsp'), Reg('rbp'), Reg('r11'), Reg('r15')]

Location = Variable | Reg

class Compiler:
    def __init__(self) -> None:
        self.temp_counter = 1
        self.stack_offset = 0
        self.callee_saved_registers_used: set[Reg] = set()

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
                        if destination == self.select_arg(exp_left) and destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('addq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_left):
                            instructions.extend([
                                Instr('addq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('addq', [self.select_arg(exp_left), destination]),
                            ])
                        else:
                            instructions.extend([
                                Instr('movq', [self.select_arg(exp_left), destination]),
                                Instr('addq', [self.select_arg(exp_right), destination]),
                            ])
                    case ast.BinOp(exp_left, ast.Sub(), exp_right):
                        if destination == self.select_arg(exp_left) and destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('subq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_left):
                            instructions.extend([
                                Instr('subq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('negq', [destination]),
                                Instr('addq', [
                                    self.select_arg(exp_left),
                                    destination,
                                ]),
                            ])
                        else:
                            instructions.extend([
                                Instr('movq', [self.select_arg(exp_left), destination]),
                                Instr('subq', [self.select_arg(exp_right), destination]),
                            ])
                    case ast.BinOp(exp_left, ast.Mult(), exp_right):
                        if destination == self.select_arg(exp_left) and destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('imulq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_left):
                            instructions.extend([
                                Instr('imulq', [self.select_arg(exp_right), destination]),
                            ])
                        elif destination == self.select_arg(exp_right):
                            instructions.extend([
                                Instr('imulq', [self.select_arg(exp_left), destination]),
                            ])
                        else:
                            instructions.extend([
                                Instr('movq', [self.select_arg(exp_left), destination]),
                                Instr('imulq', [self.select_arg(exp_right), destination]),
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
    # Uncover Live Variables
    ############################################################################

    def read_vars(self, i: instr) -> set[Location]:
        match i:
            case Instr('movq', [src, dst]):
                return {src} if isinstance(src, Location) else set()
            case Instr(name, [src, dst]) if name in ['addq', 'subq', 'imulq']:
                return {a for a in [src, dst] if isinstance(a, Location)}
            case Instr('negq', [dst]):
                return {dst} if isinstance(dst, Location) else set()
            case Callq(name, arity):
                if not 0 <= arity <= len(argument_registers):
                    raise Exception('Unsupported call arity in read_vars: ' + repr(i))
                return set(argument_registers[:arity])
            case _:
                raise Exception('Unsupported instruction in read_vars: ' + repr(i))

    def write_vars(self, i: instr) -> set[Location]:
        match i:
            case Instr(name, [src, dst]) if name in ['movq', 'addq', 'subq', 'imulq']:
                return {dst} if isinstance(dst, Location) else set()
            case Instr('negq', [dst]):
                return {dst} if isinstance(dst, Location) else set()
            case Callq(_, _):
                return set(caller_saved_registers)
            case _:
                raise Exception('Unsupported instruction in write_vars: ' + repr(i))

    def uncover_live(self, p: X86Program) -> dict[instr, set[Location]]:
        if not isinstance(p.body, list):
            raise Exception('Expected list[instr]')

        live_after: dict[instr, set[Location]] = {}
        live_before: set[Location] = set()

        for i in reversed(p.body):
            live_after[i] = live_before
            live_before = (live_before - self.write_vars(i)) | self.read_vars(i)
        print("Live After Mapping:")
        for instr, live_vars in live_after.items():
            print(f"  {instr}: {live_vars}")
        return live_after

    ############################################################################
    # Build Interference Graph
    ############################################################################

    def add_edge(self, interference_graph: UndirectedAdjList,
                 var1: Location, var2: Location) -> None:
        interference_graph.add_vertex(var1)
        interference_graph.add_vertex(var2)
        if var1 != var2 and not interference_graph.has_edge(var1, var2):
            interference_graph.add_edge(var1, var2)

    def build_interference_instr(self, i: instr, live_after: set[Location],
                                 interference_graph: UndirectedAdjList) -> None:
        written = self.write_vars(i)
        for var in self.read_vars(i) | written | live_after:
            interference_graph.add_vertex(var)

        match i:
            case Instr('movq', [src, dst]):
                if isinstance(dst, Location):
                    for var in live_after:
                        if var != src:
                            self.add_edge(interference_graph, dst, var)
            case _:
                for dst in written:
                    for var in live_after:
                        self.add_edge(interference_graph, dst, var)

    def build_interference_graph(
        self, live_after: dict[instr, set[Location]]
    ) -> UndirectedAdjList:
        interference_graph = UndirectedAdjList()
        for i, live_vars in live_after.items():
            self.build_interference_instr(i, live_vars, interference_graph)
        return interference_graph

    ############################################################################
    # Allocate Registers
    ############################################################################

    def color_graph(self, interference_graph: UndirectedAdjList,
                    register_limit: int = 11) -> dict[Location, int]:
        if not 0 <= register_limit <= len(allocatable_registers):
            raise Exception('register_limit must be between 0 and 11')

        colors: dict[Location, int] = {}
        for color, reg in enumerate(allocatable_registers):
            colors[reg] = color
        for color, reg in enumerate(reserved_registers, start=1):
            colors[reg] = -color

        print("Colors after assigning allocatable and reserved registers:", colors)
        
        variables = sorted(
            (v for v in interference_graph.vertices() if isinstance(v, Variable)),
            key=str,
        )

        # Print the interference graph for debugging
        print("Interference Graph:")
        for vertex in interference_graph.vertices():
            neighbors = interference_graph.adjacent(vertex)
            print(f"  {vertex}: {neighbors}")

        for var in variables:
            unavailable = {
                colors[neighbor]
                for neighbor in interference_graph.adjacent(var)
                if neighbor in colors
            }
            print(f"; Variable {var.id} has unavailable colors: {unavailable}")
            color = 0
            while color in unavailable:
                color += 1
            colors[var] = color

        return colors

    def allocate_registers(self, p: X86Program,
                           interference_graph: UndirectedAdjList,
                           register_limit: int) -> X86Program:
        if not isinstance(p.body, list):
            raise Exception('Expected list[instr]')
        assigned_registers = 0
        colors = self.color_graph(interference_graph, register_limit)
        self.callee_saved_registers_used = {
            allocatable_registers[color]
            for var, color in colors.items()
            if isinstance(var, Variable) and color < register_limit
            and allocatable_registers[color] in callee_saved_registers
        }
        saved_size = 8 * len(self.callee_saved_registers_used)
        spill_count = 0
        home: dict[Variable, arg] = {}
        print("; Colors after assigning allocatable and reserved registers:", colors)
        for var, color in colors.items():
            if isinstance(var, Variable):
                if color < register_limit:
                    home[var] = allocatable_registers[color]
                else:
                    spill_count += 1
                    home[var] = Deref(
                        'rbp',
                        -saved_size - 8 * spill_count,
                    )

        frame_size = saved_size + 8 * spill_count
        self.stack_offset = ((frame_size + 15) // 16) * 16 - saved_size
        print("Register Limit:", register_limit)
        new_body: list[instr] = []
        for i in p.body:
            new_body.append(self.assign_homes_instr(i, home))
        return X86Program(new_body)

    ############################################################################
    # Assign Homes
    ############################################################################

    def assign_homes_arg(self, a: arg, home: dict[Variable, arg]) -> arg:
        match a:
            case Variable() as var:
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
        if not isinstance(p.body, list):
            raise Exception('Expected list[instr]')

        home: dict[Variable, arg] = {}
        for i in p.body:
            match i:
                case Instr(name, args):
                    for a in args:
                        if isinstance(a, Variable) and a not in home:
                            home[a] = Deref('rbp', -8 * (len(home) + 1))

        self.callee_saved_registers_used = set()
        self.stack_offset = ((len(home) * 8 + 15) // 16) * 16
        new_body: list[instr] = []
        for i in p.body:
            new_body.append(self.assign_homes_instr(i, home))
        return X86Program(new_body)

    ############################################################################
    # Patch Instructions
    ############################################################################

    def patch_instr(self, i: instr) -> list[instr]:
        match i:
            case Instr('movq', [Deref() as src, Deref() as dst]) if src == dst:
                return []
            case Instr('movq', [Reg() as src, Reg() as dst]) if src == dst:
                return []
            case Instr('imulq', [src, Deref() as dst]):
                return [
                    Instr('movq', [dst, Reg('rax')]),
                    Instr('imulq', [src, Reg('rax')]),
                    Instr('movq', [Reg('rax'), dst]),
                ]
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
        if not isinstance(p.body, list):
            raise Exception('Expected list[instr]')

        saved_registers = [
            reg for reg in callee_saved_registers
            if reg in self.callee_saved_registers_used
        ]
        instructions: list[instr] = [
            Instr('pushq', [Reg('rbp')]),
            Instr('movq', [Reg('rsp'), Reg('rbp')]),
        ]
        for reg in saved_registers:
            instructions.append(Instr('pushq', [reg]))
        if(self.stack_offset > 0):
            instructions.append(Instr('subq', [Immediate(self.stack_offset), Reg('rsp')]))

        instructions.extend(p.body)

        instructions.extend([
            Instr('movq', [Immediate(0), Reg('rax')]),
            Instr('addq', [Immediate(self.stack_offset), Reg('rsp')]),
        ])
        for reg in reversed(saved_registers):
            instructions.append(Instr('popq', [reg]))
        instructions.extend([
            Instr('popq', [Reg('rbp')]),
            Instr('retq', []),
        ])
        return X86Program(instructions)


def main():
    if len(sys.argv) != 4 and len(sys.argv) != 2:
        print('Usage: python compiler.py <source_file> [--register-limit <n>]')
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        source = ast.parse(f.read())

    register_limit = 11
    if len(sys.argv) == 4 and sys.argv[2] == '--register-limit':
        register_limit = int(sys.argv[3])
        if not 0 <= register_limit <= 11:
            print('Register limit must be between 0 and 11')
            sys.exit(1)

    compiler = Compiler()
    print("/*---------------------")
    simplified = compiler.remove_complex_operands(source)
    selected = compiler.select_instructions(simplified)
    live_after = compiler.uncover_live(selected)
    interference_graph = compiler.build_interference_graph(live_after)
    allocated = compiler.allocate_registers(selected, interference_graph, register_limit)
    patched = compiler.patch_instructions(allocated)
    program = compiler.prelude_and_conclusion(patched)
    print("---------------------*/")
    print(program)


if __name__ == '__main__':
    main()
