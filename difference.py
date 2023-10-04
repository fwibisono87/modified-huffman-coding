# Computes the number of single-char edits required to transform one string into another. (Levenshtein Distance)
# Sources: https://en.wikipedia.org/wiki/Levenshtein_distance, https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/

def compare_difference(s1, s2):
  """Compares the difference between two strings with the Levenshtein Distance algorithm.

  Args:
      s1 (string): first string
      s2 (string): second string

  Returns:
      integer: number of single edits between strings
  """
  if len(s1) == 0:
      return len(s2)
  if len(s2) == 0:
      return len(s1)
  
  matrix = [[0 for _ in range(len(s1) + 1)] for _ in range(len(s2) + 1)]
  
  for i in range(len(s2) + 1):
      matrix[i][0] = i
  
  for j in range(len(s1) + 1):
      matrix[0][j] = j
  
  for i in range(1, len(s2) + 1):
      for j in range(1, len(s1) + 1):
          if s2[i-1] == s1[j-1]:
              matrix[i][j] = matrix[i-1][j-1]
          else:
              matrix[i][j] = min(
                  matrix[i-1][j-1] + 1,  # Substitution
                  min(
                      matrix[i][j-1] + 1,  # Insertion
                      matrix[i-1][j] + 1   # Deletion
                  )
              )
  
  return matrix[len(s2)][len(s1)]

if __name__ == '__main__':
  s1 = "kyou mo kawaii"
  s2 = "kyou mo kowai"

  print(compare_difference(s1, s2))