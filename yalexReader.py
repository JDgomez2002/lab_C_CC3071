from utils import parse_rules

def yalexReader(myFile: str):

  definitions = {}
  rules = {}

  errors = False
  error = ''

  with open(myFile, "r") as f:
    lines = f.readlines()

    current_key = None
    current_value = ""

    for line in lines:
      if line.startswith("rule"):
        break

      if '"' in line and not errors:
        errors = True
        error = 'Error: Invalid character: (")'
        break


      line = line.strip()
      if line.startswith("let"):
        if current_key is not None:
          definitions[current_key] = current_value.strip()
        _, line = line.split("let", 1)
        current_key, current_value = line.split("=", 1)
        current_key = current_key.strip()
        current_value = current_value.strip()
      else:
        current_value += " " + line

    if current_key is not None:
      definitions[current_key] = current_value.strip().replace('.', '\\.')

  def format_definitions(definitions):
    for def_name, def_value in reversed(definitions.items()):
      for name, definition in definitions.items():
        definitions[name] = definition.replace(def_name, def_value)
    return definitions

  definitions = format_definitions(definitions)

  # check if a definition is empty
  for definition in definitions:
    if definitions[definition].strip() == '' and not errors:
      errors = True
      error = 'Error: Empty definition'
      break

  rules = parse_rules(myFile)

  translatedRules = {}
  for rule in rules:
    if rules[rule].strip() == '' and not errors:
      errors = True
      error = 'Error: Empty rule'
      break
    if rules[rule] in definitions:
      translatedRules[rule] = definitions[rules[rule]]
    else:
      if '\\' not in rules[rule] and not errors:
        errors = True
        error = 'Error: Definition not defined'
        break
      translatedRules[rule] = rules[rule]

  expression = ''
  for rule in translatedRules:
    expression += translatedRules[rule] + '|'
  expression = expression[:-1]

  if errors:
    expression = ''
    error = '\n' + error + '\n'

  return definitions, rules, translatedRules, expression, errors, error
