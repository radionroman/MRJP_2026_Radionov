	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $64, %rsp
    movq $10, -8(%rbp)
    movq $5, -16(%rbp)
    movq $3, -24(%rbp)
    movq -16(%rbp), %rax
    imulq -16(%rbp), %rax
    movq %rax, -32(%rbp)
    movq $4, %rax
    imulq -8(%rbp), %rax
    movq %rax, -40(%rbp)
    movq -40(%rbp), %rax
    imulq -24(%rbp), %rax
    movq %rax, -48(%rbp)
    movq -32(%rbp), %rax
    subq -48(%rbp), %rax
    movq %rax, -56(%rbp)
    movq -56(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


