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

with open('assets/beemovie.txt', 'r') as f:
  lines = f.readlines()
  corpus = ''.join(lines)

  sum_of_stats = {
    'compression_ratio': {
      'modified': 0,
      'normal': 0
    },
    'distance': {
      'modified': 0,
      'normal': 0
    }
  }

  with open('assets/test_strings.txt', 'r') as test:
    testLines = test.readlines()
    numOfLines = 0

    for i in range(100):
      for line in testLines:
        numOfLines += 1
        this_res = print_huffman_results_pretty(corpus, line, 0)
        sum_of_stats['compression_ratio']['modified'] += this_res['compression_ratio']['modified']
        sum_of_stats['compression_ratio']['normal'] += this_res['compression_ratio']['normal']
        sum_of_stats['distance']['modified'] += this_res['distance']['modified']
        sum_of_stats['distance']['normal'] += this_res['distance']['normal']
    

    no_error_normal_compression_ratio = sum_of_stats['compression_ratio']['normal'] / numOfLines
    no_error_modified_compression_ratio = sum_of_stats['compression_ratio']['modified'] / numOfLines
    no_error_normal_distance = sum_of_stats['distance']['normal'] / numOfLines
    no_error_modified_distance = sum_of_stats['distance']['modified'] / numOfLines

    sum_of_stats = {
      'compression_ratio': {
        'modified': 0,
        'normal': 0
      },
      'distance': {
        'modified': 0,
        'normal': 0
      }
    }
    
    for i in range(100):
      for line in testLines:
        this_res = print_huffman_results_pretty(corpus, line, 1)
        sum_of_stats['compression_ratio']['modified'] += this_res['compression_ratio']['modified']
        sum_of_stats['compression_ratio']['normal'] += this_res['compression_ratio']['normal']
        sum_of_stats['distance']['modified'] += this_res['distance']['modified']
        sum_of_stats['distance']['normal'] += this_res['distance']['normal']


    print("===========")
    print("test compression ratio")
    print("===========")
    print("compression ratio")
    print("modified: " + str(no_error_modified_compression_ratio))
    print("normal: " + str(no_error_normal_compression_ratio))

    print("===========")
    print("test distance")
    print("===========")
    print("distance")
    print("modified: " + str(sum_of_stats['distance']['modified'] / numOfLines))
    print("normal: " + str(sum_of_stats['distance']['normal'] / numOfLines))