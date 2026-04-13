import parasail
import time

file_path = r"C:\BioInformatics\DATA\nanopore\nanopore.txt"

with open(file_path, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

seq1_full = lines[0]
seq2_full = lines[1]

lengths_to_test = [100, 300, 500, 800]
repeat_per_length = 20

print("full seq1 length:", len(seq1_full))
print("full seq2 length:", len(seq2_full))
print()

results = []

for L in lengths_to_test:
    seq1 = seq1_full[:L]
    seq2 = seq2_full[:L]

    runtimes = []

    for _ in range(repeat_per_length):
        start = time.perf_counter()
        result = parasail.sw_trace_striped_16(seq1, seq2, 2, 1, parasail.nuc44)
        end = time.perf_counter()

        runtimes.append(end - start)

    stable = runtimes[1:]
    avg_time = sum(stable) / len(stable)

    results.append((L, avg_time))

    print("length:", L)
    print("score:", result.score)
    print("average runtime:", avg_time)
    print("min:", min(stable))
    print("max:", max(stable))
    print()

print("=== summary ===")
for L, avg in results:
    print("length:", L, "avg runtime:", avg)