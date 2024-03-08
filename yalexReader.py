from utils import parse_rules

def yalexReader(myFile: str):

  definitions = {}
  rules = {}

  with open(myFile, "r") as f:
    lines = f.readlines()

    current_key = None
    current_value = ""

    for line in lines:
      if line.startswith("rule"):
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

  rules = parse_rules(myFile)

  translatedRules = {}
  for rule in rules:
    if rules[rule] in definitions:
      translatedRules[rule] = definitions[rules[rule]]
    else:
      translatedRules[rule] = rules[rule]

  expression = ''
  for rule in translatedRules:
    expression += translatedRules[rule] + '|'
  expression = expression[:-1]

  return definitions, rules, translatedRules, expression
