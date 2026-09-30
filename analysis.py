import time
import requests
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------
# 1. MODEL RESPONSE TIME ANALYSIS
# ------------------------------------------------------------
def response_time_analysis():
    queries = ["acne", "dry skin", "oily skin", "sun damage", "sensitive skin"]
    times = []

    for q in queries:
        start = time.time()
        requests.post("http://127.0.0.1:8000/chat", json={"message": q})
        end = time.time()
        times.append(end - start)

    plt.figure(figsize=(8, 5))
    plt.bar(queries, times)
    plt.ylabel("Seconds")
    plt.title("Model Response Time by Query")
    plt.show()


# ------------------------------------------------------------
# 2. KB HIT RATE ANALYSIS (simulated example)
# ------------------------------------------------------------
def kb_hit_analysis():
    categories = ["acne", "oily skin", "dry skin", "sun damage", "others"]
    kb_hits = [32, 20, 15, 10, 18]  # dummy data (replace with logs if needed)

    plt.figure(figsize=(6, 6))
    plt.pie(kb_hits, labels=categories, autopct="%1.1f%%")
    plt.title("KB Usage Distribution")
    plt.show()


# ------------------------------------------------------------
# 3. QUERY TYPE DISTRIBUTION
# ------------------------------------------------------------
def query_distribution():
    types = ["acne", "oily skin", "dry skin", "sensitive skin", "hyperpigmentation"]
    counts = [40, 25, 18, 12, 10]  # dummy data

    plt.figure(figsize=(8, 5))
    plt.bar(types, counts)
    plt.ylabel("Frequency")
    plt.title("Distribution of Skincare Query Types")
    plt.show()


# ------------------------------------------------------------
# 4. OUTPUT LENGTH ANALYSIS
# ------------------------------------------------------------
def output_length_analysis():
    queries = ["acne", "dry skin", "oily skin", "sun damage"]
    lengths = []

    for q in queries:
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": q})
        text = response.json().get("reply", "")
        lengths.append(len(text.split()))

    plt.figure(figsize=(8, 5))
    plt.plot(queries, lengths, marker="o")
    plt.ylabel("Word Count")
    plt.title("Model Output Length per Query")
    plt.grid(True)
    plt.show()


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
if __name__ == "__main__":
    print("Running Response Time Analysis...")
    response_time_analysis()

    print("Running KB Hit Rate Analysis...")
    kb_hit_analysis()

    print("Running Query Distribution Analysis...")
    query_distribution()

    print("Running Output Length Analysis...")
    output_length_analysis()
