import ctypes   # This will let us get around the Recycle Bin permissions error. 
import sys
import os

# defining the get_size function. os.scan iterates over the directors (ithink).
# Each entry will be an os.DirEntry object
# C:\Users\muska\source\repos\FileScannerChaippy\FileScannerChaippy01.py  (refference)

def is_admin():
    """Check if the script is running with administrative privileges."""   #Be sure to run terminal in administrator mode for this to work.
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_size(path="D:\\"):
    """Scans directory for file sizes, skipping folders it doesn't have permission for such as D:\System"""
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += get_size(entry.path)
    except PermissionError:
        print(f"Permission defined for {path}. Skipping...")
    return total


# this function gets the 10 largest files.

def get_largest_files(path="D:\\", top_n=10):
    files = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    files.append((entry.path, entry.stat().st_size))
                elif entry.is_dir():
                    files.extend(get_largest_files(entry.path))
        files.sort(key=lambda x: x[1], reverse=True)
    except PermissionError:
        print(f"Permission denied for {path}. Skipping...")
    return files[:top_n]


# I haven't used __main__ before, but I see others use the __name__ == "__main__""
# We can only use one __main__ because that's good code form, using two got around the UAC.
# The suggestion:  By using this idiom, you can have code that can be both used by other scripts when imported as a module and can be run standalone, we can use this for pipeline later?
if __name__ == "__main__":
    if not is_admin():
        # The script is not currently running with admin rights
        # elevate permissions
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    # The scrip returns the 10 largest and filtiest files on the drive right now    
    else:
        path_to_check = "D:\\"  # Entire Drive Scan
        print(f"Total size of '{path_to_check}': {get_size(path_to_check) / (1024*1024):.2f} MB")
        print("Top 10 largest files:")
        for file, size in get_largest_files(path_to_check):
            print(f"{file}: {size / (1024*1024):.2f} MB")

# Future notes: Look for other exceptions that might arise.
# plan to add an input/output to seearch for smaller files, specific files, etc.
# Eventually with options to suggest to remove files, etc. 
# Maybe incorporate rasa open source to act as a chatbot?

