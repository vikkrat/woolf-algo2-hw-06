import requests
import string
import matplotlib.pyplot as plt
from collections import Counter
from multiprocessing import Pool, cpu_count


# --- MAP ---
def mapper(text_chunk):
    words = text_chunk.translate(str.maketrans('', '', string.punctuation)).lower().split()
    return Counter(words)


# --- REDUCE ---
def reducer(mapped_results):
    total = Counter()
    for partial_result in mapped_results:
        total.update(partial_result)
    return total


# --- Візуалізація ---
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# --- Основна логіка ---
def main():
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Тестовий текст: "Pride and Prejudice"
    response = requests.get(url)
    text = response.text

    # Поділ на частини
    chunk_size = len(text) // cpu_count()
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    with Pool() as pool:
        mapped = pool.map(mapper, chunks)

    reduced = reducer(mapped)
    visualize_top_words(reduced)


if __name__ == "__main__":
    main()
