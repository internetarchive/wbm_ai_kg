import os
import re
import json
import argparse
from tqdm import tqdm

def read_tuples_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    tuples = []
    pattern = re.compile(r'\(\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\)')
    
    for line in content.splitlines():
        match = pattern.search(line)
        if match:
            tuples.append(match.groups())

    return tuples

def validate_and_group_tuples(tuples):
    complete_tuples = [t for t in tuples if len(t) == 5 and all(t)]
    grouped_tuples = {}

    for t in complete_tuples:
        subject, predicate, obj, subject_type, obj_type = t
        group_key = subject
        if group_key not in grouped_tuples:
            grouped_tuples[group_key] = []
        grouped_tuples[group_key].append(t)
    
    return complete_tuples, grouped_tuples

def save_processed_tuples(output_file, complete_tuples, grouped_tuples):
    with open(output_file, 'w') as file:
        json.dump({'complete_tuples': complete_tuples, 'grouped_tuples': grouped_tuples}, file, indent=4)

def main(input_file):
    tuples = read_tuples_from_file(input_file)
    
    complete_tuples, grouped_tuples = validate_and_group_tuples(tuples)
    
    output_file = os.path.splitext(input_file)[0] + '.json'
    save_processed_tuples(output_file, complete_tuples, grouped_tuples)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process key-value-relation tuples, remove incomplete ones, and group similar tuples together.")
    parser.add_argument("input_file", type=str, help="Path to the input .txt file containing key-value-relation tuples.")
    
    args = parser.parse_args()
    
    with tqdm(total=100, desc="Processing tuples") as pbar:
        main(args.input_file)
        pbar.update(100)
