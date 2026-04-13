use block_aligner::scan_block::*;
use block_aligner::scores::*;
use std::time::{Instant, Duration};
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {

    // Configuration for the adaptive block algorithm
    let min_size = 32;
    let max_size = 1024; 
    let gaps_config = Gaps { open: -5, extend: -1 };

    // 1. ILLUMINA
    let ill_path = "../data/real.illumina.b10M.txt";
    let ill_file = File::open(ill_path).expect("Illumina file missing!");
    let mut ill_lines = BufReader::new(ill_file).lines().map(|l| l.unwrap()).filter(|l| !l.is_empty());
    
    let mut ill_times = Vec::new();
    for _ in 0..1000 {
        if let (Some(s1), Some(s2)) = (ill_lines.next(), ill_lines.next()) {
            // Prepare sequences with padding for SIMD processing
            let q = PaddedBytes::from_bytes::<NucMatrix>(s1.as_bytes(), max_size);
            let r = PaddedBytes::from_bytes::<NucMatrix>(s2.as_bytes(), max_size);

            // Initialize the adaptive block
            let mut a = Block::<false, false>::new(q.len(), r.len(), max_size);
            // Measure alignment time
            let start = Instant::now();
            a.align(&q, &r, &NW1, gaps_config, min_size..=max_size, 0);
            ill_times.push(start.elapsed());
        }
    }
    // Calculate average excluding the first run (warm-up) to get stable metrics
    println!("Illumina Avg (1000 pairs): {:.8}s", ill_times[1..].iter().sum::<Duration>().as_secs_f64() / 999.0);

    // 2. NANOPORE 
    let ont_path = "../data/real.ont.b10M.txt";
    let ont_file = File::open(ont_path).expect("Nanopore file missing!");
    let mut ont_lines = BufReader::new(ont_file).lines().map(|l| l.unwrap()).filter(|l| !l.is_empty());
    
    let mut ont_times = Vec::new();
    for _ in 0..1000 {
        if let (Some(s1), Some(s2)) = (ont_lines.next(), ont_lines.next()) {
            let q = PaddedBytes::from_bytes::<NucMatrix>(s1.as_bytes(), max_size);
            let r = PaddedBytes::from_bytes::<NucMatrix>(s2.as_bytes(), max_size);
            let mut a = Block::<false, false>::new(q.len(), r.len(), max_size);
            let start = Instant::now();
            a.align(&q, &r, &NW1, gaps_config, min_size..=max_size, 0);
            ont_times.push(start.elapsed());
        }
    }
    println!("Nanopore Avg (1000 pairs): {:.8}s", ont_times[1..].iter().sum::<Duration>().as_secs_f64() / 999.0);

    // 3. CONTROLLED GAP EXPERIMENT

    // Tests how the adaptive block grows or shifts to bridge artificial gaps of varying sizes
    println!("\nControlled Gap Experiment:");
    let s1_base = b"ACGT".repeat(125); // 500bp
    let s2_base = b"ACGT".repeat(125);

    // Test gap sizes: 5, 20, 50, and 100 base pairs
    for &gap in &[5, 20, 50, 100] {

        // Create an artificial insertion gap in the middle of the second sequence
        let mut s2_mod = s2_base[..250].to_vec();
        s2_mod.extend(vec![b'T'; gap]); 
        s2_mod.extend(&s2_base[250..]);
        let q = PaddedBytes::from_bytes::<NucMatrix>(&s1_base, max_size);
        let r = PaddedBytes::from_bytes::<NucMatrix>(&s2_mod, max_size);
        let mut a = Block::<false, false>::new(q.len(), r.len(), max_size);
        let mut gap_times = Vec::new();

        // Repeat 30 times per gap size to ensure statistical accuracy
        for _ in 0..30 {
            let start = Instant::now();
            a.align(&q, &r, &NW1, gaps_config, min_size..=max_size, 0);
            gap_times.push(start.elapsed());
        }
        // Output result for each gap size
        println!("Gap: {} | Avg: {:.8}s", gap, gap_times[1..].iter().sum::<Duration>().as_secs_f64() / 29.0);
    }
}