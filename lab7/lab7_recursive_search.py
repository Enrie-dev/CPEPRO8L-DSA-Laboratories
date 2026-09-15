"""
Laboratory Activity No. 7 - Recursion Tracing & Binary Search
Course Code: CPEPRO8L
Course Title: Data Structures and Algorithms

Implements recursive Binary Search and traces each call's arguments
(low, high, mid) so the recursion / stack behavior can be observed.
"""


def recursive_binary_search(arr, low, high, target, trace=False, depth=0):
    """
    Recursively search for `target` in the sorted list `arr`.

    Parameters
    ----------
    arr    : list  - sorted list of comparable elements
    low    : int   - lower index bound of the current search window
    high   : int   - upper index bound of the current search window
    target : any   - value being searched for
    trace  : bool  - if True, print each call's arguments (a simple
                      stack trace) as the recursion unfolds
    depth  : int   - current recursion depth, used only for indenting
                      the trace output

    Returns
    -------
    int : index of `target` in `arr` if found, otherwise -1
    """
    indent = "  " * depth

    # 1. Base Case: search window is empty -> target is not in array.
    if low > high:
        if trace:
            print(f"{indent}Call(low={low}, high={high}, target={target}) "
                  f"-> low > high -> BASE CASE, return -1")
        return -1

    mid = (low + high) // 2

    if trace:
        print(f"{indent}Call(low={low}, high={high}, target={target}) "
              f"-> mid={mid}, arr[mid]={arr[mid]}")

    # 2. Found the target at the midpoint.
    if arr[mid] == target:
        if trace:
            print(f"{indent}  arr[mid] == target -> FOUND at index {mid}")
        return mid

    # 3. Target is smaller than arr[mid] -> search the left half.
    elif arr[mid] > target:
        if trace:
            print(f"{indent}  arr[mid] > target -> recurse LEFT "
                  f"(low={low}, high={mid - 1})")
        return recursive_binary_search(arr, low, mid - 1, target,
                                        trace, depth + 1)

    # 4. Target is larger than arr[mid] -> search the right half.
    else:
        if trace:
            print(f"{indent}  arr[mid] < target -> recurse RIGHT "
                  f"(low={mid + 1}, high={high})")
        return recursive_binary_search(arr, mid + 1, high, target,
                                        trace, depth + 1)


if __name__ == "__main__":
    data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    target_val = 23
    print(f"Searching for {target_val} in {data}")
    print("-" * 60)
    result = recursive_binary_search(data, 0, len(data) - 1, target_val,
                                      trace=True)
    print("-" * 60)
    print(f"Element found at index: {result}")

    print()

    target_val_2 = 56
    print(f"Searching for {target_val_2} in {data}")
    print("-" * 60)
    result_2 = recursive_binary_search(data, 0, len(data) - 1, target_val_2,
                                        trace=True)
    print("-" * 60)
    print(f"Element found at index: {result_2}")
