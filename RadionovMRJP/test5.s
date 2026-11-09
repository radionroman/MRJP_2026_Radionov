/*---------------------
Live After Mapping:
    callq print_int: set()
    movq a, %rdi: {Reg(id='rdi')}
    addq b, a: {Variable(id='a')}
    callq print_int: {Variable(id='a'), Variable(id='b')}
    movq $0, %rdi: {Variable(id='a'), Reg(id='rdi'), Variable(id='b')}
    movq $20, b: {Variable(id='a'), Variable(id='b')}
    movq $10, a: {Variable(id='a')}
Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5}
Interference Graph:
  %rdi: [Variable(id='a'), Variable(id='b')]
  %rax: [Variable(id='a'), Variable(id='b')]
  %rdx: [Variable(id='a'), Variable(id='b')]
  %r10: [Variable(id='a'), Variable(id='b')]
  %r11: [Variable(id='a'), Variable(id='b')]
  %r9: [Variable(id='a'), Variable(id='b')]
  %rcx: [Variable(id='a'), Variable(id='b')]
  %r8: [Variable(id='a'), Variable(id='b')]
  %rsi: [Variable(id='a'), Variable(id='b')]
  a: [Reg(id='rax'), Reg(id='rdi'), Reg(id='rdx'), Reg(id='r10'), Reg(id='r11'), Reg(id='r9'), Reg(id='rcx'), Reg(id='r8'), Reg(id='rsi'), Variable(id='b')]
  b: [Reg(id='rax'), Reg(id='rdi'), Reg(id='rdx'), Reg(id='r10'), Reg(id='r11'), Reg(id='r9'), Reg(id='rcx'), Reg(id='r8'), Reg(id='rsi'), Variable(id='a')]
; Variable a has unavailable colors: {0, 1, 2, 3, 4, 5, 6, -4, -1}
; Variable b has unavailable colors: {0, 1, 2, 3, 4, 5, 6, 7, -4, -1}
; Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5, Variable(id='a'): 7, Variable(id='b'): 8}
Register Limit: 11
---------------------*/
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    pushq %r12
    movq $10, %rbx
    movq $20, %r12
    movq $0, %rdi
    callq print_int
    addq %r12, %rbx
    movq %rbx, %rdi
    callq print_int
    movq $0, %rax
    addq $0, %rsp
    popq %r12
    popq %rbx
    popq %rbp
    retq 


