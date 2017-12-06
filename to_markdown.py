from __future__ import print_function
import html2text
import sys
import os
import re
import urllib


def replace_with_local_picture(mdfile):
    pic_prefix = mdfile.split(".")[0]
    filename = pic_prefix.split("/")[-1]
    answer_id = mdfile.split("_")[1]
    pic_prefix = pic_prefix.replace(filename, answer_id)
    start_tag = re.compile("\!\[\]\(http.*?\)")
    with open(mdfile) as f:
        lines = f.readlines()
    lines = [line.decode('utf-8') for line in lines]
    new_lines = []
    for line in lines:
        url_pos_pairs = [(m.start(), m.end())
                         for m in re.finditer(start_tag, line)]
        for start, end in url_pos_pairs:
            pic_url = line[start+4:end-1]
            pic_filename = "%s_%s" % (pic_prefix, pic_url.split("/")[-1])
            urllib.urlretrieve(pic_url, pic_filename)
            line = line.replace(pic_url, pic_filename.split("/")[-1])
        new_lines.append(line)
    with open(mdfile, 'w') as f:
        f.write(''.join(new_lines).encode("utf-8"))


def convert_file(filename, path=''):
    if filename[-5:] != ".html":
        return
    full_path = os.path.join(path, filename)
    print("file %s is being processed..." % full_path)
    with open(full_path) as f:
        lines = f.readlines()
    markdown = html2text.html2text(''.join(lines).decode('utf-8'))

    md_filename = "%s.md" % full_path.split(".")[0].decode('utf-8')
    with open(md_filename, 'w') as f:
        f.write(markdown.encode('utf-8'))

    if download_picture:
        replace_with_local_picture(md_filename)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("python to_markdown.py html_file")
        sys.exit(-1)
    param = sys.argv[1]
    download_picture = False
    if len(sys.argv) == 3:
        download_picture = True
    if os.path.isfile(param):
        convert_file(param)
        sys.exit(0)

    for root, dirs, filenames in os.walk(param):
        for filename in filenames:
            convert_file(filename, root)
