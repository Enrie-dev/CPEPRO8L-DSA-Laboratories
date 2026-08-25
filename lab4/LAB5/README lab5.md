# Laboratory Activity No. 5 — Stack-Based Parenthesis & Arithmetic Parser

**Course Code:** CPEPRO8L — Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## Objectives

1. Build a custom Stack class using a dynamic list.
2. Design an algorithm to check for balanced bracket pairs `()`, `[]`, `{}`.
3. Understand stack push/pop tracking in expression parsers.

## Files

- `lab5_bracket_parser.py` — contains the `Stack` class (`push`, `pop`, `peek`, `is_empty`) and the `is_balanced()` function, plus a test driver in `__main__`.

## Execution & Output

Run with:

```
python3 lab5_bracket_parser.py
```

Console output:

```
Is {[()()]} balanced? True
Is {[(])} balanced? False

--- Additional test expressions ---
Is (3 + [4 * (2 - 1)]) / {5} balanced? True
Is {[a + (b * c)] - d} balanced? True
Is ((a + b) * (c - d) balanced? False
Is [1, 2, (3, 4)] balanced? True
Is {[(])} balanced? False
```

The two required test cases match the expected results exactly (`True` for `{[()()]}`, `False` for `{[(])}`).

## Report Analysis Questions

**1. Implement the solution and verify it against 5 customized mathematical expressions.**

| # | Expression | Balanced? | Why |
|---|---|---|---|
| 1 | `(3 + [4 * (2 - 1)]) / {5}` | True | Every bracket type opens and closes in properly nested order. |
| 2 | `{[a + (b * c)] - d}` | True | Nesting order `{ [ ( ) ] }` is respected even with variables mixed in. |
| 3 | `((a + b) * (c - d)` | False | The first `(` is never closed — the stack still has one `(` left on it when the string ends, so `stack.is_empty()` returns `False`. |
| 4 | `[1, 2, (3, 4)]` | True | Commas and digits are ignored; only the bracket characters are tracked, and they nest correctly. |
| 5 | `{[(])}` | False | When `]` is encountered, the top of the stack is `(`, not `[`, so the mismatch is caught immediately and the function returns `False`. |

Non-bracket characters (digits, letters, operators, spaces, commas) are simply skipped by the loop — only characters found in `bracket_map` or its values affect the stack, which lets the same function validate arithmetic expressions, array literals, or code snippets, not just plain bracket strings.

**2. Draw the state of the stack at each loop step when evaluating `"{[()]}"`.**

Stack shown bottom → top, left to right. "push" and "pop" describe what happens to the stack *during* that step.

| Step | Char | Action | Stack after step |
|---|---|---|---|
| 1 | `{` | push `{` | `[ { ]` |
| 2 | `[` | push `[` | `[ {, [ ]` |
| 3 | `(` | push `(` | `[ {, [, ( ]` |
| 4 | `)` | pop → got `(`, matches `)` ✓ | `[ {, [ ]` |
| 5 | `]` | pop → got `[`, matches `]` ✓ | `[ { ]` |
| 6 | `}` | pop → got `{`, matches `}` ✓ | `[ ]` (empty) |

After the loop finishes, `stack.is_empty()` is `True`, so `is_balanced("{[()]}")` returns `True`. Each closing bracket always pops exactly the opening bracket that was pushed most recently and still unmatched — this LIFO behavior is precisely what lets a single stack verify correct nesting instead of just counting brackets.
