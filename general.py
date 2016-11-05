import os

# Each website crawled is a separate folder

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

#create_project_dir('Webcrawler')

# create queue and crawled files

def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt' # queue of links to be crawled and data to be entered in queue.txt
    crawled = project_name + '/crawled.txt' # already crawled links, relative path
    if not os.path.isfile(queue):
        write_file(queue, base_url) # writing to the file the data, shouldn't start empty
    if not os.path.isfile(crawled):
        write_file(crawled, '') # starts with nothing crawled

# create new file
def write_file(path,data):
    f = open(path,'w')       # 'w' for write mode,
    f.write(data)
    f.close()           # recommend to save space

#test
# create_data_files('Webcrawler','https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher')

# add data onto existing file

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# delete contents of a file

def delete_file_contents(path):
    with open(path, 'w'):
        pass        #overwriting existing with pass keyword that does nothing


# working with data: stored in set, unique elements so that same urls are not added again and crawled!
# Periodically saved to file

# Read a file and convert to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', '')) # removing newlines added on append
    return results

# Iterate through set,each item is new line in file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file,link)
