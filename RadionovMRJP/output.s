	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    movq $10, -8(%rbp)
    movq $3, -16(%rbp)
    movq $3, %rax
    addq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


