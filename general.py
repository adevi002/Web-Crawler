import os           #allows us to create directories

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

# Create queue and crawled files if not created already
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'         # when link found on website, adds it to this queue file (waitlist)
    crawled = project_name + '/crawled.txt'     # once a link page is crawled, it will be added to this crawled file
    if not os.path.isfile(queue):               #checks if file exists already
        write_file(queue, base_url)
    else:
        open(queue, 'w').close()
    if not os.path.isfile(crawled):             #checks if file exists already
        write_file(crawled, '')
    else:
        open(crawled, 'w').close()

# Creates a new file
def write_file(path, data):
    f = open(path, 'w')                 #allows for writing to opened file
    f.write(data)
    f.close()

# Adds data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:       #allows us to append data to opened file
        file.write(data + '\n')

# Deletes the contents of a file
def delete_file_contents(path):         # creates new file with same name but with no content, replacing the original file of same name
    with open(path, 'w'):
        pass                            # do nothing
    # open(path, 'w').close()

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:        # f refers to file being read
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)          # saves data set to file so data is not lost