from heapq import heapify, heappop
import pandas as pd
from collections import Counter
import re

def calculate_ngram_frequencies(text, n):
    """
    Calculate the frequencies of n-grams in the given text.

    :param text: Input text string
    :param n: Size of the n-gram (1 for unigram, 2 for bigram, 3 for trigram)
    :return: A list of dictionaries containing 'symbol', 'frequency', and 'percentage'
    """
    from collections import Counter
    import re

    # clean_text = re.sub(r'[^A-Za-z]+', '', text).upper()
    clean_text = text.upper()
    ngrams = [clean_text[i:i+n] for i in range(len(clean_text)-n+1)]
    frequency = Counter(ngrams)
    total_ngrams = sum(frequency.values())

    sorted_ngrams = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    ngram_data = [
        {'symbol': ngram[0], 'frequency': ngram[1], 'percentage': round((ngram[1] / total_ngrams) * 100, 2)}
        for ngram in sorted_ngrams
    ]

    return ngram_data

def ngram_frequencies(text):
    return calculate_ngram_frequencies(text, 1), calculate_ngram_frequencies(text, 2), calculate_ngram_frequencies(text, 3)

def character_frequencies(text):
    return calculate_ngram_frequencies(text, 1)

def get_character_frequencies(text):
    return pd.DataFrame(character_frequencies(text))

def get_ngram_frequencies(text, threshold=1.0):
    unigrams, bigrams, trigrams = ngram_frequencies(text)

    df_unigrams = pd.DataFrame(unigrams)
    df_bigrams = pd.DataFrame(bigrams)
    df_trigrams = pd.DataFrame(trigrams)

    bigrams_filtered = df_bigrams[df_bigrams['percentage'] >= threshold]
    trigrams_filtered = df_trigrams[df_trigrams['percentage'] >= threshold]

    lut_df = pd.concat([df_unigrams, bigrams_filtered, trigrams_filtered])

    return lut_df


def print_table(df, title):
    print(title)
    print(df.to_string(index=False))

def load_sample_text():
    with open('assets/beemovie.txt', 'r') as f:
        lines = f.readlines()
        return ''.join(lines)

def ngram(text):
    lut_df = get_ngram_frequencies(text)
    lut_df_sorted = lut_df.sort_values(by=['percentage'], ascending=False)
    print_table(lut_df_sorted, "N-Gram Frequencies")

def unigram(text):
    unigrams = calculate_ngram_frequencies(text, 1)
    df_unigrams = pd.DataFrame(unigrams)
    df_unigrams_sorted = df_unigrams.sort_values(by=['percentage'], ascending=False)
    print_table(df_unigrams_sorted, "Unigram Frequencies")


if __name__ == '__main__':
    text = load_sample_text()
    ngram(text)
    unigram(text)