import argparse, json

# Returns the value that is stored in the json key.
def check_json_error(data, key: str) -> str | None:
  try:
    out = data[key]
    return out
  except Exception as e:
    return None

# Parses the keys and key values and replaces the content as specified by the user.
def parse_input(args):
  config_path = args.config_file
  template_path = args.template
  output = args.output

  # The config file as a string.
  config_buffer = ""
  with open(config_path, "r") as f:
    config_buffer = f.read()

  data = None

  try:
    # Creates the json object from the config string.
    data = json.loads(config_buffer)
  except Exception as e:
    print(f"Error: {e}")

  # The template file as a string.
  templ_buffer = ""
  with open(template_path, "r") as f:
    templ_buffer = f.read()
   
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
  parser.add_argument("-o", "--output", action="store", help="The file path to the file you want to create")
  args = parser.parse_args()

  if args.config_file != None and args.template != None:
    parse_input(args)
  else:
    print("Error: No config file or template file was specified.")


if __name__ == "__main__":
  main()