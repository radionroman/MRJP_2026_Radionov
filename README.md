Open /RadionovMRJP and run the following commands in the terminal to compile and execute the test files:
```
uv run compiler.py test1.lqua > test1.s
gcc  -o test1 test1.s ../support/runtime.c
./test1
```

```
uv run compiler.py test2.lqua > test2.s
gcc  -o test2 test2.s ../support/runtime.c
./test2
```

```
uv run compiler.py test3.lqua > test3.s
gcc  -o test3 test3.s ../support/runtime.c
./test3
```
