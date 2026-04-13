import parasail
import time

file_path = r"C:\BioInformatics\DATA\illumina\illumina.txt"

pair_count = 1000
times = []
scores = []
lengths1 = []
lengths2 = []

with open(file_path, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

total_pairs = len(lines) // 2

print("total reads:", len(lines))
print("total pairs available:", total_pairs)
print("pairs to test:", pair_count)
print()

if pair_count > total_pairs:
    print("Error: pair_count is larger than available pairs.")
else:
    for i in range(0, pair_count * 2, 2):
        seq1 = lines[i]
        seq2 = lines[i + 1]

        lengths1.append(len(seq1))
        lengths2.append(len(seq2))

        start = time.perf_counter()
        result = parasail.sw_trace_striped_16(seq1, seq2, 2, 1, parasail.nuc44)
        end = time.perf_counter()

        runtime = end - start
        times.append(runtime)
        scores.append(result.score)

        pair_num = (i // 2) + 1

        if pair_num <= 5:
            print("pair", pair_num)
            print("lengths:", len(seq1), len(seq2))
            print("score:", result.score)
            print("time:", runtime)
            print()

    stable_times = times[1:]

    print("finished")
    print("pairs tested:", len(times))
    print("average runtime including first:", sum(times) / len(times))
    print("average runtime excluding first:", sum(stable_times) / len(stable_times))
    print("min runtime excluding first:", min(stable_times))
    print("max runtime excluding first:", max(stable_times))
    print("total runtime:", sum(times))
    print("average score:", sum(scores) / len(scores))
    print("average seq1 length:", sum(lengths1) / len(lengths1))
    print("average seq2 length:", sum(lengths2) / len(lengths2))