import ollama
import time
import json
import pandas as pd
import os

MODELS = ["llama3", "llama3.2", "deepseek-r1:1.5b"]

def run_inference(model: str, prompt: str) -> dict:
    start_total = time.time()
    first_token_time = None
    full_response = ""
    token_count = 0

    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if first_token_time is None:
            first_token_time = time.time() - start_total
        content = chunk["message"]["content"]
        full_response += content
        token_count += 1

    total_time = time.time() - start_total

    return {
        "model": model,
        "prompt_id": None,
        "category": None,
        "prompt": prompt[:80],
        "response": full_response,
        "time_to_first_token": round(first_token_time, 3),
        "total_latency": round(total_time, 3),
        "tokens_per_sec": round(token_count / total_time, 2),
        "token_count": token_count
    }

def run_full_benchmark(prompts_path="prompts/test_prompts.json"):
    with open(prompts_path) as f:
        prompts = json.load(f)

    results = []
    total = len(MODELS) * len(prompts)
    count = 0

    for model in MODELS:
        print(f"\n{'='*50}")
        print(f"Benchmarking {model}")
        print(f"{'='*50}")
        for item in prompts:
            count += 1
            print(f"[{count}/{total}] {model} — {item['prompt'][:50]}...")
            result = run_inference(model, item["prompt"])
            result["prompt_id"] = item["id"]
            result["category"] = item["category"]
            results.append(result)

    df = pd.DataFrame(results)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/benchmark_results.csv", index=False)
    print("\nSaved to results/benchmark_results.csv")

    print("\n--- Summary ---")
    summary = df.groupby("model")[["time_to_first_token", "total_latency", "tokens_per_sec"]].mean().round(2)
    print(summary)
    return df

if __name__ == "__main__":
    run_full_benchmark()