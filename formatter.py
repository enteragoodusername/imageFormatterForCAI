from os.path import exists, isdir, isfile
from PIL import Image
from pillow_heif import register_heif_opener
import os
import platform

def get_files_and_add(path : str, path_list : list):
    if os.path.isfile(path):
        path_list.append(path)
        return
    assert(os.path.isdir(path))
    for root, dirs, files in os.walk(path):
        for file in files:
            if file[0] == ".":
                continue
            file_path = os.path.join(root, file)
            assert os.path.isfile(file_path), file_path + " not recognized as a file, you probably chose too broad of a directory and hit a system file."
            path_list.append(file_path)
    
def create_mirror_directory(path : str,out_dir : str):
    assert(os.path.isdir(path))
    os.makedirs(out_dir,exist_ok=True)
    for root, dirs, files in os.walk(path):
        new_dir = root.replace(path,out_dir)
        if len(dirs) == 0:
            os.makedirs(new_dir, exist_ok=True)
    return out_dir

included_formats = (
        ".png",
        # jpeg formats
        ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp",
        ".heic",
        ".heif",
        ".webp" 
        )
print("Supported formats are: " + ' '.join(included_formats)) 
path = input("Enter a directory to recursively format images into 128x128 pngs\n")
path = os.path.abspath(path)

if not os.path.isdir(path):
    print("Not a valid dir, terminating")
    exit()

default_out_dir =  path+"_mirrored"
out_dir= input(f"Enter an output directory. Leave empty for {default_out_dir}\n")
if out_dir.strip() == "":
    out_dir=  default_out_dir

path_list : list[str]= []

get_files_and_add(path, path_list)

image_path_list = []
possible_error_flag : bool = False
delete_later_list : list[str]= [] 
for file in path_list:

    extension : str = file[file.rfind("."):].lower()

    # Im starting to think apple uses  HEIC to make us miserable
    if extension in included_formats:
        image_path_list.append(file)
    else:
        possible_error_flag = True
    


if len(image_path_list) == 0:
    print("No valid image file extensions found, supported formats are: " + ' '.join(included_formats)) 
    exit()
print("\n".join(image_path_list))




print()
if possible_error_flag: print("Other files were found that were not images, these will be ignored")


if os.path.isdir(out_dir):
    print(f"Theres an existing directory with the name {out_dir}, images will be added to there.")

confirmation = ""
while confirmation.lower() != "y":
    confirmation = input(f"Do you wish to format {len(image_path_list)} images listed into {out_dir}? [y/n] : \n")
    if confirmation.lower() == "n":
        print("Exiting")
        exit()

create_mirror_directory(path,out_dir)
previous_directory = ""
counter = 0
assert(os.path.isdir(out_dir))
register_heif_opener()
for file in image_path_list:
    if platform.system() == "Windows":
         new_file_directory : str = file[0:file.rfind("\\")].replace(path,out_dir)  
    else:    
        new_file_directory : str = file[0:file.rfind("/")].replace(path,out_dir)
    
    if new_file_directory != previous_directory:
        previous_directory = new_file_directory
        counter = 0

    new_file_path = f"{new_file_directory}/img{counter}.png" 
    counter+= 1
    print(new_file_path)

    while( os.path.isfile(new_file_path)):
        new_file_path = f"{new_file_directory}/img{counter}.png" 
        counter+= 1

    image = Image.open(file)
    new_size = (128,128)  # Specify the desired width and height
    resized_image = image.resize(new_size)
    resized_image.convert("RGB").save(new_file_path)

print()
print(f"Done! Files are in {out_dir}")

