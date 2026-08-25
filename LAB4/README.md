# Laboratory Activity No. 4 — Doubly and Circular Linked Lists

**Course Code:** CPEPRO8L — Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## Objectives

1. Implement a Doubly Linked List with `next` and `prev` pointers.
2. Build a Circular Singly Linked List that correctly wraps the tail link back to the head.
3. Differentiate traversal termination strategies across linear and circular lists.

## Files

- `lab4_doubly_circular.py` — contains the `DoubleNode`/`DoublyLinkedList` classes and the `Node`/`CircularSinglyLinkedList` classes, plus a test driver in `__main__`.

## Execution & Output

Run with:

```
python3 lab4_doubly_circular.py
```

Console output:

```
--- Testing Doubly Linked List ---
None <-> 10 <-> 5 <-> None

--- Testing Circular Linked List ---
100 -> 200 -> 300 -> (loops to 100)
```

Both results match the expected output specified in the activity: `insert_head` correctly places new nodes at the front while keeping `prev`/`next` consistent in both directions, and `insert_tail` correctly appends to the circular list while preserving the wrap-around link from the tail back to the head.

## Report Analysis Questions

**1. Complete the classes and verify they execute without compile or runtime errors.**

Both classes were completed and the script above executes cleanly with no exceptions. `DoublyLinkedList.insert_head` allocates a `DoubleNode`, sets its `next` to the current head, sets its `prev` to `None` (since it is the new front), updates the old head's `prev` to point back to the new node (only when a head already existed, to avoid a `NoneType` error on an empty list), and finally reassigns `self.head`. `CircularSinglyLinkedList.insert_tail` handles two cases: an empty list, where the new node is made to point to itself (`new_node.next = new_node`) and becomes the head; and a non-empty list, where the code walks the list until it finds the node whose `next` points back to `self.head` (the current tail), then relinks that tail's `next` to the new node and sets the new node's `next` back to `self.head`.

**2. Explain the termination condition in a loop traversal of a Circular Linked List to prevent infinite loops.**

A circular linked list has no `None` terminator — the last node's `next` points back to the head instead of to `None`, so a `while temp:` loop (the pattern used for a linear list) never becomes false and would loop forever. To terminate correctly, traversal must instead check whether the current pointer has come back around to the starting node. The standard pattern is a `do-while`-style loop: visit the head first, advance `temp = temp.next`, and after each step check `if temp == head: break`. This guarantees the loop runs exactly once per node — each node is visited exactly once, and the loop stops the moment it detects it has completed a full cycle back to its starting point, rather than waiting for a `None` that will never appear.
