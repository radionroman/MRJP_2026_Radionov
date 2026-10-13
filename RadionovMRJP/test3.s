	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $32, %rsp
    movq $10, -8(%rbp)
    movq $2, -16(%rbp)
    negq -16(%rbp)
    movq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    negq -8(%rbp)
    movq -16(%rbp), %rax
    subq -8(%rbp), %rax
    movq %rax, -24(%rbp)
    movq -24(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


