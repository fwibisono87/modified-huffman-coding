from heapq import heapify, heappop, heappush

from ngrams import get_ngram_frequencies, load_sample_text


class Node:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        
    # Define comparators for the priority queue
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
        # Create nodes for each symbol and add them to a priority queue
        priority_queue = [Node(symbol, frequency) for symbol, frequency in zip(self.lut_df['symbol'], self.lut_df['frequency'])]
        heapify(priority_queue)
        
        # Build the tree until the priority queue has just one node left
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
    lut_df = get_ngram_frequencies(text, 1.0)
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


def new_huffman(corpus, input_text, verbose=False):
    huffman_coding = HuffmanCoding(get_ngram_frequencies(corpus, 1.0))
    huffman_codes = huffman_coding.generate_huffman_codes()

    encoded_text = encode(input_text.upper(), huffman_codes)
    decoded_text = decode(encoded_text, huffman_coding.root)
    compression_ratio = calculate_compression_ratio(input_text, encoded_text)

    result = {
        'encoded_text': encoded_text,
        'decoded_text': decoded_text,
        'compression_ratio': compression_ratio
    }

    if verbose:
        result['huffman_codes'] = huffman_codes

    return result

if __name__ == "__main__":
    text = load_sample_text()
    input_text = "Keep your hands and antennas inside the tram at all times."

    print(new_huffman(text, input_text))

