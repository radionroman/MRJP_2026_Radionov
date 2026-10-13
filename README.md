Run with including runtime.c in gcc command to avoid undefined reference to `printf` error.


```
uv run compiler.py input_file.lqua > output_file.s
gcc  -o output_program output_file.s ../support/runtime.c
./output_program
```