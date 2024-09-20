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
base_path = '/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/c'  # Replace with the path where you want to start the search
pattern = '*.tar.gz'    # Replace with the pattern you are looking for


data_list = find_tar_gz_files(base_path, pattern)



column_titles_F3S = [
    'quark', 'model', 'process', 'order',  'YPDG', 'my(GeV)', 
    'coupling_name', 'coupling', 'XPDG', 'mx(GeV)', 'XS', 'CS(pb)', 
    'tag', 'FileExtension'
    ]

column_titles_other = [
    'quark', 'model', 'process', 'order',  'YPDG', 'my(GeV)',  
    'XPDG', 'mx(GeV)', 'coupling_name', 'coupling', 'XS', 'CS(pb)', 
    'tag', 'FileExtension'
    ]


foldername = '/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/c'

models = ['F3S', 'S3M', 'F3V']


def csvwriter(modelname):
    m = modelname
    filename = os.path.join(foldername,"{}_Sigmas.csv".format(m))
    with open(filename, 'w', newline='') as csvfile:

        csvwriter = csv.writer(csvfile)

        # Process each file name in the list
        for i, data in enumerate(data_list):

            if i == 0:
                if 'F3S' in data:
                    csvwriter.writerow(column_titles_F3S)
                else:
                    csvwriter.writerow(column_titles_other)

            data = data.replace("/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/", "")
            data = data.replace(".tar.gz", "")
            if m in data:
                # Split the string by both '/' and '_'
                result = re.split(r'[/_]', data)
                if 'tag' not in result:
                    result.append("")
                    result.append("")

                # Write the list as a row in the CSV file
                csvwriter.writerow(result)
    return 0

csvwriter('F3S')
csvwriter('S3M')
csvwriter('F3V')