
import os, fnmatch
name_string = "mass5920004_1300.0_mass51_900.0_dmf3u22_0.1_xs_3.0674e-10_tag_712946019"

new_string = name_string.split("_")

#print(new_string)


import os
import fnmatch

def find_tar_gz_files(base_path, pattern='*.tar.gz'):
    """
    Searches for .tar.gz files in base_path matching the given pattern.

    :param base_path: Directory where the search should start
    :param pattern: Pattern to match file names (default is '*.tar.gz')
    :return: List of matching file paths
    """
    matching_files = []
    
    try:
        for root, dirs, files in os.walk(base_path):
            print(f"Searching in directory: {root}")  # Debugging output
            for file_name in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, file_name)
                print(f"Found file: {file_path}")  # Debugging output
                matching_files.append(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

    return matching_files

# Usage example
base_path = '/home/amdesai/Downloads/LO/'  # Replace with the path where you want to start the search
pattern = 'mass5920004_1300.0_mass51_900.0_dmf3u22_0.1_xs_3.0674e-10_tag_*.tar.gz'    # Replace with the pattern you are looking for


tar_gz_files = find_tar_gz_files(base_path, pattern)
if not tar_gz_files:
    print("No .tar.gz files found.")
else:
    for file in tar_gz_files:
        print(f'Found file: {file}')

"""
folders = find_folder(base_path, pattern)
print(folders)
for folder in folders:
    print(f'Found folder: {folder}')
"""