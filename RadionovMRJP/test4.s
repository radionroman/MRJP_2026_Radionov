/*---------------------
Live After Mapping:
    callq print_int: set()
    movq total, %rdi: {Reg(id='rdi')}
    addq e, total: {Variable(id='total')}
    addq d, total: {Variable(id='total'), Variable(id='e')}
    addq c, total: {Variable(id='total'), Variable(id='d'), Variable(id='e')}
    addq b, total: {Variable(id='total'), Variable(id='d'), Variable(id='c'), Variable(id='e')}
    movq a, total: {Variable(id='total'), Variable(id='b'), Variable(id='e'), Variable(id='d'), Variable(id='c')}
    movq $5, e: {Variable(id='b'), Variable(id='e'), Variable(id='d'), Variable(id='a'), Variable(id='c')}
    movq $4, d: {Variable(id='a'), Variable(id='b'), Variable(id='d'), Variable(id='c')}
    movq $3, c: {Variable(id='a'), Variable(id='b'), Variable(id='c')}
    movq $2, b: {Variable(id='a'), Variable(id='b')}
    movq $1, a: {Variable(id='a')}
Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5}
Interference Graph:
  %rdi: []
  %rax: []
  %r9: []
  %r10: []
  %rdx: []
  %r11: []
  %rsi: []
  %r8: []
  %rcx: []
  total: [Variable(id='e'), Variable(id='d'), Variable(id='c'), Variable(id='b')]
  e: [Variable(id='total'), Variable(id='b'), Variable(id='d'), Variable(id='a'), Variable(id='c')]
  d: [Variable(id='total'), Variable(id='e'), Variable(id='a'), Variable(id='b'), Variable(id='c')]
  c: [Variable(id='total'), Variable(id='e'), Variable(id='d'), Variable(id='a'), Variable(id='b')]
  b: [Variable(id='total'), Variable(id='e'), Variable(id='d'), Variable(id='c'), Variable(id='a')]
  a: [Variable(id='e'), Variable(id='d'), Variable(id='c'), Variable(id='b')]
; Variable a has unavailable colors: set()
; Variable b has unavailable colors: {0}
; Variable c has unavailable colors: {0, 1}
; Variable d has unavailable colors: {0, 1, 2}
; Variable e has unavailable colors: {0, 1, 2, 3}
; Variable total has unavailable colors: {1, 2, 3, 4}
; Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5, Variable(id='a'): 0, Variable(id='b'): 1, Variable(id='c'): 2, Variable(id='d'): 3, Variable(id='e'): 4, Variable(id='total'): 0}
Register Limit: 11
---------------------*/
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    movq $1, %rcx
    movq $2, %rdx
    movq $3, %rsi
    movq $4, %rdi
    movq $5, %r8
    addq %rdx, %rcx
    addq %rsi, %rcx
    addq %rdi, %rcx
    addq %r8, %rcx
    movq %rcx, %rdi
    callq print_int
    movq $0, %rax
    addq $0, %rsp
    popq %rbp
    retq 


