from heapq import heapify, heappop, heappush
import random

from ngrams import get_character_frequencies, get_ngram_frequencies, load_sample_text


class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.frequency < other.frequency
    
    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, Node):
            return False
        return self.frequency == other.frequency

class HuffmanCoding:
    def __init__(self, lut_df):
        self.lut_df = lut_df
        self.root = self.build_huffman_tree()

    def build_huffman_tree(self):
        priority_queue = [Node(symbol, frequency) for symbol, frequency in zip(self.lut_df['symbol'], self.lut_df['frequency'])]
        heapify(priority_queue)
        
        while len(priority_queue) > 1:
            left = heappop(priority_queue)
            right = heappop(priority_queue)
            merged = Node(None, left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            heappush(priority_queue, merged)
        
        return priority_queue[0]

    def generate_huffman_codes(self, node=None, prefix=""):
        if node is None:
            node = self.root
            self.codes = {}
        
        if node.symbol:
            self.codes[node.symbol] = prefix
        else:
            self.generate_huffman_codes(node.left, prefix + "0")
            self.generate_huffman_codes(node.right, prefix + "1")
        return self.codes
    
def train(text):
    lut_df = get_ngram_frequencies(text, 1)
    huffman_coding = HuffmanCoding(lut_df)
    huffman_codes = huffman_coding.generate_huffman_codes()
    return huffman_codes




def encode(input_text, huffman_codes):
    encoded_text = ''
    i = 0
    while i < len(input_text):
        match_found = False
        for size in reversed(range(1, max(map(len, huffman_codes.keys())) + 1)):
            n_gram = input_text[i:i+size]
            if n_gram in huffman_codes:
                encoded_text += huffman_codes[n_gram]
                i += size
                match_found = True
                break
        if not match_found:
            encoded_text += huffman_codes[input_text[i]]
            i += 1
    return encoded_text

def decode(encoded_text, huffman_tree_root):
    decoded_text = ''
    node = huffman_tree_root
    for bit in encoded_text:
        node = node.left if bit == '0' else node.right
        if node.symbol:
            decoded_text += node.symbol
            node = huffman_tree_root 
    return decoded_text

def calculate_compression_ratio(original_text, encoded_text, bits_per_character=8):
    size_of_original = len(original_text) * bits_per_character
    size_of_encoded = len(encoded_text)
    ratio = size_of_original / size_of_encoded if size_of_encoded != 0 else float('inf')
    return ratio if ratio <= 1 else 1 / ratio

def flip_bits(binary_string, flip_percentage):
    num_to_flip = int(len(binary_string) * (flip_percentage / 100))
    positions_to_flip = random.sample(range(len(binary_string)), num_to_flip)
    binary_list = list(binary_string)
    for pos in positions_to_flip:
        binary_list[pos] = '0' if binary_list[pos] == '1' else '1'

    return ''.join(binary_list)

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def normal_huffman(corpus, input_text, verbose=False, errorRate=0):
    huffman_coding = HuffmanCoding(get_character_frequencies(corpus))
    huffman_codes = huffman_coding.generate_huffman_codes()
    input_text = input_text.upper()

    encoded_text = encode(input_text, huffman_codes)
    errored_text = flip_bits(encoded_text, errorRate)
    decoded_text = decode(errored_text, huffman_coding.root)
    compression_ratio = calculate_compression_ratio(input_text, encoded_text)

    result = {
        'encoded_text': encoded_text,
        'decoded_text': decoded_text,
        'compression_ratio': compression_ratio,
        'distance': levenshtein_distance(input_text, decoded_text)
    }
    if verbose:
        result['huffman_codes'] = huffman_codes

    return result


def new_huffman(corpus, input_text, verbose=False, errorRate = 0):
    huffman_coding = HuffmanCoding(get_ngram_frequencies(corpus, 1.0))
    huffman_codes = huffman_coding.generate_huffman_codes()
    input_text = input_text.upper()

    encoded_text = encode(input_text.upper(), huffman_codes)
    errored_text = flip_bits(encoded_text, errorRate)
    decoded_text = decode(errored_text, huffman_coding.root)
    compression_ratio = calculate_compression_ratio(input_text, encoded_text)

    result = {
        'encoded_text': encoded_text,
        'decoded_text': decoded_text,
        'compression_ratio': compression_ratio,
        'distance': levenshtein_distance(input_text, decoded_text)
    }

    if verbose:
        result['huffman_codes'] = huffman_codes

    return result

if __name__ == "__main__":
    text = load_sample_text()
    input_text = """
        Glasses are really versatile. First, you can have glasses-wearing girls take them off and suddenly become beautiful, or have girls wearing glasses flashing those cute grins, or have girls stealing the protagonist's glasses and putting them on like, "Haha, got your glasses!" That's just way too cute! Also, boys with glasses! I really like when their glasses have that suspicious looking gleam, and it's amazing how it can look really cool or just be a joke. I really like how it can fulfill all those abstract needs. Being able to switch up the styles and colors of glasses based on your mood is a lot of fun too! It's actually so much fun! You have those half rim glasses, or the thick frame glasses, everything! It's like you're enjoying all these kinds of glasses at a buffet. I really want Luna to try some on or Marine to try some on to replace her eyepatch. We really need glasses to become a thing in hololive and start selling them for HoloComi. Don't. You. Think. We. Really. Need. To. Officially. Give. Everyone. Glasses?"""

    print("modified:")
    print(new_huffman(text, input_text)["compression_ratio"])
    print("normal:")
    print(normal_huffman(text, input_text)["compression_ratio"])

