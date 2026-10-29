def lexical_analysis(file_path: str, output_file_path: str | None = None):
  """Reads the source code file and generates tokens. It \
  returns a list of dictionaries representing tokens. It \
  can also save tokens to a specified file.

  Args:
    file_path: The source code file path
    output_file_path: Where the tokens are to be saved. \
    If not specified, tokens are not saved on disk.

  Returns:
    A list of tokens represented in dictionaries
  """

  