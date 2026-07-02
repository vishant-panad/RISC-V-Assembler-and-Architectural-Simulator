from Encoding import R_encoding
from Encoding import I_encoding
from Encoding import S_encoding
from Encoding import B_encoding
from Encoding import J_encoding

def lines_strip(line):
  return line.strip().split()

def check_instruction(tokens):
  operation = tokens[0]
  if operation in R_encoding.R_operations or operation in I_encoding.I_operations or operation in S_encoding.S_operations or operation in B_encoding.B_operations or operation in J_encoding.J_operations:
    return True
  else:
    return False
    
def check_lines(tokens, line_no):
  if len(tokens) == 0:
    return "Empty line", line_no
  if len(tokens) == 1:
    return "Incomplete instruction", line_no
  if not check_instruction(tokens):
    return f"Invalid instruction '{tokens[0]}'", line_no
  if len(tokens)<2:
    return f"Incomplete operands for '{tokens[0]}'", line_no
  return None, None

def main3(lines):
  l = []
  for j in lines:
   if ":" in j:
    line_split = j.split(":")[1]
    l.append(line_split)
   if ":" not in j:
    l.append(j)
  # Check for errors and output error 
  error_found = False
  for i, line in enumerate(l, 1):
    tokens = lines_strip(line)
    error, error_line = check_lines(tokens, i)
    if error:
      print(f"Error: {error} at line {error_line}")
      error_found = True
      continue
  if not error_found:
    print("No errors found.")

