import re

def format(regex):
    all_operators = ["|", "+", "?", "*"]
    binary_operators = ["|"]
    res = ""

    for i in range(len(regex)):
        c1 = regex[i]

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            res += c1

            if (
                c1 != "("
                and c2 != ")"
                and c2 not in all_operators
                and c1 not in binary_operators
            ):
                res += "."

    res += regex[-1]
    return res


def shunting_yard(regex):
    precedence = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
    queue = []
    stack = []

    regex = format(regex)

    # CHAPUS
    hasHash = False
    if "#" in regex:
        hasHash = True
        regex = regex.replace("#", "")
    # CHAPUS

    for token in regex:
        if token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()
        elif token in precedence: # else
            while (
                stack
                and stack[-1] != "("
                and precedence[token] <= precedence[stack[-1]]
            ):
                queue.append(stack.pop())
            stack.append(token)
        else: 
            stack.append(token)

    while stack:
        queue.append(stack.pop())

    # CHAPUS
    # print('regex:', regex)
    result = "".join(queue)
    result = result.replace("|.|", "||")
    if hasHash:
        result += "#." # Add the # to the end of the expression
    # CHAPUS

    # print('result:', result)

    return result


def add_concat(regex):
    output = ""
    operators = set([".", "|", "*", "(", ")"])  # regex operators
    for i in range(len(regex) - 1):
        output += regex[i]
        if (
            (regex[i] not in operators and regex[i + 1] not in operators)
            or (regex[i] not in operators and regex[i + 1] == "(")
            or (regex[i] == ")" and regex[i + 1] not in operators)
            or (regex[i] == "*" and regex[i + 1] not in operators)
            or (regex[i] == "*" and regex[i + 1] == "(")
        ):
            output += "."
    output += regex[-1]
    return output

def isValidExpression(expression):
    stack = []
    if expression == "" or expression.isspace():
        print("\tError: Empty expression")
        return False
    for char in expression:
        if not char.isalnum() and char not in {"*", "|", ".", "ϵ", "(", ")", "+", "?"}:
            print("\tError: Invalid character in expression")
            return False
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack.pop() != '(':
                print("\tError: Unbalanced expression")
                return False
    balanced = len(stack) == 0
    if balanced:
        return True
    else:
        print("\tError: Unbalanced expression")
        return False
    # return len(stack) == 0

chars = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]

def translateBracketsExpression(regex: str):
    newRegex = "("
    if '[' not in regex or ']' not in regex:
        return regex
    elif '-' in regex and '^' not in regex:
        first = ''
        regex = regex.replace("'",'')
        for char in regex:
            if char == '-':
                first = newRegex[-1]
            elif char != ']':
                if first != '':
                    if char != newRegex[-1]:
                        for i in range(chars.index(first) + 1, chars.index(char) + 1):
                            newRegex += '|' + chars[i]
                        first = ''
                        if regex.index(char) != len(regex) - 1 and regex[regex.index(char) + 1] != ']':
                            newRegex += '|'
                elif char != '[':
                    newRegex += char
    elif "''" in regex:
        regex = regex.replace("[", '').replace("]",'').split("''")
        for char in regex:
            newRegex += char.replace("'",'')
            if char != regex[-1]:
                newRegex += '|'
    elif '"' in regex:
        regex = list(regex.replace("[", '').replace("]",'').replace('"',''))
        for char in regex:
            newRegex += char
            if char != regex[-1]:
                newRegex += '|'
        newRegex = newRegex.replace('\\|', '\\')
    elif '^' in regex:
        regex = regex.replace('^', '')
        # negativeNewRegex = newRegex
        first = ''
        regex = regex.replace("'",'')
        for char in regex:
            if char == '-':
                first = newRegex[-1]
            elif char != ']':
                if first != '':
                    if char != newRegex[-1]:
                        for i in range(chars.index(first) + 1, chars.index(char) + 1):
                            newRegex += '|' + chars[i]
                        first = ''
                        if regex.index(char) != len(regex) - 1 and regex[regex.index(char) + 1] != ']':
                            newRegex += '|'
                elif char != '[':
                    newRegex += char
        result = '('
        for char in chars:
            if char not in newRegex:
                result += char + '|'
        result += ')'
        newRegex = result.replace('|)', '')
    else:
        return regex

    return newRegex + ')'

def parseDefinitions(self, filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()

        current_key = None
        current_value = ""

        for line in lines:
            if line.startswith("rule"):
                break

            line = line.strip()
            if line.startswith("let"):
                if current_key is not None:
                    self.definitions[current_key] = current_value.strip()
                _, line = line.split("let", 1)
                current_key, current_value = line.split("=", 1)
                current_key = current_key.strip()
                current_value = current_value.strip()
            else:
                current_value += " " + line

        if current_key is not None:
            self.definitions[current_key] = current_value.strip()

    def format_definitions(definitions):
        for def_name, def_value in reversed(definitions.items()):
            for name, definition in definitions.items():
                definitions[name] = definition.replace(def_name, def_value)
        return definitions

    self.definitions = format_definitions(self.definitions)

def parse_rules(filename: str):
        with open(filename, "r") as file:
            content = file.read()

        # Find the line containing the keyword "rule"
        rule_index = content.find("rule")
        if rule_index == -1:
            return []

        # Extract the content after the "rule" line
        content = content[rule_index:]

        pattern = (
            r"(\w+)\s*\{\s*return\s*(\w+)\s*\}|\'([^\'\\])\'\s*\{\s*return\s*(\w+)\s*\}"
        )

        matches = re.findall(pattern, content)

        tokens = []

        for match in matches:
            if match[0]:
                token_name = match[0]
                token_value = token_name
            else:
                token_name = match[3]
                token_value = match[2]
                if token_value in ["+", "-", "*", "/", "(", ")"]:
                    token_value = "\\" + token_value

            tokens.append((token_name, token_value))

        rules = dict(tokens)

        return rules