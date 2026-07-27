import time

# O(1) Constant Time Function
def constant_time_check(arr):
    # Returns the first element of the array
    return arr[0] if len(arr) > 0 else None

# O(n) Linear Time Function
def linear_time_sum(arr):
    total = 0
    for value in arr:
        total += value
    return total

# O(n^2) Quadratic Time Function
def quadratic_time_pairs(arr):
    pair_sum = 0
    n = len(arr)
    for i in range(n):
        for j in range(n):
            pair_sum += (arr[i] * arr[j])
    return pair_sum

# Benchmarking Logic
N_values = [100, 500, 1000, 5000, 10000]

results = []

for n in N_values:
    test_list = list(range(n))
    print(f"\n--- Benchmarking N = {n} ---")

    # 1. Profile O(1)
    start = time.perf_counter()
    constant_time_check(test_list)
    t_constant = (time.perf_counter() - start) * 1_000_000  # microseconds

    # 2. Profile O(n)
    start = time.perf_counter()
    linear_time_sum(test_list)
    t_linear = (time.perf_counter() - start) * 1_000_000

    # 3. Profile O(n^2)
    # Hint: Skip N = 10000 for O(n^2) if it runs too slowly on your system!
    if n <= 5000:
        start = time.perf_counter()
        quadratic_time_pairs(test_list)
        t_quadratic = (time.perf_counter() - start) * 1_000_000
        q_text = f"{t_quadratic:.2f} us"
    else:
        q_text = "SKIPPED (too slow)"

    print(f"Constant time: {t_constant:.2f} us")
    print(f"Linear time:   {t_linear:.2f} us")
    print(f"Quadratic time: {q_text}")

    results.append((n, t_constant, t_linear, q_text))

# Print a comparative summary table at the end
print("\n\n--- SUMMARY TABLE ---")
print(f"{'N':>8} | {'O(1) us':>12} | {'O(n) us':>12} | {'O(n^2) us':>15}")
print("-" * 55)
for n, tc, tl, q in results:
    print(f"{n:>8} | {tc:>12.2f} | {tl:>12.2f} | {q:>15}")
