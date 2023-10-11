import huffman
import buildFrequencyTable
from difference import compare_difference

def headless(message, errorLevel):
  currentFreqTable = buildFrequencyTable.buildFrequencyTable(message)
  currentHuffman = huffman.Huffman(currentFreqTable)
  currentHuffman.setMessage(message)

  corrupted_msg, corrupted_indexes = huffman.test_bit_flip(currentHuffman.encoded_message, errorLevel)
  corrupted_decoded_message = currentHuffman.decode_message(corrupted_msg)

  return compare_difference(currentHuffman.getMessage(), corrupted_decoded_message), corrupted_decoded_message, corrupted_indexes

if __name__ == '__main__':
  print("welcome to huffman coder")
  while True:
    print("Enter message")
    msg = input("> ")
    currentFreqTable = buildFrequencyTable.buildFrequencyTable(msg)
    currentHuffman = huffman.Huffman(currentFreqTable)
    currentHuffman.setMessage(msg)
    print("Encoded message: " + currentHuffman.encoded_message)

    print("Set an error level (0-100)")
    errorLevel = int(input("> "))

    corrupted_msg, corrupted_indexes = huffman.test_bit_flip(currentHuffman.encoded_message, errorLevel)
    corrupted_decoded_message = currentHuffman.decode_message(corrupted_msg)

    print(f"Corrupted Message: {corrupted_msg}")
    print(f"Corrupted Indexes: {corrupted_indexes}")
    print(f"Difference of encoded vs corrupted encoded message: {compare_difference(currentHuffman.encoded_message, corrupted_msg)}")
    

    print(f"Decoded Corrupted Message: {currentHuffman.decode_message(corrupted_msg)}")
    print(f"Difference of original vs corrupted decoded message: {compare_difference(currentHuffman.getMessage(), corrupted_decoded_message)}")
