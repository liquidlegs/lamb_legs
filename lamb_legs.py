import argparse, json, re

GET_IF_RESULT = r"\S+\s*=\s*'[\S ]+'|\S+\s*=\s*\"[\S ]+\""
GET_STRING = r"'[\S ]+'|\"[\S ]+\""

# Returns the value that is stored in the json key.
def check_json_error(data, key: str) -> str | None:
  try:
    out = data[key]
    return out
  except Exception as e:
    return None

# Reads a file and returns it a string.
def read_file(file_name: str) -> str:
  buffer = ""

  with open(file_name, "r") as f:
    buffer = f.read()

  return buffer

# Used to check if the if statement matches the syntax.
def check_if_expr(pattern: str, statement: str) -> str | None:
  output = None
  chk = re.search(pattern, statement)
  
  if chk != None:
    output = chk.group(0)
    return output
  else:
    print("Error: invalid syntax. Must be assigning a value to a key.")
    return None


# Sets the key of a python dictonary to a partiocular value.
def set_value(data: str, key: str, value: str) -> bool:
  try:
    data[key] = value
    return True
  except Exception as e:
    print(f"Error: {e}")
    return False


# Parses the keys and key values and replaces the content as specified by the user.
def parse_input(args):
  config_path = args.config_file
  template_path = args.template
  output = args.output

  # The config file as a string.
  config_buffer = read_file(config_path)
  data = None

  try:
    # Creates the json object from the config string.
    data = json.loads(config_buffer)
  except Exception as e:
    print(f"Error: {e}")

  # The template file as a string.
  templ_buffer = read_file(template_path)
   
  for key in data:

    # Code block reads through each key in the config file and extracts the value.
    match = "{" + key + "}"
    value = check_json_error(data, key)

    if value[0:2] == "if":
      # Removes the characters "if " from the statement string.
      statement = value[3:]
      expr = None

      if "then" in statement:
        # if 'then' is present, we extract the body of the if statement.
        split_statement = statement.split("then ")

        # Statement stores the if condition while expr stores the result if true.
        statement = split_statement[0]
        expr = split_statement[len(split_statement)-1]
      
      # Stores the name of the key.
      var = ""
      for i in data:
        temp = ""
        
        # Checks if the key exists within the json.
        if i in statement:
          temp = i

          # Checks for an exact match before assinging to var.
          if i == temp:
            var = temp
      
      # Gets the value of the variable and encloses it with quotes.
      var_value = check_json_error(data, var)
      var_value = f"'{var_value}'"

      # Replaces the name of the variable with the actual value and executes the code.
      statement = statement.replace(var, var_value)
      code_string = eval(statement)

      if code_string == True:
        # Seperates the name of the key and the value to assign to the key
        check_key = check_if_expr(GET_IF_RESULT, expr)
        expr_value = check_if_expr(GET_STRING, expr)

        # Modifies the json to assign the value to the key as sepcified in the if statement.
        check_key = check_key.replace(expr_value, "").replace(" ", "").replace("=", "")
        expr_value = expr_value.replace('"', "").replace("'", "")

        set_value(data, check_key, expr_value)

    # Each value is matched with the key/varible in the template and is replace with the value.
    if value != None:
      templ_buffer = templ_buffer.replace(match, value)  

  # Writes the resulting data to a file.
  if output == None:
    print(templ_buffer)
  else:
    size = len(templ_buffer)
    
    with open(output, "w") as f:
      f.write(templ_buffer)
      print(f"Successfully wrote {size} bytes to {output}")


def main():
  parser = argparse.ArgumentParser(description="none")
  parser.add_argument("-c", "--config_file", action="store", help="The file path that holds the keys and key values")
  parser.add_argument("-t", "--template", action="store", help="The file path to the template to modify")
  parser.add_argument("-o", "--output", action="store", help="The file path to the file you want to create")
  args = parser.parse_args()

  if args.config_file != None and args.template != None:
    parse_input(args)
  else:
    print("Error: No config file or template file was specified.")


if __name__ == "__main__":
  main()