import os
import sys
import rarfile
import zipfile
from tqdm import tqdm  

LOG_FILE = os.path.join(os.path.expanduser("~"), "extractor_log.txt")

def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def extract_rar(file_path):
    try:
        rarfile.UNRAR_TOOL = os.path.join(os.path.dirname(__file__), "UnRAR.dll")
        if not rarfile.is_rarfile(file_path):
            log("Not a valid RAR file")
            return

        output_folder = os.path.splitext(file_path)[0]
        os.makedirs(output_folder, exist_ok=True)

        with rarfile.RarFile(file_path) as rf:
            files = rf.namelist()
            log(f"Extracting {len(files)} files from RAR")
            
            with tqdm(total=len(files), desc="Extracting RAR", unit="file") as pbar:
                for file in files:
                    rf.extract(file, output_folder)
                    pbar.update(1)

        log(f"Extracted RAR to: {output_folder}")
    except Exception as e:
        log(f"RAR Extraction error: {e}")

def extract_zip(file_path):
    try:
        if not zipfile.is_zipfile(file_path):
            log("Not a valid ZIP file")
            return

        output_folder = os.path.splitext(file_path)[0]
        os.makedirs(output_folder, exist_ok=True)

        with zipfile.ZipFile(file_path, 'r') as zf:
            files = zf.namelist()
            log(f"Extracting {len(files)} files from ZIP")

            with tqdm(total=len(files), desc="Extracting ZIP", unit="file") as pbar:
                for file in files:
                    zf.extract(file, output_folder)
                    pbar.update(1)

        log(f"Extracted ZIP to: {output_folder}")
    except Exception as e:
        log(f"ZIP Extraction error: {e}")

if __name__ == "__main__":
    log("Program started")

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        log(f"Received file: {file_path}")

        if file_path.lower().endswith(".rar"):
            extract_rar(file_path)
        elif file_path.lower().endswith(".zip"):
            extract_zip(file_path)
        else:
            log("Unsupported file format")
    else:
        log("No file provided.")

