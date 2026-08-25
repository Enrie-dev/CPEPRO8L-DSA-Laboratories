"""
Laboratory Activity No. 6: Circular Queue Buffer Implementation
Course: CPEPRO8L - Data Structures and Algorithms
"""


class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0

    def is_full(self):
        return self.size == self.capacity

    def is_empty(self):
        return self.size == 0

    def enqueue(self, item):
        # If full, print overflow warning and return False.
        # Otherwise, insert item at tail, increment size, and update tail circularly.
        if self.is_full():
            print(f"Overflow! Cannot enqueue {item}, queue is full.")
            return False

        self.queue[self.tail] = item
        self.size += 1
        self.tail = (self.tail + 1) % self.capacity
        return True

    def dequeue(self):
        # If empty, print underflow warning and return None.
        # Otherwise, retrieve head item, set position to None, decrement size,
        # and update head circularly.
        if self.is_empty():
            print("Underflow! Cannot dequeue, queue is empty.")
            return None

        item = self.queue[self.head]
        self.queue[self.head] = None
        self.size -= 1
        self.head = (self.head + 1) % self.capacity
        return item

    def display(self):
        print(f"Queue array: {self.queue} | Head: {self.head} | Tail: {self.tail}")


if __name__ == "__main__":
    cq = CircularQueue(5)
    cq.enqueue(1)
    cq.enqueue(2)
    cq.enqueue(3)
    print(f"Dequeued: {cq.dequeue()}")  # Expected: Dequeued: 1
    cq.enqueue(4)
    cq.display()

    print("\n--- 10-operation trace (capacity 5) ---")
    cq2 = CircularQueue(5)
    ops = [
        ("enqueue", 10), ("enqueue", 20), ("enqueue", 30),
        ("dequeue", None), ("enqueue", 40), ("enqueue", 50),
        ("enqueue", 60), ("dequeue", None), ("enqueue", 70),
        ("enqueue", 80),
    ]
    for op, val in ops:
        if op == "enqueue":
            cq2.enqueue(val)
            print(f"enqueue({val}) ->", end=" ")
        else:
            result = cq2.dequeue()
            print(f"dequeue() = {result} ->", end=" ")
        cq2.display()
