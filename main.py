import os
import subprocess
import sys
import glob


def run_command(command):
    try:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

def fetch_data(url, tsv_file, num_lines):
    command = f"python page_fetch.py {url} {tsv_file} --num_lines={num_lines}"
    run_command(command)
    print("Complete Fetch Data")

def fetch_data2(url1, url2):
    command = f"python page_fetch2.py {url1} {url2}"
    run_command(command)
    print("Complete Fetch Data")

def extract_text(main_folder):
    command = f"python text_extract.py {main_folder}"
    run_command(command)
    print("Complete Text Extract")



def generate_tuple(folder_path):
    command = f"python generate_tuple.py {folder_path}"
    run_command(command)
    print("Complete Generate Tuple")


def process_kvp(folder_path):
    command = f"python kvp_process.py {folder_path}"
    run_command(command)
    print("Complete Process KVP")

def delete_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
                print(f"Deleted empty folder: {dir_path}")
            except OSError:
                # Folder is not empty or some other error occurred, so we skip it
                pass
    
def approach1(folder_path):
    # List to store the paths of the txt files
    txt_file_paths = []

    # Iterate over all subdirectories in the given folder_path
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        # Check if it is a directory
        if os.path.isdir(subfolder_path):
            # Search for the .txt file named content_....txt in the subfolder
            txt_files = glob.glob(os.path.join(subfolder_path, "content_*.txt"))
            
            # If a txt file is found, add it to the list
            if txt_files:
                txt_file_paths.append(txt_files[0])  # Assuming there's only one .txt file per subfolder

    # Ensure there are exactly two .txt files
    if len(txt_file_paths) == 2:
        # Create the command with the two file paths as arguments
        command = f"python Approach/approach1.py {txt_file_paths[0]} {txt_file_paths[1]}"
        print(f"Running command: {command}")
        
        # Optionally, you can execute the command using subprocess
        subprocess.run(command, shell=True)
    else:
        print("Error: There should be exactly two 'content_*.txt' files, but found:", len(txt_file_paths))

def approach2(folder_path):
    # List to store the paths of the txt files
    txt_file_paths = []

    # Iterate over all subdirectories in the given folder_path
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        
        # Check if it is a directory
        if os.path.isdir(subfolder_path):
            # Search for the .txt file named content_....txt in the subfolder
            txt_files = glob.glob(os.path.join(subfolder_path, "tupleLLM_content_*.txt"))
            
            # If a txt file is found, add it to the list
            if txt_files:
                txt_file_paths.append(txt_files[0])  # Assuming there's only one .txt file per subfolder

    # Ensure there are exactly two .txt files
    if len(txt_file_paths) == 2:
        # Create the command with the two file paths as arguments
        command = f"python Approach/approach2.py {txt_file_paths[0]} {txt_file_paths[1]}"
        print(f"Running command: {command}")
        
        # Optionally, you can execute the command using subprocess
        subprocess.run(command, shell=True)
    else:
        print("Error: There should be exactly two 'tupleLLM_content_*.txt' files, but found:", len(txt_file_paths))




def main(url1, url2):
    fetch_data2(url1, url2)

    main_folder="temp_base"
    extract_text(main_folder)
    
    text_folder_path = os.path.join(main_folder, "output")
    generate_tuple(main_folder)
    
    process_kvp(main_folder)
    delete_empty_folders(text_folder_path)
    approach1(main_folder)
    approach2(main_folder)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <url1> <url2>")

    else:
        url = sys.argv[1]
        url2=sys.argv[2]
        main(url, url2)
