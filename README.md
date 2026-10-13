Run with


```
uv run RadionovMRJP/compiler.py input_file.lqua > output_file.s
gcc  -o output_program output_file.s /support/runtime.c
./output_program
```
