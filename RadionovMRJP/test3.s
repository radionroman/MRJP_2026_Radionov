/*---------------------
Live After Mapping:
    callq print_int: set()
    movq %tmp1, %rdi: {Reg(id='rdi')}
    addq b, %tmp1: {Variable(id='%tmp1')}
    movq a, %tmp1: {Variable(id='%tmp1'), Variable(id='b')}
    callq print_int: {Variable(id='a'), Variable(id='b')}
    movq b, %rdi: {Variable(id='a'), Reg(id='rdi'), Variable(id='b')}
    callq print_int: {Variable(id='a'), Variable(id='b')}
    movq a, %rdi: {Variable(id='a'), Reg(id='rdi'), Variable(id='b')}
    movq %rax, b: {Variable(id='a'), Variable(id='b')}
    callq input_int: {Variable(id='a'), Reg(id='rax')}
    movq %rax, a: {Variable(id='a')}
    callq input_int: {Reg(id='rax')}
Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5}
Interference Graph:
  %rcx: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %rdx: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %r11: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %rsi: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %rax: [Variable(id='a'), Variable(id='b'), Reg(id='rcx'), Reg(id='rdx'), Reg(id='r11'), Reg(id='rsi'), Reg(id='r8'), Reg(id='r9'), Reg(id='rdi'), Reg(id='r10')]
  %r8: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %r9: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %rdi: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %r10: [Variable(id='a'), Variable(id='b'), Reg(id='rax')]
  %tmp1: [Variable(id='b')]
  b: [Variable(id='%tmp1'), Reg(id='rcx'), Reg(id='rdx'), Reg(id='r11'), Reg(id='rsi'), Reg(id='rax'), Reg(id='r8'), Reg(id='r9'), Reg(id='rdi'), Reg(id='r10'), Variable(id='a')]
  a: [Reg(id='rcx'), Reg(id='rdx'), Reg(id='r11'), Reg(id='rsi'), Reg(id='rax'), Reg(id='r8'), Reg(id='r9'), Reg(id='rdi'), Reg(id='r10'), Variable(id='b')]
; Variable %tmp1 has unavailable colors: set()
; Variable a has unavailable colors: {0, 1, 2, 3, 4, 5, 6, -4, -1}
; Variable b has unavailable colors: {0, 1, 2, 3, 4, 5, 6, 7, -4, -1}
; Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5, Variable(id='%tmp1'): 0, Variable(id='a'): 7, Variable(id='b'): 8}
Register Limit: 11
---------------------*/
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    pushq %r12
    callq input_int
    movq %rax, %rbx
    callq input_int
    movq %rax, %r12
    movq %rbx, %rdi
    callq print_int
    movq %r12, %rdi
    callq print_int
    movq %rbx, %rcx
    addq %r12, %rcx
    movq %rcx, %rdi
    callq print_int
    movq $0, %rax
    addq $0, %rsp
    popq %r12
    popq %rbx
    popq %rbp
    retq 


