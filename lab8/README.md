# Laboratory Activity No. 8: Binary Search Tree Insertion and Traversals

**Course Code:** CPEPRO8L  **Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026-2027

## Objectives

1. Implement dynamic tree nodes with left and right child references.
2. Build insertion and lookup functions in a BST.
3. Implement Inorder, Preorder, and Postorder recursive tree traversals.

## Files

| File | Description |
|---|---|
| `lab8_bst.py` | `TreeNode` and `BST` with `insert`, `search`, `inorder`, `preorder`, `postorder` |
| `sample_output.txt` | Console capture of `python lab8_bst.py` |

## How to Run

```bash
python lab8_bst.py
```

No external libraries are needed (Python 3.8+).

## Implementation Summary

- **`_insert_recursive`:** if `key < node.key`, go left (create the node if the left child is empty, otherwise recurse). Otherwise go right in the same way. Duplicates go to the right subtree.
- **`search`:** walks down from the root, going left or right by comparison, until the key is found or a `None` child is reached.
- **Traversals:** each is recursive and prints keys on one line. They differ only in when the node is visited:

| Traversal | Order |
|---|---|
| Inorder | Left -> Node -> Right |
| Preorder | Node -> Left -> Right |
| Postorder | Left -> Right -> Node |

## Execution & Output

Test tree, built by inserting `[50, 30, 70, 20, 40, 60, 80]`:

```text
         50
       /    \
     30      70
    /  \    /  \
  20   40  60   80
```

Console output:

```text
Inorder Traversal:
20 30 40 50 60 70 80 
Preorder Traversal:
50 30 20 40 70 60 80 
Postorder Traversal:
20 40 30 60 80 70 50 
Lookup:
search(60) -> True
search(25) -> False
```

## Report Analysis Questions

### 1. Complete all traversals and write down the Preorder and Postorder outputs for the test tree.

| Traversal | Output |
|---|---|
| Preorder (Node, Left, Right) | `50 30 20 40 70 60 80` |
| Postorder (Left, Right, Node) | `20 40 30 60 80 70 50` |
| Inorder (Left, Node, Right) | `20 30 40 50 60 70 80` |

**Preorder trace:** visit 50, then go left: visit 30, then 20 (leaf), then 40 (leaf). Back at 50, go right: visit 70, then 60 (leaf), then 80 (leaf).

**Postorder trace:** go as far left as possible. 20 and 40 are visited first, then their parent 30. Next 60 and 80 are visited, then their parent 70. The root 50 comes last.

### 2. Explain why the inorder traversal of a BST outputs items in sorted order.

The BST property says that for every node, all keys in the left subtree are smaller than the node and all keys in the right subtree are larger. Inorder traversal visits **left subtree, then node, then right subtree**, so at every node it prints all the smaller keys first, then the node itself, then all the larger keys.

This can be shown by induction on the number of nodes:

- **Base case:** an empty tree or a single node outputs nothing or one key, which is trivially sorted.
- **Inductive step:** assume inorder outputs sorted order for both subtrees of a node `n`. The output is `sorted(left) + [n] + sorted(right)`. Every key in `left` is less than `n`, and every key in `right` is greater than `n`, so the whole sequence is sorted.

In the test tree: the left subtree of 50 outputs `20 30 40` (all < 50), then 50 is printed, then the right subtree outputs `60 70 80` (all > 50), giving `20 30 40 50 60 70 80`.

Because of this, inorder traversal costs O(n) and gives a sorted listing without a separate sort. (With duplicates sent right, equal keys appear adjacent, so the output is still non-decreasing.)
