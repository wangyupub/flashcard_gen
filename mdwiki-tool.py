import os

EXCLUDED_FILES = set(['navigation.md'])

def generateIndex(folder, output = "index(generated).md", exclusion = set([])) :
    TITLE_FORMAT = "#{head1}"
    exclusion.add(output)
    out = open(output, 'w')
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
    generateIndex(".", exclusion = EXCLUDED_FILES)
