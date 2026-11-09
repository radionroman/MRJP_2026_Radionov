/*---------------------
Live After Mapping:
    callq print_int: set()
    movq c, %rdi: {Reg(id='rdi')}
    movq $30, c: {Variable(id='c')}
    callq print_int: set()
    movq b, %rdi: {Reg(id='rdi')}
    movq $20, b: {Variable(id='b')}
    imulq a, a: set()
    callq print_int: {Variable(id='a')}
    movq a, %rdi: {Variable(id='a'), Reg(id='rdi')}
    imulq $5, a: {Variable(id='a')}
    callq print_int: {Variable(id='a')}
    movq a, %rdi: {Variable(id='a'), Reg(id='rdi')}
    imulq $5, a: {Variable(id='a')}
    callq print_int: {Variable(id='a')}
    movq a, %rdi: {Variable(id='a'), Reg(id='rdi')}
    imulq $5, a: {Variable(id='a')}
    movq $3, a: {Variable(id='a')}
    movq $10, a: set()
Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5}
Interference Graph:
  %r10: [Variable(id='a')]
  %r8: [Variable(id='a')]
  %r9: [Variable(id='a')]
  %r11: [Variable(id='a')]
  %rdi: [Variable(id='a')]
  %rcx: [Variable(id='a')]
  %rax: [Variable(id='a')]
  %rdx: [Variable(id='a')]
  %rsi: [Variable(id='a')]
  c: []
  b: []
  a: [Reg(id='r10'), Reg(id='r8'), Reg(id='r9'), Reg(id='r11'), Reg(id='rdi'), Reg(id='rcx'), Reg(id='rax'), Reg(id='rdx'), Reg(id='rsi')]
; Variable a has unavailable colors: {0, 1, 2, 3, 4, 5, 6, -4, -1}
; Variable b has unavailable colors: set()
; Variable c has unavailable colors: set()
; Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5, Variable(id='a'): 7, Variable(id='b'): 0, Variable(id='c'): 0}
Register Limit: 11
---------------------*/
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    subq $8, %rsp
    movq $10, %rbx
    movq $3, %rbx
    imulq $5, %rbx
    movq %rbx, %rdi
    callq print_int
    imulq $5, %rbx
    movq %rbx, %rdi
    callq print_int
    imulq $5, %rbx
    movq %rbx, %rdi
    callq print_int
    imulq %rbx, %rbx
    movq $20, %rcx
    movq %rcx, %rdi
    callq print_int
    movq $30, %rcx
    movq %rcx, %rdi
    callq print_int
    movq $0, %rax
    addq $8, %rsp
    popq %rbx
    popq %rbp
    retq 


