import ctypes


class DynamicArray:
    def __init__(self):
        self.size = 0        # number of elements
        self.capacity = 1    # initial capacity
        self.array = self._make_array(self.capacity)

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        # Check if the index is valid. If not, raise IndexError.
        # Otherwise, return the element at the index.
        if not 0 <= index < self.size:
            raise IndexError(f"Index {index} out of bounds for size {self.size}")
        return self.array[index]

    def append(self, element):
        # Check if size equals capacity. If so, call _resize to double capacity.
        # Then, place the element at the current size index, and increment size.
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        self.array[self.size] = element
        self.size += 1

    def _resize(self, new_capacity):
        # 1. Print capacity change trace.
        # 2. Make a new array with new_capacity.
        # 3. Copy elements from self.array to the new array.
        # 4. Reassign self.array and self.capacity.
        print(f"  [RESIZE] size={self.size} hit capacity={self.capacity} "
              f"-> allocating new capacity={new_capacity}, copying {self.size} elements")

        new_array = self._make_array(new_capacity)
        for i in range(self.size):
            new_array[i] = self.array[i]

        self.array = new_array
        self.capacity = new_capacity

    def _make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()


# Testing script
if __name__ == "__main__":
    arr = DynamicArray()
    for i in range(10):
        arr.append(i)
        print(f"Appending {i} | Size: {len(arr)} | Capacity: "
              f"{arr.capacity} | Element at index {i}: {arr[i]}")
