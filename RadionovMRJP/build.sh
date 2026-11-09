for name in test1 test2 test3 test4 test5; do
    uv run compiler.py "$name.lqua" --register-limit 11 > "$name.s" &&
    gcc -o "$name" "$name.s" ../support/runtime.c || break
done