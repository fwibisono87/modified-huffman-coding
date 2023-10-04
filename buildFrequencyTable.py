def buildFrequencyTable(input): 
  """Builds a frequency table for the given input string.

  Args:
      input (string): input string

  Returns:
      dict: key/value dictionary containing characters and their frequencies
  """
  masterDict = {}

  for char in input :
    if char in masterDict :
      masterDict[char] += 1
    else :
      masterDict[char] = 1

  return masterDict

if __name__ == '__main__':
  print(buildFrequencyTable('kyou mo kawaii'))