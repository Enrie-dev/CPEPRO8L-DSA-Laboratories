"""
Laboratory Activity No. 9: Height Balancing in AVL Trees
Course: CPEPRO8L - Data Structures and Algorithms
"""


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, y):
        """Right rotation around y. Returns the new subtree root."""
        x = y.left
        t2 = x.right

        # Rotate
        x.right = y
        y.left = t2

        # Update heights (y first, since it is now the child of x)
        self._update_height(y)
        self._update_height(x)
        return x

    def rotate_left(self, x):
        """Left rotation around x. Returns the new subtree root."""
        y = x.right
        t2 = y.left

        # Rotate
        y.left = x
        x.right = t2

        # Update heights (x first, since it is now the child of y)
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, root, key, verbose=False):
        # 1. Standard BST insertion
        if root is None:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key, verbose)
        elif key > root.key:
            root.right = self.insert(root.right, key, verbose)
        else:
            return root  # duplicates not allowed

        # 2. Update height of this ancestor
        self._update_height(root)

        # 3. Balance factor
        balance = self.get_balance(root)

        # 4. Rebalance if outside [-1, 1]
        if balance > 1 and key < root.left.key:  # LL
            if verbose:
                print(f"  Node {root.key}: balance={balance:+d} -> LL case, rotate right")
            return self.rotate_right(root)

        if balance < -1 and key > root.right.key:  # RR
            if verbose:
                print(f"  Node {root.key}: balance={balance:+d} -> RR case, rotate left")
            return self.rotate_left(root)

        if balance > 1 and key > root.left.key:  # LR
            if verbose:
                print(f"  Node {root.key}: balance={balance:+d} -> LR case, rotate left "
                      f"on {root.left.key} then right on {root.key}")
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        if balance < -1 and key < root.right.key:  # RL
            if verbose:
                print(f"  Node {root.key}: balance={balance:+d} -> RL case, rotate right "
                      f"on {root.right.key} then left on {root.key}")
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    # ---------- helpers for display ----------
    def inorder(self, node):
        return self.inorder(node.left) + [node.key] + self.inorder(node.right) if node else []

    def preorder(self, node):
        return [node.key] + self.preorder(node.left) + self.preorder(node.right) if node else []

    def print_tree(self, node, prefix="", is_left=True):
        """Prints a sideways tree with (height, balance) annotations."""
        if node is None:
            return
        if node.right:
            self.print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ")
              + f"{node.key} (h={node.height}, bf={self.get_balance(node):+d})")
        if node.left:
            self.print_tree(node.left, prefix + ("    " if is_left else "│   "), True)


def demo_sequence(keys, title):
    print("=" * 60)
    print(title)
    print("=" * 60)
    tree = AVLTree()
    root = None
    for k in keys:
        print(f"\nInsert {k}:")
        root = tree.insert(root, k, verbose=True)
        tree.print_tree(root)
    print(f"\nIn-order : {tree.inorder(root)}")
    print(f"Pre-order: {tree.preorder(root)}")
    print(f"Root height: {tree.get_height(root)}\n")
    return tree, root


def main():
    # Required trace: [10, 20, 30] triggers an RR case -> single left rotation
    demo_sequence([10, 20, 30], "Trace 1: Insert [10, 20, 30] (RR case)")

    # Mirror case: LL -> single right rotation
    demo_sequence([30, 20, 10], "Trace 2: Insert [30, 20, 10] (LL case)")

    # Double rotations
    demo_sequence([30, 10, 20], "Trace 3: Insert [30, 10, 20] (LR case)")
    demo_sequence([10, 30, 20], "Trace 4: Insert [10, 30, 20] (RL case)")

    # Sorted data: a plain BST would be a linked list of height 7
    demo_sequence(list(range(1, 8)), "Trace 5: Insert sorted [1..7] (stays balanced)")


if __name__ == "__main__":
    main()
