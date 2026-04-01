import ollama
import json
import time
from pydantic import BaseModel, ValidationError
from typing import Optional

class StructuredResponse(BaseModel):
    answer: str
    confidence: str
    reasoning: str
    category: str

def query_with_schema(model: str, prompt: str, temperature: float = 0.0) -> dict:
    system_prompt = """You are a precise assistant. You must ALWAYS respond with valid JSON only.
No explanation, no markdown, no code blocks. Just raw JSON.
Your response must follow this exact schema:
{
  "answer": "your direct answer here",
  "confidence": "high, medium, or low",
  "reasoning": "one sentence explaining your answer",
  "category": "factual, reasoning, coding, summarization, creative, or analytical"
}"""

    start = time.time()
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        options={"temperature": temperature}
    )
    latency = round(time.time() - start, 3)
    raw = response["message"]["content"].strip()

    # Clean markdown if model wraps in code blocks
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return raw, latency

def validate_with_retry(model: str, prompt: str, temperature: float = 0.0) -> dict:
    for attempt in range(2):
        raw, latency = query_with_schema(model, prompt, temperature)
        try:
            parsed = json.loads(raw)
            validated = StructuredResponse(**parsed)
            return {
                "status": "success",
                "attempt": attempt + 1,
                "model": model,
                "temperature": temperature,
                "latency": latency,
                "data": validated.dict()
            }
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == 0:
                print(f"Attempt 1 failed for {model} — retrying...")
                continue
            return {
                "status": "failed",
                "attempt": 2,
                "model": model,
                "temperature": temperature,
                "latency": latency,
                "error": str(e),
                "raw": raw
            }

if __name__ == "__main__":
    models = ["llama3", "llama3.2", "deepseek-r1:1.5b"]
    prompt = "What is the capital of France?"

    print("\n=== Temperature 0.0 (deterministic) ===")
    for model in models:
        print(f"\nTesting {model}...")
        result = validate_with_retry(model, prompt, temperature=0.0)
        print(f"Status: {result['status']}")
        print(f"Attempts: {result['attempt']}")
        print(f"Latency: {result['latency']}s")
        if result['status'] == 'success':
            print(f"Answer: {result['data']['answer']}")
            print(f"Confidence: {result['data']['confidence']}")
            print(f"Reasoning: {result['data']['reasoning']}")

    print("\n=== Temperature 0.7 (creative) ===")
    for model in models:
        print(f"\nTesting {model}...")
        result = validate_with_retry(model, prompt, temperature=0.7)
        print(f"Status: {result['status']}")
        print(f"Attempts: {result['attempt']}")
        print(f"Latency: {result['latency']}s")
        if result['status'] == 'success':
            print(f"Answer: {result['data']['answer']}")
            print(f"Confidence: {result['data']['confidence']}")
            print(f"Reasoning: {result['data']['reasoning']}")