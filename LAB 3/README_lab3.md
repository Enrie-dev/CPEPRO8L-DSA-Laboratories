# Laboratory Activity No. 3 — Singly Linked List CRUD Operations

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

At the end of this activity, the student is able to:

1. Construct custom `Node` and `SinglyLinkedList` classes.
2. Implement insertion at the head, tail, and specific values.
3. Manage list nodes and pointers cleanly without losing references.

## 2. Repository Contents

| File | Description |
|---|---|
| `lab3_singly_linked_list.py` | Completed `Node` and `SinglyLinkedList` classes (`insert_head`, `insert_tail`, `delete_value`, `search`, `display`), plus a test driver covering insertion, search, and deletion (head/middle/tail cases). |
| `README.md` | This documentation file. |

The script was run with Python 3 in a Linux sandbox environment; the trace below is the actual console output.

## 3. Implementation Notes

- **`insert_head(data)`** — wraps `data` in a new `Node`, points the new node's `next` at the current `self.head`, then rebinds `self.head` to the new node. O(1) — no traversal needed.
- **`insert_tail(data)`** — handles the empty-list case first (`self.head is None` → the new node simply becomes `self.head`). Otherwise it walks from `self.head` until it finds the node whose `next` is `None` (the tail) and links that node's `next` to the new node. O(n), since it must walk the whole list to find the end.
- **`delete_value(target)`** — walks the list with two pointers, `previous` and `current`. When `current.data == target` is found: if `previous is None` the target was the head, so `self.head` is simply advanced to `current.next`; otherwise `previous.next` is rewired to skip over `current` and point directly at `current.next`. The removed node's own `next` is cleared to fully detach it. Returns `True` on success, `False` if the value was never found (loop runs off the end with `current` becoming `None`).
- **`search(target)`** — linear traversal comparing `temp.data` against `target`, returning `True` on a match and `False` after exhausting the list. O(n).

## 4. Execution & Output

Script: `lab3_singly_linked_list.py`

```
20 -> 10 -> 30 -> None
20 -> 30 -> None
Is 30 in list? True
Is 10 in list? False
Deleting 999 (not present): False
5 -> 20 -> 30 -> 40 -> None
5 -> 30 -> 40 -> None
30 -> 40 -> None
30 -> None
```

This matches the two outputs specified in the activity exactly:

- After `insert_head(10)`, `insert_head(20)`, `insert_tail(30)` → `20 -> 10 -> 30 -> None` ✅
- After `delete_value(10)` → `20 -> 30 -> None` ✅
- `search(30)` → `True` ✅

The remaining lines were added to more thoroughly exercise the CRUD operations beyond the minimum required trace:

| Operation | Result | What it confirms |
|---|---|---|
| `search(10)` after deletion | `False` | Deleted nodes are truly gone, not just unlinked from `display()` |
| `delete_value(999)` | `False` | Deleting a value that doesn't exist fails gracefully instead of crashing |
| `insert_tail(40)`, `insert_head(5)` | `5 -> 20 -> 30 -> 40 -> None` | Head and tail insertion both still work correctly on a non-empty list |
| `delete_value(20)` | `5 -> 30 -> 40 -> None` | Deleting a genuine **middle** node (traced in detail below) |
| `delete_value(5)` | `30 -> 40 -> None` | Deleting the **head** node |
| `delete_value(40)` | `30 -> None` | Deleting the **tail** node |

## 5. Analysis Questions

**Run the completed script and include console outputs showing insertion, search, and deletion.**

See Section 4 above — the full console trace demonstrates insertion (`insert_head`, `insert_tail`), search (`search(30)`, `search(10)`), and deletion (`delete_value` for a not-found value, a middle node, the head node, and the tail node).

**Trace the pointers step-by-step when deleting the middle node.**

Using the state right before `delete_value(20)` is called, the list is:

```
head -> [5] -> [20] -> [30] -> [40] -> None
```

Step-by-step trace of `delete_value(20)`:

1. **Initialize:** `previous = None`, `current = self.head` → `current` points at node `[5]`.
2. **Iteration 1:** `current.data` is `5`, which is not `20`. Move forward: `previous = current` (now `[5]`), `current = current.next` (now `[20]`).
3. **Iteration 2:** `current.data` is `20` — **match found**. `previous` is `[5]`, which is not `None`, so this is not a head deletion.
4. **Relink:** execute `previous.next = current.next`. `current.next` is node `[30]`, so `[5].next` is reassigned from `[20]` to `[30]`. At this instant, both `[5]` and the original `[20].next` point at `[30]`, but `[20]` is no longer reachable by walking from `head`, since nothing points at it anymore.
5. **Detach:** execute `current.next = None`, clearing `[20]`'s own `next` pointer so the removed node doesn't retain a dangling link into the rest of the list (and so nothing accidentally re-enters the list through it later).
6. **Return:** `True` is returned, signaling a successful deletion.

Resulting structure:

```
head -> [5] -> [30] -> [40] -> None
```

The key insight is that **only one pointer changes** to remove a middle node — `previous.next` is redirected around the target node — which is why deletion from a linked list is O(1) *once the target node has been located* (the O(n) cost is entirely in the search/traversal to find `previous` and `current`, not in the removal itself). This is in contrast to an array-based structure, where deleting a middle element requires shifting every subsequent element left by one position.
