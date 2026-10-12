"""
Laboratory Activity No. 8: Binary Search Tree Insertion and Traversals
Course: CPEPRO8L - Data Structures and Algorithms
"""


class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = TreeNode(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        # Smaller keys go to the left subtree, otherwise to the right.
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        """Lookup: returns True if key exists in the tree."""
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def inorder(self, node):
        # Left -> Node -> Right
        if node:
            self.inorder(node.left)
            print(node.key, end=" ")
            self.inorder(node.right)

    def preorder(self, node):
        # Node -> Left -> Right
        if node:
            print(node.key, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        # Left -> Right -> Node
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.key, end=" ")


if __name__ == "__main__":
    tree = BST()
    elements = [50, 30, 70, 20, 40, 60, 80]
    for el in elements:
        tree.insert(el)

    print("Inorder Traversal:")
    tree.inorder(tree.root)  # Expected: Sorted order (20 30 40 50 60 70 80)
    print()

    print("Preorder Traversal:")
    tree.preorder(tree.root)
    print()

    print("Postorder Traversal:")
    tree.postorder(tree.root)
    print()

    print("Lookup:")
    for k in (60, 25):
        print(f"search({k}) -> {tree.search(k)}")
