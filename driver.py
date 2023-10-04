import huffman
import buildFrequencyTable

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

  print(f"Corrupted Message: {corrupted_msg}")
  print(f"Corrupted Indexes: {corrupted_indexes}")
  print(f"Decoded Corrupted Message: {currentHuffman._decode_message(corrupted_msg)}")