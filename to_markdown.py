from __future__ import print_function
import html2text
import sys
import os
import re
import urllib.request
import traceback


def replace_with_local_picture(mdfile):
    try:
        basename = os.path.basename(mdfile)
        basedir = os.path.dirname(mdfile)
        answer_id = basename.split("_")[0]
        pic_prefix = os.path.join(basedir, answer_id)
    except Exception as e:
        print("Failed to process %s with error msg: %s" % (mdfile, e))
        failed_file_list.append(mdfile)
        traceback.print_exc()
        return
    start_tag = re.compile("\!\[\]\(http.*?\)")
    with open(mdfile) as f:
        lines = f.readlines()
    lines = [line for line in lines]
    new_lines = []
    for line in lines:
        while 1:
            url_pos_pairs = [(m.start(), m.end())
                             for m in re.finditer(start_tag, line)]
            if len(url_pos_pairs) == 0:
                break
            start, end = url_pos_pairs[0]
            pic_url = line[start+4:end-1]
            pic_filename = "%s_%s" % (pic_prefix, pic_url.split("/")[-1])
            try:
                urllib.request.urlretrieve(pic_url, pic_filename)
            except Exception as e:
                print(e, pic_url)
                break
            line = line.replace(line[start:end],
                                "![](%s)" % pic_filename.split("/")[-1])
        new_lines.append(line)
    with open(mdfile, 'w') as f:
        f.write(''.join(new_lines))


def convert_file(filename, path=''):
    if filename[-5:] != ".html":
        return
    full_path = os.path.join(path, filename)
    print("file %s is being processed..." % full_path)
    with open(full_path) as f:
        lines = f.readlines()
    markdown = html2text.html2text(''.join(lines))

    md_filename = "%s.md" % full_path[:-5]
    if os.path.exists(md_filename):
        print("%s has been converted to markdown file. Skip it." % filename)
        if download_picture:
            replace_with_local_picture(md_filename)
        return
    with open(md_filename, 'w') as f:
        f.write(markdown)

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
    failed_file_list = []
    for root, dirs, filenames in os.walk(param):
        for filename in filenames:
            convert_file(filename, root)
    if len(failed_file_list) != 0:
        print("\n\nAll files below failed to download pictures.")
        print("\n".join(failed_file_list))
