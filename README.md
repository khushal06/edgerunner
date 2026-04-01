# Edgerunner — Local AI Model Benchmarking Tool

A production-grade benchmarking tool that runs multiple open-source AI models completely offline, measures their performance across 90 inferences, and produces a data-driven report to help teams decide which model to use based on their specific needs.

## The Problem

Most engineers default to GPT-4 or Claude without asking a simple question — do we actually need this? In the real world there are four constraints that make local models the only option:

- **Privacy** — You cannot send sensitive data to an external API. Medical records, financial documents, legal contracts — none of it should leave your network.
- **Latency** — Network roundtrips add unpredictable delays. Local inference is deterministic.
- **Cost** — API costs scale with usage. At production scale, paying per token gets expensive fast.
- **Connectivity** — Edge deployments, air-gapped environments, and offline scenarios have no internet access at all.

Most candidates have zero hands-on experience with these constraints. This project fixes that.

## What I Built

A CLI benchmarking tool that:
1. Runs 3 open-source models completely offline on local hardware
2. Tests each model on 30 standardized prompts across 6 categories
3. Measures time to first token, total latency, and tokens per second for every inference
4. Saves all results to CSV for analysis
5. Produces a summary showing exactly which model wins for which use case

## What Is Actually Happening

When you run this tool, here is what happens step by step:

1. Ollama loads the model into your Mac's memory (no internet needed)
2. Each prompt is sent to the model one at a time
3. The model streams its response token by token
4. The tool measures how long until the first token arrives (time to first token) and how fast tokens are generated (tokens per second)
5. Every result is logged to a CSV file
6. A summary table is printed showing average performance per model

## Benchmark Results

These numbers were recorded on a MacBook Pro running all models locally with no internet connection:

| Model | Time to First Token | Total Latency | Tokens/sec |
|---|---|---|---|
| deepseek-r1:1.5b | 0.21s | 9.83s | 67.29 |
| llama3.2 | 0.27s | 3.49s | 35.65 |
| llama3 | 0.78s | 21.33s | 10.54 |

### What These Numbers Mean

- **llama3.2 wins on total latency** — fastest end-to-end response at 3.49s average. Best for real-time applications where the user is waiting.
- **deepseek-r1:1.5b wins on tokens/sec** — generates 67 tokens per second, 6x faster than llama3. Best for long document generation.
- **llama3 is the quality baseline** — slowest but most thorough responses. Best for complex reasoning tasks where accuracy matters more than speed.

## Project Structure
```
edgerunner/
├── src/
│   ├── benchmark.py       # Core benchmarking engine — runs all inferences, measures latency
│   ├── models.py          # Model configuration and management
│   ├── validator.py       # Pydantic JSON schema validation + retry logic (Phase 2)
│   └── __init__.py
├── prompts/
│   └── test_prompts.json  # 30 standardized prompts across 6 categories
├── results/
│   └── benchmark_results.csv  # Raw benchmark data from all 90 inferences
├── main.py                # CLI entrypoint
├── .gitignore
└── README.md
```

## Prompt Categories

The 30 test prompts cover 6 categories to measure model performance across different task types:

| Category | Count | What It Tests |
|---|---|---|
| Factual | 5 | Basic knowledge retrieval accuracy |
| Reasoning | 5 | Logic, math, deduction |
| Coding | 5 | Python, SQL, algorithms |
| Summarization | 5 | Concise, accurate compression |
| Creative | 5 | Open-ended generation quality |
| Analytical | 5 | Multi-point structured thinking |

## Tech Stack

| Component | Tool |
|---|---|
| Local model runner | Ollama |
| Models benchmarked | llama3, llama3.2, deepseek-r1:1.5b |
| Results storage | CSV via pandas |
| Validation | Pydantic (Phase 2) |
| Language | Python 3.11 |

## Setup

### 1. Install Ollama
Download from https://ollama.com and pull the models:
```bash
ollama pull llama3
ollama pull llama3.2
ollama pull deepseek-r1:1.5b
```

### 2. Clone and set up environment
```bash
git clone https://github.com/saikhushaldulam/edgerunner.git
cd edgerunner
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install ollama pydantic pandas matplotlib tabulate pyyaml
```

### 4. Run the benchmark
```bash
python src/benchmark.py
```

This runs 90 inferences (30 prompts x 3 models) and saves results to results/benchmark_results.csv. Takes approximately 30-40 minutes on a MacBook Pro.

### 5. View results
```bash
cat results/benchmark_results.csv
```

## Why This Matters For Real Engineering

Model selection is a decision every AI team makes regularly. Most teams pick whatever is trending on social media. This project shows how to make that decision with data:

- If you need **real-time responses** — use llama3.2 (3.49s average latency)
- If you need **high throughput document generation** — use deepseek-r1:1.5b (67 tokens/sec)
- If you need **maximum quality** — use llama3 and accept the latency cost
- If you need **zero cost and zero privacy risk** — use any of them locally

That is the kind of thinking that separates engineers from prompt engineers.
