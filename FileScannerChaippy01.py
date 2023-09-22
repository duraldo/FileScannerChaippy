import ctypes   
import sys
import os


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


#We are adding a simply input/output.
if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
     
    else:
        user_input = input("Hey! Welcome to Chaippy File Scanner, would you like to scan for the top 10 biggest files? Yes? No?")
        if user_input.lower() == "yes" or user_input.lower() == "y":   
            #Continues to ask for input. using while loop

            #Top 10 files in the drive.
            while True:
                file_type = input("I'm not a mind reader, would you like to scan the whole drive or a specfic folder?")
            
                if file_type.lower() == "drive":
                    path_to_check = "D:\\"  # Entire Drive Scan
                    print(f"Total size of '{path_to_check}': {get_size(path_to_check) / (1024*1024):.2f} MB")
                    print("Top 10 largest files:")
                    for file, size in get_largest_files(path_to_check):
                        print(f"{file}: {size / (1024*1024):.2f} MB")
                # if filetype is asked for, it doesn't work yet, placeholder.
                elif file_type.lower() == "filetype" or file_type.lower() == "file":
                    print ("Too bad, that feature doesn't work yet.")


        elif user_input.lower() == "no" or user_input.lower() == "n":   
        # elif user_input.lower() == "no" or user_input.lower() == "n": can also be used.

            print("Okay, fine, be that way, bye! :P")
        else:
            print("Invalid Input. please enter correct input")



# Future notes: Look for other exceptions that might arise.
# plan to add an input/output to seearch for smaller files, specific files, etc.
# Eventually with options to suggest to remove files, etc. 
# Maybe incorporate rasa open source to act as a chatbot?

