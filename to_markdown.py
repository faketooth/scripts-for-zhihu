from __future__ import print_function
import html2text
import sys


if len(sys.argv) < 2:
    print("python to_markdown.py html_file")
    sys.exit(-1)
filename = sys.argv[1]
with open(filename) as f:
    lines = f.readlines()
markdown = html2text.html2text(''.join(lines).decode('utf-8'))

with open("%s.md" % filename.split(".")[0].decode('utf-8'), 'w') as f:
    f.write(markdown.encode('utf-8'))
