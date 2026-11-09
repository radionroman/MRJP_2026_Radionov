/*---------------------
Live After Mapping:
    callq print_int: set()
    movq %tmp4, %rdi: {Reg(id='rdi')}
    addq ogon, %tmp4: {Variable(id='%tmp4')}
    movq %tmp3, %tmp4: {Variable(id='%tmp4'), Variable(id='ogon')}
    addq a4, %tmp3: {Variable(id='ogon'), Variable(id='%tmp3')}
    movq %tmp2, %tmp3: {Variable(id='ogon'), Variable(id='%tmp3'), Variable(id='a4')}
    addq a3, %tmp2: {Variable(id='%tmp2'), Variable(id='ogon'), Variable(id='a4')}
    movq %tmp1, %tmp2: {Variable(id='%tmp2'), Variable(id='ogon'), Variable(id='a4'), Variable(id='a3')}
    addq a2, %tmp1: {Variable(id='ogon'), Variable(id='a4'), Variable(id='a3'), Variable(id='%tmp1')}
    movq a1, %tmp1: {Variable(id='ogon'), Variable(id='a2'), Variable(id='a4'), Variable(id='a3'), Variable(id='%tmp1')}
    movq $0, ogon: {Variable(id='ogon'), Variable(id='a4'), Variable(id='a3'), Variable(id='a2'), Variable(id='a1')}
    movq %rax, a4: {Variable(id='a1'), Variable(id='a4'), Variable(id='a3'), Variable(id='a2')}
    callq input_int: {Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')}
    movq %rax, a3: {Variable(id='a1'), Variable(id='a3'), Variable(id='a2')}
    callq input_int: {Variable(id='a1'), Reg(id='rax'), Variable(id='a2')}
    movq %rax, a2: {Variable(id='a1'), Variable(id='a2')}
    callq input_int: {Variable(id='a1'), Reg(id='rax')}
    movq %rax, a1: {Variable(id='a1')}
    callq input_int: {Reg(id='rax')}
Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5}
Interference Graph:
  %rdi: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %r8: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %rsi: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %rax: [Reg(id='rdi'), Reg(id='r8'), Reg(id='rsi'), Variable(id='a1'), Variable(id='a3'), Variable(id='a2'), Reg(id='rdx'), Reg(id='r11'), Reg(id='r9'), Reg(id='r10'), Reg(id='rcx')]
  %rdx: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %r11: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %r9: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %r10: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %rcx: [Variable(id='a1'), Reg(id='rax'), Variable(id='a3'), Variable(id='a2')]
  %tmp4: [Variable(id='ogon')]
  ogon: [Variable(id='%tmp4'), Variable(id='%tmp3'), Variable(id='%tmp2'), Variable(id='%tmp1'), Variable(id='a4'), Variable(id='a3'), Variable(id='a2'), Variable(id='a1')]
  %tmp3: [Variable(id='ogon'), Variable(id='a4')]
  a4: [Variable(id='%tmp3'), Variable(id='%tmp2'), Variable(id='%tmp1'), Variable(id='ogon'), Variable(id='a1'), Variable(id='a3'), Variable(id='a2')]
  %tmp2: [Variable(id='ogon'), Variable(id='a4'), Variable(id='a3')]
  a3: [Variable(id='%tmp2'), Variable(id='%tmp1'), Variable(id='ogon'), Variable(id='a4'), Reg(id='rdi'), Reg(id='r8'), Reg(id='rsi'), Reg(id='rax'), Reg(id='rdx'), Reg(id='r11'), Reg(id='r9'), Reg(id='r10'), Reg(id='rcx'), Variable(id='a1'), Variable(id='a2')]
  %tmp1: [Variable(id='ogon'), Variable(id='a4'), Variable(id='a3'), Variable(id='a2')]
  a2: [Variable(id='%tmp1'), Variable(id='ogon'), Variable(id='a4'), Reg(id='rdi'), Reg(id='r8'), Reg(id='rsi'), Reg(id='rax'), Reg(id='rdx'), Reg(id='r11'), Reg(id='r9'), Reg(id='r10'), Reg(id='rcx'), Variable(id='a3'), Variable(id='a1')]
  a1: [Variable(id='ogon'), Variable(id='a4'), Reg(id='rdi'), Reg(id='r8'), Reg(id='rsi'), Reg(id='rax'), Reg(id='rdx'), Reg(id='r11'), Reg(id='r9'), Reg(id='r10'), Reg(id='rcx'), Variable(id='a3'), Variable(id='a2')]
; Variable %tmp1 has unavailable colors: set()
; Variable %tmp2 has unavailable colors: set()
; Variable %tmp3 has unavailable colors: set()
; Variable %tmp4 has unavailable colors: set()
; Variable a1 has unavailable colors: {0, 1, 2, 3, 4, 5, 6, -4, -1}
; Variable a2 has unavailable colors: {0, 1, 2, 3, 4, 5, 6, 7, -4, -1}
; Variable a3 has unavailable colors: {0, 1, 2, 3, 4, 5, 6, 7, 8, -4, -1}
; Variable a4 has unavailable colors: {0, 9, 8, 7}
; Variable ogon has unavailable colors: {0, 1, 7, 8, 9}
; Colors after assigning allocatable and reserved registers: {Reg(id='rcx'): 0, Reg(id='rdx'): 1, Reg(id='rsi'): 2, Reg(id='rdi'): 3, Reg(id='r8'): 4, Reg(id='r9'): 5, Reg(id='r10'): 6, Reg(id='rbx'): 7, Reg(id='r12'): 8, Reg(id='r13'): 9, Reg(id='r14'): 10, Reg(id='rax'): -1, Reg(id='rsp'): -2, Reg(id='rbp'): -3, Reg(id='r11'): -4, Reg(id='r15'): -5, Variable(id='%tmp1'): 0, Variable(id='%tmp2'): 0, Variable(id='%tmp3'): 0, Variable(id='%tmp4'): 0, Variable(id='a1'): 7, Variable(id='a2'): 8, Variable(id='a3'): 9, Variable(id='a4'): 1, Variable(id='ogon'): 2}
Register Limit: 11
---------------------*/
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    pushq %rbx
    pushq %r12
    pushq %r13
    subq $8, %rsp
    callq input_int
    movq %rax, %rbx
    callq input_int
    movq %rax, %r12
    callq input_int
    movq %rax, %r13
    callq input_int
    movq %rax, %rdx
    movq $0, %rsi
    movq %rbx, %rcx
    addq %r12, %rcx
    addq %r13, %rcx
    addq %rdx, %rcx
    addq %rsi, %rcx
    movq %rcx, %rdi
    callq print_int
    movq $0, %rax
    addq $8, %rsp
    popq %r13
    popq %r12
    popq %rbx
    popq %rbp
    retq 


