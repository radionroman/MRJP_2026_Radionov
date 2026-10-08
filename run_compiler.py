"""Place beside compiler_skel.py and run: uv run python run_compiler.py"""

import ast

from compiler_skel import Compiler


# Replace the program between the triple quotes with your own code.
# For now, use simple operands: x + 2 works; (x + 2) + 3 needs RCO.
SOURCE = """
x = 40
y = x + 2
z = -y
print(z)
"""


def main() -> None:
    # Parse the source into Python's abstract syntax tree.
    tree = ast.parse(SOURCE)

    # Run just the pass you are currently implementing.
    program_step2 = Compiler().select_instructions(tree)
    program_step3 = Compiler().assign_homes(program_step2)
    program_step4 = Compiler().patch_instructions(program_step3)
    program_step5 = Compiler().prelude_and_conclusion(program_step4)
    # X86Program.__str__ formats the instruction objects as assembly text.
    print(program_step5)


if __name__ == "__main__":
    main()
