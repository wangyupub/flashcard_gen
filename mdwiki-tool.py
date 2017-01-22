import os
import argparse
import hashlib
import logging

EXCLUDED_FILES = set(['navigation.md', 'pages', 'images', 'index(generated).md'])
LOG = logging.getLogger('mdwiki-tool')
LOG.setLevel(logging.INFO)
def generateIndex(folder, output_filename, exclusion, depth) :
    next_depth = depth
    if depth:
        print("depth: " + str(depth))
        if depth < 1:
            return
        next_depth = depth - 1

    # default case: no file exist, then update hash and create file
    mode = "write"
    update_hash = True

    output_pathname = os.path.join(folder, output_filename)
    hash_pathname = os.path.join(folder, output_filename + ".md5")

    file_exist = os.path.exists(output_pathname)
    
    if file_exist:
        print("file " + output_pathname + " exist in " + folder + "\n")
        hash_exist = os.path.exists(hash_pathname)
        if hash_exist:
            print("file " + hash_pathname + " exist in " + folder + "\n")
            calculated_hash = _md5(output_pathname)
            with open(hash_pathname) as hash_file:
                saved_hash = hash_file.read()
                # file changed since last save, append mode
                # do not update hash to disallow future overwriting
                if saved_hash != calculated_hash:
                    mode = "append"
                    update_hash = False
                # file has not changed, overwrite
                else:
                    mode = "write"

        # hash does not exist, need to verify file content
        else:
            mode = "verify"

    content, subdirectory_list = _process_directory(folder, exclusion, output_filename)

    if mode == "verify":
        with open(output_pathname) as output_file:
            saved_content = output_file.read()
            # file not changed, overwrite
            if content == saved_content:
                mode = "write"
            # file changed, no future ovewriting
            else:
                mode = "append"
                update_hash = False

    print("file mode: " + mode)
    out = open(output_pathname, mode[0])
    if mode == "append":
        print("File: " + output_pathname + " requires manual update")
        out.write("(__generated content below__)\n")
    out.write(content)
    out.close()
    if update_hash:
        hash_ = open(hash_pathname, 'w')
        hash_.write(_md5(output_pathname))
        hash_.close()
        
    for subdirectory in subdirectory_list:
        generateIndex(subdirectory, output_filename, exclusion, next_depth)


# _process_directory: process the given directory
# returns:
# 1. a generated content string
# 2. a list of the sub directory for further process
def _process_directory(folder, exclusion, output_filename):
    TITLE_FORMAT = "#{head1}"
    subdirectory_list = []
    # write the folder name as title
    title = (os.path.basename(os.path.abspath(folder)))
    content = TITLE_FORMAT.format(head1 = title) + "\n"
    # out.write(TITLE_FORMAT.format(head1 = title))
    # out.write("\n")
    print("writing title: " + title)
    # write the links
    print("reading folder: " + folder)
    for file in os.listdir(folder):
        print("file: " + file)
        if file not in exclusion:
            filePath = os.path.join(folder, file)
            if os.path.isfile(filePath) and file.endswith(".md"):
                content += _generateLink(file)
                # out.write(_generateLink(file))
                print("writing file link: " + file)
            if os.path.isdir(filePath):
                content += _getFolderLink(file, output_filename)
                # out.write(_getFolderLink(file, outputName))
                print("writing dir link: " + file)
                subdirectory_list.append(filePath)
                # generateIndex(filePath, output, exclusion, depth)
            # out.write("\n")
            content += "\n"
    return content, subdirectory_list

def _generateLink(file):
    LINK_FORMAT = "[{title}]({location})\n"
    name = os.path.splitext(os.path.basename(file))[0]
    return LINK_FORMAT.format(title = _normalize(name), location = file)

def _getFolderLink(dir, indexName):
    LINK_FORMAT = "[{title}]({location}/{index})\n"
    name = dir
    return LINK_FORMAT.format(title = _normalize(name), location = dir, index = indexName)

def _md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _normalize(name):
    SPECIAL_CHARS = "_#*"
    for c in SPECIAL_CHARS:
        name = name.replace(c, "\\" + c)
    return name

if __name__ == "__main__":
    # define arguments
    parser = argparse.ArgumentParser(description = "Generate index files for wiki")
    parser.add_argument("--indexName", help = "Generated index file name")
    parser.add_argument("--rootDir", help = "Root directory")
    parser.add_argument("--depth", type = int, help = "Max level of directories to process")
    parser.add_argument("--smartAppend", action="store_true", help = "Append to existing index file")
    args = parser.parse_args()

    indexName = "index(generated)"
    rootDir = "."
    depth = None
    
    if (args.indexName):
        indexName = args.indexName
        print("indexName: " + indexName)
    if (args.rootDir):
        rootDir = args.rootDir
        print("rootDir: " + rootDir)
    if (args.depth):
        depth = args.depth

    file_name = indexName + ".md"
    hash_name = indexName + ".md5"
    EXCLUDED_FILES.add(file_name)
    EXCLUDED_FILES.add(hash_name)
        
    # generate index files
    generateIndex(rootDir, file_name, EXCLUDED_FILES, depth)
