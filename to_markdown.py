from __future__ import print_function
import html2text
import sys
import os


def convert_file(filename, path=''):
    if filename[-5:] != ".html":
        return
    full_path = os.path.join(path, filename)
    print("file %s is being processed..." % full_path)
    with open(full_path) as f:
        lines = f.readlines()
    markdown = html2text.html2text(''.join(lines).decode('utf-8'))

    with open("%s.md" % full_path.split(".")[0].decode('utf-8'), 'w') as f:
        f.write(markdown.encode('utf-8'))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("python to_markdown.py html_file")
        sys.exit(-1)
    param = sys.argv[1]
    if os.path.isfile(param):
        convert_file(param)
        sys.exit(0)

    for root, dirs, filenames in os.walk(param):
        for filename in filenames:
            convert_file(filename, path)
