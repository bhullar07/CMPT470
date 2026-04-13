import parasail
import time
import statistics

file_path = r"C:\BioInformatics\DATA\nanopore\nanopore.txt"

with open(file_path, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

seq1 = lines[0][:500]
seq2 = lines[1][:500]

gap_sizes = [5, 20, 50, 100]
repeat_per_gap = 30

print("base seq1 length:", len(seq1))
print("base seq2 length:", len(seq2))
print()

results = []

for gap in gap_sizes:
    insertion = "T" * gap
    seq2_modified = seq2[:250] + insertion + seq2[250:]

    runtimes = []

    for _ in range(repeat_per_gap):
        start = time.perf_counter()
        result = parasail.sw_trace_striped_16(seq1, seq2_modified, 2, 1, parasail.nuc44)
        end = time.perf_counter()

        runtimes.append(end - start)

    stable = runtimes[1:]

    avg_time = sum(stable) / len(stable)
    median_time = statistics.median(stable)

    results.append((gap, avg_time, median_time))

    print("gap size:", gap)
    print("modified seq2 length:", len(seq2_modified))
    print("score:", result.score)
    print("average runtime:", avg_time)
    print("median runtime:", median_time)
    print("min:", min(stable))
    print("max:", max(stable))
    print()

print("=== summary ===")
for gap, avg, med in results:
    print("gap:", gap, "avg runtime:", avg, "median runtime:", med)