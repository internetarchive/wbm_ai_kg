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

def process_files_in_directory(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.startswith('tupleLLM_'):
                file_path = os.path.join(subdir, file)
                print(f"Processing {file_path}")
                tuples = read_tuples_from_file(file_path)
                complete_tuples, grouped_tuples = validate_and_group_tuples(tuples)
                output_file = os.path.splitext(file_path)[0] + '.json'
                save_processed_tuples(output_file, complete_tuples, grouped_tuples)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process key-value-relation tuples from all files named 'version_*' inside subfolders, remove incomplete ones, and group similar tuples together.")
    parser.add_argument("root_dir", type=str, help="Path to the root directory containing subfolders with 'version_*' files.")
    
    args = parser.parse_args()
    
    with tqdm(total=100, desc="Processing all files") as pbar:
        process_files_in_directory(args.root_dir)
        pbar.update(100)
    
