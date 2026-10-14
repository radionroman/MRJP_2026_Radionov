	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    movq $1, -8(%rbp)
    movq $2, -16(%rbp)
    movq -8(%rbp), %rax
    addq -16(%rbp), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq -8(%rbp), %rax
    addq $10, %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq $10, %rax
    addq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq -16(%rbp), %rax
    addq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq -8(%rbp), %rax
    addq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq -8(%rbp), %rax
    movq %rax, -8(%rbp)
    negq -8(%rbp)
    movq -8(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


