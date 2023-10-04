import heapq


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_tree_size(node):
    """Calculates the size of a tree recursively.

    Args:
        node (Node): the root node of the tree

    Returns:
        integer: the size of this node and it's children
    """
    if not node:
        return 0

    size = 8  # char
    size += 32  # freq
    size += 64  # left pointer
    size += 64  # right pointer

    size += calculate_tree_size(node.left)
    size += calculate_tree_size(node.right)

    return size

class Huffman:
    """The class to simulate Huffman Coding
    """
    def __init__(self, data):
        """Initialization function

        Args:
            data (dictionary): key:value dictionary of chars and frequency
        """
        self.root = self._build_huffman_tree(data)
        self.mapping = self._create_mapping(self.root)
        self.message = ""
        self.encoded_message = ""

    def _build_huffman_tree(self, data):
        priority_queue = [Node(char, freq) for char, freq in data.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)

            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(priority_queue, merged)

        return priority_queue[0]

    def _create_mapping(self, root, path='', mapping=None):
        if mapping is None:
            mapping = {}

        if root is None:
            return

        if root.char is not None:
            mapping[root.char] = path

        self._create_mapping(root.left, path + '0', mapping)
        self._create_mapping(root.right, path + '1', mapping)

        return mapping

    def setMessage(self, message):
        """Sets the message

        Args:
            message (String): message
        """
        self.message = message
        self.encoded_message = self._encode_message(self.message)

    def getMessage(self):
        return self._decode_message(self.encoded_message)

    def _encode_message(self, message):
        return ''.join(self.mapping[char] for char in message)

    def _decode_message(self, encoded_message):
        decoded_message = ''
        node = self.root
        for bit in encoded_message:
            node = node.left if bit == '0' else node.right

            if node.char is not None:
                decoded_message += node.char
                node = self.root

        return decoded_message

    def printTree(self):
        self._print_tree(self.root)

    def _print_tree(self, root, indent=0):
        if not root:
            return

        print('  ' * indent + f"{root.char if root.char else '*'} ({root.freq})")
        self._print_tree(root.left, indent + 1)
        self._print_tree(root.right, indent + 1)

    def get_sizes_and_compression_rate(self):
        original_message_size = len(self.message) * 8  # in bits
        encoded_message_size = len(self.encoded_message)  # in bits
        tree_size = calculate_tree_size(self.root)  # in bits
        
        message_with_tree = encoded_message_size + tree_size

        if original_message_size == 0:  # To avoid division by zero
            compression_rate = 0
        else:
            compression_rate = (1 - (encoded_message_size / original_message_size)) * 100
        
        return original_message_size, encoded_message_size, message_with_tree, compression_rate, tree_size


def test_bit_flip(binary_message, corruption_level, seed="None"):
    """Simulates bit flips based on corruption level on a binary string.

    Args:
        binary_message (string): Binary string to be "corrupted"
        corruption_level (integer): Level of corruption [0-100]
        seed (str, optional): String for the RNG. Defaults to "None".

    Returns:
        string: the corrupted message
        list: the indexes that got corrupted
    """
    import random
    if seed is not None:
        random.seed(seed)

    binary_len = len(binary_message)
    corrupted_chars = int(binary_len * corruption_level / 100)
    corrupted_indexes = random.sample(range(binary_len), corrupted_chars)

    corrupted_message = list(binary_message)
    for index in corrupted_indexes:
        corrupted_message[index] = '1' if corrupted_message[index] == '0' else '0'
    
    return ''.join(corrupted_message), corrupted_indexes

def correct_percentage(original, decoded):
    """Temporary function to calculate the percentage of correctness between two strings. Will be superseeded with Levenshtein Distance.        

    Args:
        original (string): original message
        decoded (string): decoded message

    Returns:
        integer: percentage of similarity
    """
    if len(original) != len(decoded):
        return 0.0

    correct_count = sum(o == d for o, d in zip(original, decoded))
    return (correct_count / len(original)) * 100


# Usage example
if __name__ == "__main__":
    data = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
    huffman = Huffman(data)

    print("Huffman Tree:")
    huffman.printTree()

    original_message = "abccba"
    huffman.setMessage(original_message)
    print(f"Original Message: {original_message}")
    print(f"Encoded Message: {huffman.encoded_message}")

    decoded_message = huffman.getMessage()
    print(f"Decoded Message: {decoded_message}")

    original_size, encoded_size, message_with_tree, compression_rate, tree_size = huffman.get_sizes_and_compression_rate()
    print(f"\nOriginal Message Size: {original_size} bits")
    print(f"Encoded Message Size: {encoded_size} bits")
    print(f"Tree Size: {tree_size} bits")
    print(f"Message with Tree Size: {message_with_tree} bits")
    print(f"Compression Rate: {compression_rate:.2f}%")

    print("error handling/resiliency testing")
    error_level = 88
    print(f"Error Level: {error_level}%")
    corrupted_message, corrupted_indexes = test_bit_flip(huffman.encoded_message, error_level)
    print(f"Corrupted Message: {corrupted_message}")
    corrupted_decoded_message = huffman._decode_message(corrupted_message)
    print(f"Decoded Corrupted Message: {corrupted_decoded_message}")
    correct_percentage = correct_percentage(original_message, corrupted_decoded_message)
    print(f"We now have a {correct_percentage}% correctness rate")