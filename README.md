# Edgerunner — Local AI Benchmarking Tool

I got tired of everyone just defaulting to GPT-4 without asking if they actually need it. So I built a tool that runs 3 AI models completely offline on my laptop, tests them on the same 30 questions, and tells you with real numbers which one to use and when.

No API keys. No cloud. No cost. Just models running on my machine.

## Why I Built This

There are situations where you literally cannot use ChatGPT or Claude:

- A hospital cannot send patient data to OpenAI
- A bank cannot send financial records to an external server
- An app deployed in a remote area has no internet connection
- A startup paying $500/month in API costs needs a cheaper option

Most people in AI have never dealt with any of these constraints hands-on. I wanted to actually understand them, not just read about them.

## What I Did

I pulled 3 open-source models once using Ollama. After that everything ran completely offline — no internet needed, no data left my machine.

I benchmarked all 3 models across 90 total inferences — 30 prompts each, covering factual questions, reasoning, coding, summarization, creative writing, and analytical thinking.

For every single inference I measured:
- How long until the first word appeared (time to first token)
- How long the full response took (total latency)
- How fast the model was generating (tokens per second)

Then I saved everything to a CSV and analyzed the results.

## The Results

Models were downloaded once — all inference ran fully offline after that:

| Model | First Word | Full Response | Speed |
|---|---|---|---|
| deepseek-r1:1.5b | 0.21s | 9.83s | 67 tokens/sec |
| llama3.2 | 0.27s | 3.49s | 35 tokens/sec |
| llama3 | 0.78s | 21.33s | 10 tokens/sec |

### What this actually means

**Use llama3.2 if** you need fast responses and the user is waiting. 3.49 seconds average. Solid quality. Best all-rounder.

**Use deepseek-r1:1.5b if** you need to generate a lot of text fast. 67 tokens per second is insane for a model this small. Great for batch jobs.

**Use llama3 if** quality is everything and speed doesn't matter. Slowest by far but most thorough answers.

**Use any of them if** you care about privacy, cost, or offline access. They all run 100% locally after the initial download.

## Project Structure
```
edgerunner/
├── src/
│   ├── benchmark.py       # runs all inferences, measures every timing metric
│   └── __init__.py
├── prompts/
│   └── test_prompts.json  # 30 prompts across 6 categories
├── results/
│   └── benchmark_results.csv  # all 90 inference results
├── main.py
└── README.md
```

## Prompt Categories

| Category | Count | What It Tests |
|---|---|---|
| Factual | 5 | Basic knowledge retrieval accuracy |
| Reasoning | 5 | Logic, math, deduction |
| Coding | 5 | Python, SQL, algorithms |
| Summarization | 5 | Concise, accurate compression |
| Creative | 5 | Open-ended generation quality |
| Analytical | 5 | Multi-point structured thinking |

## How To Run It Yourself

### 1. Get Ollama and pull the models
Download from https://ollama.com then run once:
```bash
ollama pull llama3
ollama pull llama3.2
ollama pull deepseek-r1:1.5b
```
After this step you never need internet again.

### 2. Clone and set up
```bash
git clone https://github.com/saikhushaldulam/edgerunner.git
cd edgerunner
python -m venv .venv
source .venv/bin/activate
pip install ollama pydantic pandas matplotlib tabulate pyyaml
```

### 3. Run the benchmark
```bash
python src/benchmark.py
```
Takes around 30-40 minutes — runs 90 inferences back to back on your CPU. Grab a coffee.

### 4. See your results
```bash
cat results/benchmark_results.csv
```

## What I Learned

The biggest surprise was llama3.2. I expected llama3 to dominate everything since it is the bigger model. But llama3.2 was 6x faster on total latency with responses that were honestly just as good for most tasks. For anything real-time, llama3 is just not worth the wait.

Deepseek was the wild card — insanely fast token generation but weird response patterns on some prompts. Great for throughput, not always great for quality.

The takeaway: bigger does not always mean better. It depends entirely on what you are actually trying to do.

## Tech Stack

| Component | Tool |
|---|---|
| Local model runner | Ollama |
| Models | llama3, llama3.2, deepseek-r1:1.5b |
| Language | Python 3.11 |
| Results storage | pandas + CSV |
