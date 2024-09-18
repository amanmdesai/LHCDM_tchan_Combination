import re, csv
import os, fnmatch


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
            #print(f"Searching in directory: {root}")  # Debugging output
            for file_name in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, file_name)
                #print(f"Found file: {file_path}")  # Debugging output
                matching_files.append(file_path)
    except Exception as e:
        print(f"An error occurred: {e}")

    return matching_files

# Usage example
base_path = 'c/'  # Replace with the path where you want to start the search
pattern = '*.tar.gz'    # Replace with the pattern you are looking for


data_list = find_tar_gz_files(base_path, pattern)


"""
if not tar_gz_files:
    print("No .tar.gz files found.")
else:
        #with open(filename, 'w') as file:
        for file in tar_gz_files:
            #print(f'Found file: {file}')
            file = re.split(r'[/_]', file)
                print(file)
"""

filename = 'Sigmas.csv'


column_titles = [
    'quark', 'model', 'process', 'order',  'YPDG', 'my(GeV)', 'XPDG', 'mx(GeV)', 'coupling_name', 'coupling', 'XS', 'CS(pb)', 'Tag', 'FileExtension'
]

#mx(GeV) thecoupling_name file icoupling write modCS(pb)
with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_titles)

    # Process each file name in the list
    for data in data_list:
        # Split the string by both '/' and '_'
        result = re.split(r'[/_]', data)
        # Write the list as a row in the CSV file
        csvwriter.writerow(result)

