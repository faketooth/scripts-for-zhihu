from __future__ import print_function
from zhihu_oauth import ZhihuClient
import sys
import time
import random

def main(url):
    if url[:4] == 'http':
        answer = client.from_url(url)
    else:
        answer = client.answer(url)
    filename = "%s_%s_%s" % (answer.author.name, answer.id, answer.voteup_count)
    answer.save(answer.question.title, filename)



if __name__ == '__main__':
    client = ZhihuClient()
    client.load_token('token.pkl')
    if len(sys.argv)<2:
        print("python save_by_question.py answer_url")
        sys.exit(-1)
    main(sys.argv[1])
