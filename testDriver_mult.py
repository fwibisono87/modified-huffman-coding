from newHuffman import normal_huffman, new_huffman 

def print_huffman_results_pretty(corpus, string, errorlevel):
  modified_huffman_res = new_huffman(corpus, string, errorRate=errorlevel, verbose=True)
  normal_huffman_res = normal_huffman(corpus, string, errorRate=errorlevel, verbose=True)

  print("-----------")
  print("orignal string: " + string)
  print("error level: " + str(errorlevel))
  if(errorlevel == 0):
    print("no errors")
  print("output from modified huffman: " + modified_huffman_res['decoded_text'])
  print("compression ratio: " + str(modified_huffman_res['compression_ratio']))
  if(errorlevel > 0):
    print("distance from original: " + str(modified_huffman_res['distance']))
  print("output from normal huffman: " + normal_huffman_res['decoded_text'])
  print("compression ratio: " + str(normal_huffman_res['compression_ratio']))
  if(errorlevel > 0):
    print("distance from original: " + str(normal_huffman_res['distance']))
  

  res = {
    'compression_ratio': {
      'modified': modified_huffman_res['compression_ratio'],
      'normal': normal_huffman_res['compression_ratio']
    },
    'distance': {
      'modified': modified_huffman_res['distance'],
      'normal': normal_huffman_res['distance']
    }
  }
  return res

import concurrent.futures

def process_line(line, corpus, error_mode):
    # Your existing logic
    this_res = print_huffman_results_pretty(corpus, line, error_mode)
    return this_res

def process_line_helper(args):
    # Unpack arguments
    return process_line(*args)

def process_lines(testLines, corpus, error_mode, num_repetitions):
    sum_of_stats = {
        'compression_ratio': {'modified': 0, 'normal': 0},
        'distance': {'modified': 0, 'normal': 0}
    }

    # Repeat each line num_repetitions times
    args = [(line, corpus, error_mode) for line in testLines for _ in range(num_repetitions)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_line_helper, args)

        for this_res in results:
            sum_of_stats['compression_ratio']['modified'] += this_res['compression_ratio']['modified']
            sum_of_stats['compression_ratio']['normal'] += this_res['compression_ratio']['normal']
            sum_of_stats['distance']['modified'] += this_res['distance']['modified']
            sum_of_stats['distance']['normal'] += this_res['distance']['normal']

    return sum_of_stats

# Main part of the script
with open('assets/beemovie.txt', 'r') as f:
    lines = f.readlines()
    corpus = ''.join(lines)

with open('assets/test_strings.txt', 'r') as test:
    testLines = test.readlines()

# Process lines without error
stats_no_error = process_lines(testLines, corpus, 0, 5)
no_error_normal_compression_ratio = stats_no_error['compression_ratio']['normal'] / len(testLines)
no_error_modified_compression_ratio = stats_no_error['compression_ratio']['modified'] / len(testLines)
no_error_normal_distance = stats_no_error['distance']['normal'] / len(testLines)
no_error_modified_distance = stats_no_error['distance']['modified'] / len(testLines)

# Process lines with error
stats_error = process_lines(testLines, corpus, 1, 1000)
error_normal_compression_ratio = stats_error['compression_ratio']['normal'] / len(testLines)
error_modified_compression_ratio = stats_error['compression_ratio']['modified'] / len(testLines)
error_normal_distance = stats_error['distance']['normal'] / len(testLines)
error_modified_distance = stats_error['distance']['modified'] / len(testLines)

# Print results
print("===========")
print("huffman comparisons")
print("total number of lines: " + str(len(testLines)))
print("===========")
print("test compression ratio")
print("===========")
print("compression ratio")
print("modified (no error): " + str(no_error_modified_compression_ratio))
print("normal (no error): " + str(no_error_normal_compression_ratio))
print("modified (error): " + str(error_modified_compression_ratio))
print("normal (error): " + str(error_normal_compression_ratio))

print("===========")
print("test distance")
print("===========")
print("distance")
print("modified (no error): " + str(no_error_modified_distance))
print("normal (no error): " + str(no_error_normal_distance))
print("modified (error): " + str(error_modified_distance))
print("normal (error): " + str(error_normal_distance))
