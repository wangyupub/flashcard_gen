import os
import argparse

EXCLUDED_FILES = set(['navigation.md'])

def generateIndex(folder, output, exclusion, depth) :
    if depth:
        print "depth: " + str(depth)
        if depth < 1:
            return
        depth -= 1


    TITLE_FORMAT = "#{head1}"
    outputName = output + ".md"
    exclusion.add(outputName)
    out = open(os.path.join(folder, outputName), 'w')
    # write the folder name as title
    title = (os.path.basename(os.path.abspath(folder)))
    out.write(TITLE_FORMAT.format(head1 = title))
    out.write("\n")
    print "writing title: " + title
    # write the links
    print "reading folder: " + folder
    for file in os.listdir(folder):
        print "file: " + file
        if file not in exclusion:
            filePath = os.path.join(folder, file)
            if os.path.isfile(filePath) and file.endswith(".md"):
                out.write(_generateLink(file))
                print "writing file: " + file
            if os.path.isdir(filePath):
                out.write(_getFolderLink(file, outputName))
                print "writing dir: " + file
                generateIndex(filePath, output, exclusion, depth)
            out.write("\n")
    out.close()

def _generateLink(file):
    LINK_FORMAT = "[{title}]({location})\n"
    name = os.path.splitext(os.path.basename(file))[0]
    return LINK_FORMAT.format(title = name, location = file)

def _getFolderLink(dir, indexName):
    LINK_FORMAT = "[{title}]({location}/{index})\n"
    name = dir
    return LINK_FORMAT.format(title = name, location = dir, index = indexName)

if __name__ == "__main__":
    # define arguments
    parser = argparse.ArgumentParser(description = "Generate index files for wiki")
    parser.add_argument("--indexName", help = "Generated index file name")
    parser.add_argument("--rootDir", help = "Root directory")
    parser.add_argument("--depth", type = int, help = "Max level of directories to process")
    args = parser.parse_args()

    indexName = "index(generated)"
    rootDir = "."
    depth = None

    if (args.indexName):
        indexName = args.indexName
        print "indexName: " + indexName
    if (args.rootDir):
        rootDir = args.rootDir
        print "rootDir: " + rootDir
    if (args.depth):
        depth = args.depth

    # generate index files
    generateIndex(rootDir, indexName, EXCLUDED_FILES, depth)
