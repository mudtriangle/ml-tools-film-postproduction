import json

with open('../test_liene/file_structure.json', 'r') as f:
    structure = json.load(f)

print(json.dumps(structure, indent=4))
