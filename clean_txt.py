import os
import argparse

def delete_txt_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt") or file.endswith(".json") :
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete all .txt files inside a folder and its subfolders.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing .txt files.")
    
    args = parser.parse_args()
    delete_txt_files(args.folder_path)
