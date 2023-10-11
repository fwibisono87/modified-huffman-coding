from huffmanDriver import headless as huffman_headless
import random
import time

def print_huffman_results_pretty(string, errorlevel):
  difference, corruptedmsg, corruptedIdx= huffman_headless(string, errorlevel)
  print("-----------")
  print(f"Corrupted Message: {corruptedmsg}")
  print("-----------")
  print(f"Difference of encoded vs corrupted encoded message: {difference}")
  print("-----------")
  # print(f"Corrupted Indexes: {corruptedIdx}")
  # print("-----------")

def runErrorsAtRandom(string, repetition):
  string_length = len(string)
  array_of_difference = []
  array_of_error_levels=[]
  for i in range(repetition):
    print(f"Running error {i} out of {repetition}")
    errorLevel = random.randint(0,100)
    array_of_error_levels.append(errorLevel)
    difference, _, _  = huffman_headless(string, errorLevel)
    array_of_difference.append(difference)

  average_dist = sum(array_of_difference)/len(array_of_difference)
  average_error_level = sum(array_of_error_levels)/len(array_of_error_levels)
  print("Average of error levels:")
  print(average_error_level)
  print("Average Levensthein Difference:")
  print(average_error_level)

  correct_chars = string_length - average_dist
  print("Correct chars:")
  print(correct_chars)
  print("Correct chars percentage:")
  print(f"{correct_chars*100/string_length}%")

with open ('./assets/pembukaan_uud_45.txt') as uud45:
  uud45_text = " ".join(line.strip() for line in uud45)  
  print("===========")
  print(uud45_text)
  print("zero errors")
  print_huffman_results_pretty(uud45_text, 0)
  print("10% errors")
  print_huffman_results_pretty(uud45_text, 10)
  print("===========")
  print("random errors")
  start_time = time.time()
  runErrorsAtRandom(uud45_text, 400)
  elapsed_time = time.time() - start_time
  print(f"It took {elapsed_time} seconds to run 400 random errors")