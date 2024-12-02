import re
import json
import sys

def read_file_lines(filename):
    # différents encodages pour lire le fichier
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError:
            if encoding == encodings[-1]:
                raise
            continue

def parse_line(line):
    line = line.strip()
    if not line or line.startswith('%') or line.startswith('#'):
        return []
    
    # regex pour trouver les instructions
    pattern = r'si\s*\(.*?\)|boucle|fin|pause|[}{]|[A-Za-z0-9]+'
    tokens = re.findall(pattern, line)
    
    parsed_instructions = []
    for token in tokens:
        token = token.strip()
        if re.match(r'si\s*\(.*?\)', token):
            # pour les différentes conditions
            condition = re.search(r'\((.*?)\)', token).group(1)
            parsed_instructions.append({"type": "si", "condition": condition, "content": []})
        elif token == 'boucle':
            parsed_instructions.append({"type": "boucle", "content": []})
        elif token == '}':
            parsed_instructions.append({"type": "end_block"})
        elif token == 'fin':
            parsed_instructions.append({"type": "fin"})
        elif token == 'pause':
            parsed_instructions.append({"type": "instruction", "value": 'pause'})
        elif token in ['I', 'G', 'D', '0', '1']:
            parsed_instructions.append({"type": "instruction", "value": token})
        else:
            # 如果有未识别的指令
            parsed_instructions.append({"type": "instruction", "value": token})
    
    return parsed_instructions

def parse_instructions(lines):
    instructions = []
    stack = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        index += 1

        parsed_line = parse_line(line)
        if not parsed_line:
            continue

        for parsed in parsed_line:
            if parsed["type"] == "end_block":
                if stack:
                    stack.pop()
                else:
                    print("pattern non trouvé")
                continue
            elif parsed["type"] in ["si", "boucle"]:
                if stack:
                    stack[-1]["content"].append(parsed)
                else:
                    instructions.append(parsed)
                stack.append(parsed)
            elif parsed["type"] == "fin":
                if stack:
                    stack[-1]["content"].append(parsed)
                else:
                    instructions.append(parsed)
            else:
                if stack:
                    stack[-1]["content"].append(parsed)
                else:
                    instructions.append(parsed)
    return instructions

def read_turing_file(filename):
    lines = read_file_lines(filename)
    parsed_structure = parse_instructions(lines)
    result = {"parsed_structure": parsed_structure}
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python read_turing_file.py <输入文件名> <输出文件名>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    result = read_turing_file(input_filename)
    
    # stocker les résultats sous forme json
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print(f"output: {output_filename}")