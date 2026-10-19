
	.globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $16, %rsp
    callq input_int
    movq %rax, -8(%rbp)
    callq input_int
    movq %rax, -16(%rbp)
    movq -8(%rbp), %rax
    imulq -16(%rbp), %rax
    movq %rax, -16(%rbp)
    movq -16(%rbp), %rdi
    callq print_int
    movq $0, %rax
    movq %rbp, %rsp
    popq %rbp
    retq 


