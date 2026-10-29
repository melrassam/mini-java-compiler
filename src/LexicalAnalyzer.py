from Token import Token

T = [
  
]

class LexicalAnalyzer:
  def __init__(self, file_path = "data/main.mjava"):
    self.file_path = file_path

  def tokenize(self, output_file_path = None):
    # read source code and handle errors
    source = ""
    try:
      with open(file=self.file_path, mode='r') as file:
        source = file.read()

    except:
      print(f"ERROR: failed to open {self.file_path}")
      return []


    tokens = []
    curr_state = 'q0'


    return tokens

# lexer = LexicalAnalyzer("data/main.mjava")
# lexer.tokenize()