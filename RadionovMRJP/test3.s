	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $48, %rsp
    callq input_int
    movq %rax, -8(%rbp)
    callq input_int
    movq %rax, -16(%rbp)
    callq input_int
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    addq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -8(%rbp), %rax
    subq -32(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


