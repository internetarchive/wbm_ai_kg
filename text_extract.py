import os
import argparse
from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Try decoding with UTF-8
            try:
                html_content = file.read().decode('utf-8')
            # If UTF-8 decoding fails, try different encodings
            except UnicodeDecodeError:
                html_content = file.read().decode('latin-1')
                
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text from different parts of the page
        title = soup.title.string if soup.title else ''
        
        meta_description = ''
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_description_tag:
            meta_description = meta_description_tag['content']
        
        meta_keywords = ''
        meta_keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords_tag:
            meta_keywords = meta_keywords_tag['content']
        
        visible_text = ' '.join(soup.stripped_strings)
        
        # Concatenate all parts with newline separators
        text_content = '\n'.join([title, meta_description, meta_keywords, visible_text])
        
        return text_content.strip()
    except Exception as e:
        print(f'Error processing {file_path}: {e}')
        return ''

def process_directory(main_folder):
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.html'):
                html_file_path = os.path.join(root, file)
                text_content = extract_text_from_html(html_file_path)
                if text_content:
                    text_file_path = os.path.join(root, os.path.splitext(file)[0] + '.txt')
                    # Split content into lines and filter out empty lines
                    lines = filter(lambda x: x.strip(), text_content.split('\n'))
                    with open(text_file_path, 'w', encoding='utf-8') as text_file:
                        text_file.write('\n'.join(lines))
                    print(f'Extracted text from {html_file_path} to {text_file_path}')
                else:
                    print(f'No text extracted from {html_file_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract text content from HTML files.')
    parser.add_argument('main_folder', type=str, help='The path to the main folder containing subfolders with HTML files.')
    args = parser.parse_args()
    
    process_directory(args.main_folder)
