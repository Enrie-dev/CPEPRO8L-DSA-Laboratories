"""
Laboratory Activity No. 5: Stack-Based Parenthesis & Arithmetic Parser
Course: CPEPRO8L - Data Structures and Algorithms
"""


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        # Append the item to the items list.
        self.items.append(item)

    def pop(self):
        # Pop and return the last item from the list.
        # Check if empty first and raise IndexError if so.
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if not self.is_empty() else None


def is_balanced(expression):
    stack = Stack()
    bracket_map = {')': '(', '}': '{', ']': '['}
    opening = set(bracket_map.values())

    for char in expression:
        # If char is an opening bracket, push it to stack.
        # If it is a closing bracket, pop from stack and check if it matches.
        # If stack is empty or doesn't match, return False.
        if char in opening:
            stack.push(char)
        elif char in bracket_map:
            if stack.is_empty():
                return False
            top = stack.pop()
            if top != bracket_map[char]:
                return False
        # any other character (digits, operators, letters) is ignored

    return stack.is_empty()


if __name__ == "__main__":
    expr1 = "{[()()]}"
    expr2 = "{[(])}"
    print(f"Is {expr1} balanced? {is_balanced(expr1)}")  # Expected: True
    print(f"Is {expr2} balanced? {is_balanced(expr2)}")  # Expected: False

    print("\n--- Additional test expressions ---")
    test_expressions = [
        "(3 + [4 * (2 - 1)]) / {5}",   # balanced, mixed math expression
        "{[a + (b * c)] - d}",          # balanced, with variables
        "((a + b) * (c - d)",           # unbalanced: missing closing )
        "[1, 2, (3, 4)]",               # balanced
        "{[(])}",                       # unbalanced: wrong nesting order
    ]
    for expr in test_expressions:
        print(f"Is {expr} balanced? {is_balanced(expr)}")
