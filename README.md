# wbm_ai_kg
Google Summer of Code (GSoC) 2024 Wayback Machine GenAI Knowledge Graph project

# Wayback Machine CDX Fetcher

This Python script fetches data from the Wayback Machine CDX API for a given URL, filters the data, and saves it to a TSV (Tab-Separated Values) file. It also downloads and saves the archived content for each filtered record.

## Requirements

The requirements for the environment are in the file conda_requirements.txt

## Usage
## Page Fetch


```python page_fetch.py <url to fetch> <file name in .tsv> --num_lines 50```

example:

```python page_fetch.py https://channel3now.com/2024/07/29/17-year-old-ali-al-shakati-arrested-in-connection-with-the-stabbings-in-southport-england/ channel.tsv --num_lines=1000```


It fetches data from the Wayback Machine CDX API for the provided URL. Filters the data to retain only successful responses with text/html mimetype. Saves the filtered data to a TSV file, keeping the last specified number of lines.
Creates a directory for each timestamped entry and fetches the archived content of the corresponding web page, saving it as content.html.

Error Handling:
If fetching data or content fails, appropriate error messages are displayed.
The script ensures that directories for saving content are created only if they do not already exist. If a file with the same name as the directory exists, an exception is raised.

## Text Extract

```python text_extract.py /path/to/main/folder```

example

```python text_extract.py channel```

This script extracts textual content from HTML files and saves it as plain text files. It is particularly useful for extracting visible text, titles, meta descriptions, and meta keywords from HTML files within a directory structure.

 Extracts text content from HTML files, including:
  - Page title
  - Meta description
  - Meta keywords
  - Visible text content from the HTML body
- **Encoding Handling**: Attempts to read HTML files using UTF-8 encoding. If that fails, it falls back to Latin-1 encoding.
- **Directory Traversal**: Recursively processes HTML files in all subdirectories of a specified main folder.
- **File Output**: Saves the extracted text content in `.txt` files, named based on the original HTML file and its containing subfolder.

The script will:
Traverse through all subfolders and locate .html files.
Extract text content from each .html file.
Save the extracted text in a new .txt file in the same folder, with a filename based on the original HTML file name and its containing subfolder.


## Generate Tuple 

```python generate_tuple.py <folder path>```

example:
```python generate_tuple.py /home/aura/gsoc/wbm_ai_kg/PageExtraction/channel```

This script processes text files in a given folder, splits them into smaller chunks, and generates key-value-relation tuples using an OpenAI language model.


- **Chunking:** Splits large text files into smaller chunks of customizable size (default: 2000 characters).
- **Tuple Extraction:** Extracts tuples representing relationships between entities in the text in the format `(key, value, relation, type of key, type of value)`.
- **Automated Processing:** Automatically processes all `.txt` files in the specified input folder and its subfolders.


## Key-Value Pair Processing
```python kvp_precess.py <folder path>```

example:
```python  kvp_precess.py /home/aura/gsoc/wbm_ai_kg/PageExtraction/channel```

This script processes key-value-relation tuples from files within a specified directory. The tuples are extracted, validated, and grouped based on specific criteria. The script is designed to handle files that start with `tupleLLM_`, and outputs the processed data in JSON format.

1. **Read Tuples:** The script reads tuples from files, where each tuple is a 5-element structure (subject, predicate, object, subject type, object type).
2. **Validate and Group Tuples:** Incomplete tuples are removed, and the remaining tuples are grouped by their subject.
3. **Save Processed Data:** The processed tuples are saved in JSON format, with two sections: `complete_tuples` and `grouped_tuples`.
4. **Process Files in Directory:** The script recursively processes all files in the directory that start with `tupleLLM_`.

After this we will be ready with our JSONs to be rendered at the page. The scripts under webpage2/ render the current view of the page. 
