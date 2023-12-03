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
    print("Word Error Rate: " + str(modified_huffman_res['wer']))
  print("output from normal huffman: " + normal_huffman_res['decoded_text'])
  print("compression ratio: " + str(normal_huffman_res['compression_ratio']))
  if(errorlevel > 0):
    print("distance from original: " + str(normal_huffman_res['distance']))
    print("Word Error Rate: " + str(normal_huffman_res['wer']))
  

  res = {
    'compression_ratio': {
      'modified': modified_huffman_res['compression_ratio'],
      'normal': normal_huffman_res['compression_ratio']
    },
    'distance': {
      'modified': modified_huffman_res['distance'],
      'normal': normal_huffman_res['distance']
    },
    'wer': {
      'modified': modified_huffman_res['wer'],
      'normal': normal_huffman_res['wer']
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
    total_length = 0

    # Repeat each line num_repetitions times
    args = [(line, corpus, error_mode) for line in testLines for _ in range(num_repetitions)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_line_helper, args)

        for line, this_res in zip(testLines * num_repetitions, results):
            line_length = len(line.strip())  # Strip to remove newline characters, if any
            total_length += line_length

            sum_of_stats['compression_ratio']['modified'] += this_res['compression_ratio']['modified']
            sum_of_stats['compression_ratio']['normal'] += this_res['compression_ratio']['normal']

            # Normalizing the distance by the length of the string
            if line_length > 0:  # Avoid division by zero
                normalized_modified_distance = this_res['distance']['modified'] / line_length
                normalized_normal_distance = this_res['distance']['normal'] / line_length
            else:
                normalized_modified_distance = 0
                normalized_normal_distance = 0

            sum_of_stats['distance']['modified'] += normalized_modified_distance
            sum_of_stats['distance']['normal'] += normalized_normal_distance

    return sum_of_stats, total_length


# Main part of the script
with open('assets/beemovie.txt', 'r') as f:
    lines = f.readlines()
    corpus = ''.join(lines)

with open('assets/test_strings.txt', 'r') as test:
    testLines = test.readlines()

# Process lines without error
stats_no_error, total_length_no_error = process_lines(testLines, corpus, 0, 5)
no_error_normal_compression_ratio = stats_no_error['compression_ratio']['normal'] / len(testLines)
no_error_modified_compression_ratio = stats_no_error['compression_ratio']['modified'] / len(testLines)
no_error_normal_distance = stats_no_error['distance']['normal'] / total_length_no_error
no_error_modified_distance = stats_no_error['distance']['modified'] / total_length_no_error

# Process lines with error
stats_error, total_length_error = process_lines(testLines, corpus, 1, 1000)
error_normal_compression_ratio = stats_error['compression_ratio']['normal'] / len(testLines)
error_modified_compression_ratio = stats_error['compression_ratio']['modified'] / len(testLines)
error_normal_distance = stats_error['distance']['normal'] / total_length_error
error_modified_distance = stats_error['distance']['modified'] / total_length_error



print("===========")
print("examples for 1% error rate")
process_lines(testLines, corpus, 1, 1)

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
print("-----------")
print("Word Error Rate")
print("modified (no error): " + str(stats_error['wer']['modified']))
print("normal (no error): " + str(stats_error['wer']['normal']))
print("modified (error): " + str(stats_error['wer']['modified']))
print("normal (error): " + str(stats_error['wer']['normal']))
