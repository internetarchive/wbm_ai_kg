import os
import requests
import re
import argparse

def extract_timestamp_and_original_url(wayback_url):
    """
    Extract the timestamp and original URL from a Wayback Machine URL.
    
    Parameters:
        wayback_url (str): The Wayback Machine URL.
    
    Returns:
        tuple: The timestamp and the original URL.
    """
    match = re.search(r'/web/(\d{14})/(https?://.+)', wayback_url)
    if match:
        timestamp = match.group(1)
        original_url = match.group(2)
        return timestamp, original_url
    else:
        raise ValueError("Timestamp or original URL not found in the Wayback Machine URL.")

def save_html_content(wayback_url, output_dir="temp"):
    """
    Download and save HTML content from a Wayback Machine URL into a specified directory.
    The HTML file will be saved as content.html inside a subfolder named after the timestamp.
    
    Parameters:
        wayback_url (str): The Wayback Machine URL.
        output_dir (str): The directory where HTML content will be saved.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Extract timestamp and original URL
    timestamp, original_url = extract_timestamp_and_original_url(wayback_url)
    
    # Create a subfolder named after the timestamp
    subfolder_path = os.path.join(output_dir, timestamp)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    
    # The file will be saved as content.html inside the subfolder
    file_path = os.path.join(subfolder_path, "content.html")
    
    # Fetch the HTML content and save it
    archive_url = f"https://web.archive.org/web/{timestamp}/{original_url}"
    
    try:
        response = requests.get(archive_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"HTML content saved as {file_path}")
        else:
            print(f"Failed to download content for {timestamp}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading content for {timestamp}: {e}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Fetch and save HTML content from Wayback Machine URLs.")
    parser.add_argument('cdx_url_1', type=str, help="First Wayback Machine URL")
    parser.add_argument('cdx_url_2', type=str, help="Second Wayback Machine URL")

    args = parser.parse_args()

    # Convert URLs to strings (although they are already strings)
    cdx_url_1 = str(args.cdx_url_1)
    cdx_url_2 = str(args.cdx_url_2)

    # Create the default folder "temp"
    output_dir = "temp_base"
    
    # Save HTML content from both URLs inside the "temp" folder in their respective subfolders
    save_html_content(cdx_url_1, output_dir)
    save_html_content(cdx_url_2, output_dir)

    print(f"HTML content saved in the '{output_dir}' folder.")
