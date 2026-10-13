	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    movq $2, -8(%rbp)
    movq $4, -8(%rbp)
    movq $6, %rax
    addq $8, %rax
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq -16(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


