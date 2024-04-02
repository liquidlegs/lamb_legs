import argparse, json, re
from platform import system
from pathlib import Path

GET_VARS = r"{\S+}"

# Returns the value that is stored in the json key.
def check_json_error(data, key: str) -> str | None:
  try:
    out = data[key]
    return out
  except Exception as e:
    return None

# Reads a file and returns it a string.
def read_file(file_name: str) -> str | None:
  buffer = ""

  if file_name == None:
    return

  path = Path(file_name)
  if path.exists() == False:
    print(f"Error: path not found - {file_name}")
    return None

  with open(file_name, "r") as f:
    buffer = f.read()

  return buffer


# Finds all variables/keys in the template file and creates a config file from it. 
def search_template_variables(args, display_data=False):

  # Reads the template file into a string and parses it for the variables.
  templ_buffer = read_file(args.parse_template)
  find_vars = re.findall(GET_VARS, templ_buffer)
  json_keys = []

  # Removes the curly braces from each variable and places items ina new list.
  for var in find_vars:
    key = var.replace("{", "").replace("}", "")
    json_keys.append(key)

  # Removes duplicates from the list.
  filter_vars = list(set(json_keys))
  json_dictonary = []

  # Gives each key a value.
  for key in filter_vars:
    json_dictonary.append([key, ""])

  # Creates the json structure.
  json_data = json.dumps(dict(json_dictonary), indent=4)
  
  # Displays data to the screen.
  if display_data == True:
    print(json_data)
  else:
    # Writes data to a file.
    with open(args.output, "w") as f:
      f.write(json_data)
      print(f"Successfully wrote {len(json_data)} bytes to {args.output}")


# Parses the keys and key values and replaces the content as specified by the user.
def parse_input(args):
  config_path = args.config_file
  template_path = args.template
  script_path = args.logic
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
  logic_buffer = read_file(script_path)

  if logic_buffer != None:
    exec(logic_buffer, locals())

  for key in data:
    # Code block reads through each key in the config file and extracts the value.
    match = "{" + key + "}"
    value = check_json_error(data, key)

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
  parser.add_argument("-l", "--logic", action="store")
  parser.add_argument("-p", "--parse_template", action="store")
  parser.add_argument("-o", "--output", action="store", help="The file path to the file you want to create")
  args = parser.parse_args()

  if args.config_file != None and args.template != None:
    parse_input(args)
  elif args.parse_template != None and args.output != None:
    search_template_variables(args)
  elif args.parse_template != None and args.output == None:
    search_template_variables(args, display_data=True)
  else:
    print("Error: No config file or template file was specified.")


if __name__ == "__main__":
  main()