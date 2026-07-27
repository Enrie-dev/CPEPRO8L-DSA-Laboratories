class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_head(self, data):
        # Create a new node. Link its next to head, and update head.
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_tail(self, data):
        # Create a new node. Traverse to the tail node, and link its next to the new node.
        # Handle the case where the list is empty first.
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        temp = self.head
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node

    def delete_value(self, target):
        # Search and delete the node containing the target value.
        # Be careful to link the previous node's next pointer to the
        # current node's next pointer.
        # Return True if successfully deleted, False otherwise.
        current = self.head
        previous = None

        while current is not None:
            if current.data == target:
                if previous is None:
                    # Deleting the head node
                    self.head = current.next
                else:
                    previous.next = current.next
                current.next = None  # detach the removed node cleanly
                return True
            previous = current
            current = current.next

        return False

    def search(self, target):
        # Search for target in the list. Return True if found, False otherwise.
        temp = self.head
        while temp is not None:
            if temp.data == target:
                return True
            temp = temp.next
        return False

    def display(self):
        temp = self.head
        elements = []
        while temp:
            elements.append(str(temp.data))
            temp = temp.next
        print(" -> ".join(elements) + " -> None")


if __name__ == "__main__":
    sll = SinglyLinkedList()
    sll.insert_head(10)
    sll.insert_head(20)
    sll.insert_tail(30)
    sll.display()  # Expected: 20 -> 10 -> 30 -> None
    sll.delete_value(10)
    sll.display()  # Expected: 20 -> 30 -> None
    print(f"Is 30 in list? {sll.search(30)}")  # Expected: True

    # Extra checks to more fully exercise CRUD behavior
    print(f"Is 10 in list? {sll.search(10)}")            # Expected: False (already deleted)
    print(f"Deleting 999 (not present): {sll.delete_value(999)}")  # Expected: False
    sll.insert_tail(40)
    sll.insert_head(5)
    sll.display()  # Expected: 5 -> 20 -> 30 -> 40 -> None
    sll.delete_value(20)  # delete a true middle node
    sll.display()  # Expected: 5 -> 30 -> 40 -> None
    sll.delete_value(5)   # delete head
    sll.display()  # Expected: 30 -> 40 -> None
    sll.delete_value(40)  # delete tail
    sll.display()  # Expected: 30 -> None
