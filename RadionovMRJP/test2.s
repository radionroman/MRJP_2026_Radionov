	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $48, %rsp
    movq $2, %rax
    addq $3, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rax
    movq %rax, -16(%rbp)
    negq -16(%rbp)
    movq $10, %rax
    subq $4, %rax
    movq %rax, -24(%rbp)
    movq -16(%rbp), %rax
    imulq -24(%rbp), %rax
    movq %rax, -32(%rbp)
    movq -32(%rbp), %rax
    addq $7, %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


