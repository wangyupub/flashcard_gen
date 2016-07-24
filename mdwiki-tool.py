import os
import argparse

EXCLUDED_FILES = set(['navigation.md'])

def generateIndex(folder, output, exclusion = set([])) :
    TITLE_FORMAT = "#{head1}"
    outputName = output + ".md"
    exclusion.add(outputName)
    out = open(os.path.join(folder, outputName), 'w')
    # write the folder name as title
    title = (os.path.basename(os.path.abspath(folder)))
    out.write(TITLE_FORMAT.format(head1 = title))
    out.write("\n")
    # write the links
    for file in os.listdir(folder):
        if file.endswith(".md") and file not in exclusion:
            out.write(_generateLink(file))
            out.write("\n")
    out.close()

def _generateLink(file) :
    LINK_FORMAT = "[{title}]({location})\n"
    name = os.path.splitext(os.path.basename(file))[0]
    return LINK_FORMAT.format(title = name, location = file)

if __name__ == "__main__":
    # define arguments
    parser = argparse.ArgumentParser(description = "Generate index files for wiki")
    parser.add_argument("--indexName", help = "Generated index file name")
    parser.add_argument("--rootDir", help = "Root directory")
    args = parser.parse_args()

    indexName = "index(generated)"
    rootDir = "."
    if (args.indexName):
        indexName = args.indexName
        print "indexName: " + indexName
    if (args.rootDir):
        rootDir = args.rootDir
        print "rootDir: " + rootDir

    # generate index files
    generateIndex(rootDir, indexName, EXCLUDED_FILES)
