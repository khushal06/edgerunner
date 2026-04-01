import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

COLORS = {
    "deepseek-r1:1.5b": "#FF6B6B",
    "llama3": "#4A90D9",
    "llama3.2": "#50C878"
}

def load_results(path="results/benchmark_results.csv"):
    return pd.read_csv(path)

def plot_tokens_per_sec(df):
    summary = df.groupby("model")["tokens_per_sec"].mean().round(2)
    models = summary.index.tolist()
    values = summary.values.tolist()
    colors = [COLORS[m] for m in models]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#0F0F0F")
    ax.set_facecolor("#1A1A1A")

    bars = ax.barh(models, values, color=colors, height=0.5)

    for bar, val in zip(bars, values):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f"{val} tok/s", va="center", fontsize=12,
                fontweight="bold", color="white")

    ax.set_title("Tokens Per Second — Higher is Faster", fontsize=14,
                 fontweight="bold", color="white", pad=15)
    ax.set_xlabel("Tokens / Second", color="#AAAAAA")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#333333")
    ax.xaxis.label.set_color("#AAAAAA")
    for label in ax.get_yticklabels():
        label.set_color("white")
        label.set_fontsize(11)

    plt.tight_layout()
    plt.savefig("results/tokens_per_sec.png", dpi=150, facecolor="#0F0F0F")
    print("Saved tokens_per_sec.png")
    plt.close()

def plot_latency(df):
    summary = df.groupby("model")["total_latency"].mean().round(2)
    models = summary.index.tolist()
    values = summary.values.tolist()
    colors = [COLORS[m] for m in models]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#0F0F0F")
    ax.set_facecolor("#1A1A1A")

    bars = ax.barh(models, values, color=colors, height=0.5)

    for bar, val in zip(bars, values):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                f"{val}s", va="center", fontsize=12,
                fontweight="bold", color="white")

    ax.set_title("Total Latency — Lower is Better", fontsize=14,
                 fontweight="bold", color="white", pad=15)
    ax.set_xlabel("Seconds", color="#AAAAAA")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#333333")
    ax.xaxis.label.set_color("#AAAAAA")
    for label in ax.get_yticklabels():
        label.set_color("white")
        label.set_fontsize(11)

    plt.tight_layout()
    plt.savefig("results/latency.png", dpi=150, facecolor="#0F0F0F")
    print("Saved latency.png")
    plt.close()

def plot_latency_by_category(df):
    pivot = df.groupby(["category", "model"])["total_latency"].mean().round(2).unstack()
    categories = pivot.index.tolist()
    models = pivot.columns.tolist()
    x = np.arange(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("#0F0F0F")
    ax.set_facecolor("#1A1A1A")

    for i, model in enumerate(models):
        bars = ax.bar(x + i * width, pivot[model], width,
                      label=model, color=COLORS[model], alpha=0.9)

    ax.set_title("Latency by Category — Lower is Better", fontsize=14,
                 fontweight="bold", color="white", pad=15)
    ax.set_ylabel("Seconds", color="#AAAAAA")
    ax.set_xticks(x + width)
    ax.set_xticklabels(categories, color="white", fontsize=10)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#333333")
    ax.yaxis.label.set_color("#AAAAAA")

    legend = ax.legend(facecolor="#2A2A2A", labelcolor="white",
                       fontsize=10, title="Model",
                       title_fontsize=10)
    legend.get_title().set_color("white")

    plt.tight_layout()
    plt.savefig("results/latency_by_category.png", dpi=150, facecolor="#0F0F0F")
    print("Saved latency_by_category.png")
    plt.close()

def plot_first_token(df):
    summary = df.groupby("model")["time_to_first_token"].mean().round(3)
    models = summary.index.tolist()
    values = summary.values.tolist()
    colors = [COLORS[m] for m in models]

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#0F0F0F")
    ax.set_facecolor("#1A1A1A")

    bars = ax.barh(models, values, color=colors, height=0.5)

    for bar, val in zip(bars, values):
        ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                f"{val}s", va="center", fontsize=12,
                fontweight="bold", color="white")

    ax.set_title("Time to First Token — Lower is Better", fontsize=14,
                 fontweight="bold", color="white", pad=15)
    ax.set_xlabel("Seconds", color="#AAAAAA")
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#333333")
    ax.xaxis.label.set_color("#AAAAAA")
    for label in ax.get_yticklabels():
        label.set_color("white")
        label.set_fontsize(11)

    plt.tight_layout()
    plt.savefig("results/first_token.png", dpi=150, facecolor="#0F0F0F")
    print("Saved first_token.png")
    plt.close()

def print_report(df):
    print("\n" + "="*60)
    print("EDGERUNNER — MODEL COMPARISON REPORT")
    print("="*60)

    summary = df.groupby("model")[["time_to_first_token", "total_latency", "tokens_per_sec"]].mean().round(2)
    print("\n--- Overall Performance ---")
    print(summary.to_string())

    print("\n--- Latency by Category ---")
    cat = df.groupby(["model", "category"])["total_latency"].mean().round(2).unstack()
    print(cat.to_string())

    print("\n--- Winners ---")
    print(f"Fastest total response:  {summary['total_latency'].idxmin()}")
    print(f"Most tokens per second:  {summary['tokens_per_sec'].idxmax()}")
    print(f"Fastest first token:     {summary['time_to_first_token'].idxmin()}")
    print("="*60)

if __name__ == "__main__":
    df = load_results()
    print_report(df)
    plot_tokens_per_sec(df)
    plot_latency(df)
    plot_latency_by_category(df)
    plot_first_token(df)
    print("\nAll charts saved to results/")