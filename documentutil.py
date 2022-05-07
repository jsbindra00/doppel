import os
from shutil import copy
import subprocess



# ███╗░░██╗░░███╗░░░██████╗░██╗░░██╗████████╗██████╗░██╗██████╗░██████╗░██████╗░
# ████╗░██║░████║░░██╔════╝░██║░░██║╚══██╔══╝██╔══██╗██║██╔══██╗╚════██╗██╔══██╗
# ██╔██╗██║██╔██║░░██║░░██╗░███████║░░░██║░░░██████╔╝██║██║░░██║░█████╔╝██████╔╝
# ██║╚████║╚═╝██║░░██║░░╚██╗██╔══██║░░░██║░░░██╔══██╗██║██║░░██║░╚═══██╗██╔══██╗
# ██║░╚███║███████╗╚██████╔╝██║░░██║░░░██║░░░██║░░██║██║██████╔╝██████╔╝██║░░██║
# ╚═╝░░╚══╝╚══════╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═════╝░╚═════╝░╚═╝░░╚═╝
# DISCLAIMER: i am not responsible for what you choose to do with my code. have fun.

temporary_folder_name = "document_folder"

def change_directory(new_directory):
    os.chdir(new_directory)
def convertStringToDirectory(string):
    return string.replace('\\', '\\\\')


def writeFile(file_contents, file_name):
    file = open(file_name, "w")
    file.write(file_contents)
    file.close()

def runScript(path, *argv):
    print(list(argv))
    subprocess.call(["pythonw ", path] + list(argv))

def get_file_from_directory(directory, file_name):
    if directory is None : directory = os.getcwd()
    return os.path.join(directory, file_name)
def open_file(path):
    os.startfile(path)
def readFile(path):
    file = open(path)
    return file.readlines()
    
def merge_dir_and_callable(dir, callable):
    return dir + "\\" + callable

def create_new_folder(dir, folder_name):
    path_name = merge_dir_and_callable(dir, folder_name)
    if not os.path.exists(path_name):
        os.makedirs(path_name)
        return path_name
        
    else:
        print("please choose a new temporary folder name for the program")
        return path_name

def extract_all_files_to_dir(src, dest, extension):
    os.chdir(src)
    print(src)
    print(dest)

    file_paths = []
    for root, dirs, files in os.walk(src):
        if root == dest: continue
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                print("COPYING " + file_path + " ....")
                copy(file_path, dest)
                file_paths.append(file_path)
    return file_paths






import os
def get_immediate_subdirectories(a_dir):
    return [os.path.join(a_dir, name)  for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


dir = "C:\\Users\\jasbi\\OneDrive\\Documents\\Items - Copy\\Dad"
x = get_immediate_subdirectories(dir)




def create_folders(dirs):
    for dir in x:
        change_directory(dir)
        create_new_folder(dir, "studio")



