import argparse
import os
from mcmetadata import extract

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    metadata = extract(url="https://www.hostelworld.com/")
    text = metadata
    print(text)
    1/0
    if not text:
        print(f"No text extracted from {file_path}")
    else:
        print(f"Extracted text from {file_path}: {text[:100]}...")  # Print the first 100 characters

    return text

def save_text_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'content.html':
                html_file_path = os.path.join(root, file)
                extracted_text = extract_text_from_html(html_file_path)
                output_file_path = os.path.join(root, 'extracted_text.txt')
                save_text_to_file(extracted_text, output_file_path)
                print(f'Extracted text saved to {output_file_path}')



if __name__ == "__main__":
    metadata = extract(url="https://www.cnbc.com/2024/06/20/nvidia-tops-the-stock-market-values-of-germany-france-and-the-uk.html")
    text = metadata
    print(text)
    1/0
    parser = argparse.ArgumentParser(description='Extract text content from HTML files.')
    parser.add_argument('main_folder', type=str, help='The path to the main folder containing subfolders with HTML files.')
    args = parser.parse_args()
    
    process_directory(args.main_folder)
