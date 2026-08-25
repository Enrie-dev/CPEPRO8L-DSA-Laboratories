"""
Laboratory Activity No. 4: Doubly and Circular Linked Lists
Course: CPEPRO8L - Data Structures and Algorithms
"""


class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_head(self, data):
        # Create a new DoubleNode. Link it at the head,
        # ensuring both next and prev pointers are correctly set.
        new_node = DoubleNode(data)
        new_node.next = self.head
        new_node.prev = None

        if self.head is not None:
            self.head.prev = new_node

        self.head = new_node

    def display_forward(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(str(temp.data))
            temp = temp.next
        print("None <-> " + " <-> ".join(elements) + " <-> None")


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularSinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_tail(self, data):
        # Create a new Node. Traverse to the tail node.
        # Connect tail's next to the new node, and the new node's next back
        # to the head.
        # Handle empty list scenario where head.next = head.
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            new_node.next = self.head  # points to itself
            return

        temp = self.head
        while temp.next != self.head:
            temp = temp.next

        temp.next = new_node
        new_node.next = self.head

    def display(self):
        # Traverse and print all elements of the circular list once.
        # Hint: Stop traversing when you loop back to the head.
        if self.head is None:
            print("Empty list")
            return

        elements = []
        temp = self.head
        while True:
            elements.append(str(temp.data))
            temp = temp.next
            if temp == self.head:
                break

        print(" -> ".join(elements) + f" -> (loops to {self.head.data})")


if __name__ == "__main__":
    print("--- Testing Doubly Linked List ---")
    dll = DoublyLinkedList()
    dll.insert_head(5)
    dll.insert_head(10)
    dll.display_forward()  # Expected: None <-> 10 <-> 5 <-> None

    print("\n--- Testing Circular Linked List ---")
    cll = CircularSinglyLinkedList()
    cll.insert_tail(100)
    cll.insert_tail(200)
    cll.insert_tail(300)
    cll.display()  # Expected: 100 -> 200 -> 300 -> (loops to 100)