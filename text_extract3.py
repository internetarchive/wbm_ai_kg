import os
import argparse
import html2text

def extract_text_from_html(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Try decoding with UTF-8
            try:
                html_content = file.read().decode('utf-8')
            # If UTF-8 decoding fails, try different encodings
            except UnicodeDecodeError:
                html_content = file.read().decode('latin-1')
                
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images = True
        text_maker.ignore_emphasis = True
        text_maker.bypass_tables = True
        
        text_content = text_maker.handle(html_content)
        
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
                    subfolder_name = os.path.basename(root)
                    text_file_name = f"{os.path.splitext(file)[0]}_{subfolder_name}.txt"
                    text_file_path = os.path.join(root, text_file_name)
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
