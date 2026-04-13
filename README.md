# CMPT470 - Project


1. ## Project Title & Overview
    This project compares the performance of the Adaptive Block Aligner (Rust) against the Parasail library (C/Python). We demonstrate how block-based heuristics significantly reduce the scaling penalty for long-read genomic data.

2. ## Repository Structure
    
    block-aligner/: Rust implementation of the Adaptive Block algorithm.

    parasail/: Python-wrapped C implementation used as a performance baseline.

    data/: Shared directory containing Illumina and Nanopore datasets.

    README.md: Project documentation and execution guide.

3. ## Execution Guide
    How to Run Block Aligner
    Navigate to: cd CMPT470/block-aligner
    Run the Optimized build: cargo run --release --features simd_neon --bin run_align (For MacOS)

    ### **Cross-Platform Compatibility**
    | Architecture | Common Platforms | Rust Feature Flag |
        | :--- | :--- | :--- |
    | **ARM (Neon)** | MacBook M1/M2/M3 | `--features simd_neon` |
    | **Modern x86 (AVX2)** | Recent Intel/AMD (Windows/Linux) | `--features simd_avx2` |
    | **Legacy x86 (SSE2)** | Older PCs / Basic compatibility | `--features simd_sse2` |
    | **WASM SIMD** | Web Browsers | `--features simd_wasm` |

    ### **Running Parasail (Python)**
    1. `cd parasail`
    2. `python3 Nanopore.py`  
    *Note: You may need to update the `file_path` variable at the top of the scripts in the `/parasail` directory to point to your local `/data` folder.*


4. ## Methodology & Data

    Real Data: Performance was measured using real-world Illumina (150 bp) and Nanopore (1,000 bp) reads.

    Controlled Gap Stress Test: To test the Adaptive nature of the algorithm, we inserted artificial gaps (5 bp to 100 bp) into synthetic 500 bp sequences.

5. ## Key Results


    Summary of Findings
    Speed: Block Aligner achieved ~100x speedup over Parasail for short reads.

    Scaling: While Parasail showed a 28x slowdown when moving from short to long reads, Block Aligner only showed an 8x slowdown.

    Efficiency: The algorithm maintained microsecond-level performance even when bridging 100 bp gaps.  
