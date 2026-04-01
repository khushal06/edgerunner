# Edgerunner — Local AI Benchmarking Tool

I built a tool that tests 3 AI models on my laptop with no internet, no API keys, and zero cost. It runs 90 questions across all 3 models, measures how fast and reliable each one is, and tells you which one to use depending on what you actually need.

## The Problem

Everyone just uses ChatGPT or Claude without asking if they need to. But there are real situations where you cannot:

- A hospital cannot send patient records to OpenAI
- A bank cannot send financial data to an external server
- A remote app with no internet cannot call any API
- A startup cannot afford $500/month in API costs at scale

I wanted to actually understand these constraints hands-on instead of just reading about them.

## What I Did

I downloaded 3 AI models once. After that everything ran 100% offline on my MacBook.

I tested all 3 models on the same 30 questions covering 6 topics — facts, reasoning, coding, summarization, creative writing, and analysis. That's 90 total tests.

For each test I measured:
- How long until the first word showed up
- How long the full answer took
- How many words it generated per second

Then in Phase 2 I made each model respond in strict JSON format, validated it with code, and built an automatic retry if the output was broken.

## Results

| Model | First Word | Full Answer | Speed |
|---|---|---|---|
| deepseek-r1:1.5b | 0.21s | 9.83s | 67 tokens/sec |
| llama3.2 | 0.27s | 3.49s | 35 tokens/sec |
| llama3 | 0.78s | 21.33s | 10 tokens/sec |

**llama3.2** — fastest full response, best for real-time use

**deepseek** — fastest raw generation, best for bulk tasks

**llama3** — slowest but most detailed answers, best when quality matters most

## JSON Reliability Test

I also forced each model to respond in structured JSON and tested how reliable they were:

| Model | Strict Mode (temp 0) | Relaxed Mode (temp 0.7) |
|---|---|---|
| llama3 | passed first try | passed first try |
| llama3.2 | passed first try | needed 1 retry |
| deepseek | failed completely | needed 1 retry |

If your app needs structured data outputs — use llama3 or llama3.2. Deepseek is fast but unreliable for JSON.

## How To Run It

### 1. Download Ollama and pull the models
Go to https://ollama.com and install it. Then:
```bash
ollama pull llama3
ollama pull llama3.2
ollama pull deepseek-r1:1.5b
```
You only do this once. No internet needed after this.

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
Takes 30-40 minutes. It's running 90 tests back to back on your CPU.

### 4. Run the JSON validation test
```bash
python src/validator.py
```

### 5. See the results
```bash
cat results/benchmark_results.csv
```

## What I Learned

llama3.2 surprised me the most. I assumed the bigger model would always win but llama3.2 was 6x faster with answers that were just as good for most questions. Size does not equal quality.

Deepseek was fast but messy. Great at generating text quickly but bad at following strict formatting rules. You would not use it in a system that needs clean structured outputs.

Temperature matters. At 0.7 even llama3.2 needed a retry to produce valid JSON. At 0.0 it passed every time. In any production system that needs consistent outputs always use temperature 0.

## Project Status

- [x] Phase 1 — benchmark 3 models across 90 inferences
- [x] Phase 2 — JSON validation, retry logic, temperature testing
- [ ] Phase 3 — charts and full technical report

## Files
```
edgerunner/
├── src/
│   ├── benchmark.py    # runs all the tests and measures speed
│   ├── validator.py    # forces JSON output and validates it
│   └── __init__.py
├── prompts/
│   └── test_prompts.json   # the 30 questions used for testing
├── results/
│   └── benchmark_results.csv   # all 90 results saved here
└── README.md
```
