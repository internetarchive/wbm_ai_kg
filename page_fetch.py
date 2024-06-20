import subprocess
import pandas as pd
import argparse
from tqdm import tqdm
import json
import os

def fetch_cdx_data(url):
    # Using curl to make the request to the Wayback Machine CDX API
    curl_command = f"curl -s 'http://web.archive.org/cdx/search/cdx?url={url}&output=json'"
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Failed to fetch data: {result.stderr}")
    
    data = json.loads(result.stdout)
    
    if len(data) == 0:
        raise Exception("No data retrieved from the Wayback Machine CDX API.")
    
    headers = ["urlkey", "timestamp", "original", "mimetype", "statuscode", "digest", "length"]
    records = data[1:]
    
    # Adding a progress bar for processing records
    with tqdm(total=len(records), desc="Processing records") as pbar:
        df = pd.DataFrame(records, columns=headers)
        for _ in df.iterrows():
            pbar.update(1)
    
    return df

def filter_data(df):
    # Filtering the DataFrame
    filtered_df = df[(df['mimetype'] == 'text/html') & (df['statuscode'] == '200')]
    return filtered_df[['timestamp', 'original']]

def save_to_csv(df, filename, num_lines=10):
    # Get the last num_lines of the DataFrame
    df = df.tail(num_lines)
    
    # Saving the DataFrame to a CSV file with a progress bar
    with tqdm(total=1, desc="Saving to CSV") as pbar:
        df.to_csv(filename, index=False)
        pbar.update(1)
    print(f"Data successfully saved to {filename}")
    return df  # Return the DataFrame for further processing

def fetch_and_save_content(row, base_dir):
    timestamp = row['timestamp']
    original_url = row['original']
    archive_url = f"https://web.archive.org/web/{timestamp}id_/{original_url}"
    
    # Create a directory named after the timestamp inside the base directory
    directory = os.path.join(base_dir, timestamp)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Fetch the content using curl
    content_command = f"curl -s '{archive_url}'"
    result = subprocess.run(content_command, shell=True, capture_output=True)
    
    if result.returncode != 0:
        raise Exception(f"Failed to fetch content: {result.stderr}")
    
    # Save the content to a file in the directory
    filepath = os.path.join(directory, "content.html")
    with open(filepath, 'wb') as file:  # Write in binary mode to avoid encoding issues
        file.write(result.stdout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch CDX data and save to CSV.')
    parser.add_argument('url', type=str, help='The URL to search in the Wayback Machine')
    parser.add_argument('output', type=str, help='The output CSV file name')
    parser.add_argument('--full', action='store_true', help='Dump full data')
    parser.add_argument('--num_lines', type=int, default=10, help='Number of lines to save from the end of the CSV')
    
    args = parser.parse_args()
    df = fetch_cdx_data(args.url)
    
    if not args.full:
        df = filter_data(df)
    
    df = save_to_csv(df, args.output, args.num_lines)  # Save and get the last num_lines of data
    
    # Create a base directory named after the CSV file (without .csv extension)
    base_dir = os.path.splitext(args.output)[0]
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Fetch and save the content for each filtered record with a progress bar
    with tqdm(total=len(df), desc="Fetching and saving content") as pbar:
        for _, row in df.iterrows():
            fetch_and_save_content(row, base_dir)
            pbar.update(1)
