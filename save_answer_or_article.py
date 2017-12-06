from __future__ import print_function
from zhihu_oauth import ZhihuClient
import sys


def save_answer(url):
    answer = client.from_url(url)
    filename = "%s_%s_voteup%s" % (answer.author.name,
                                   answer.id,
                                   answer.voteup_count)
    answer.save(answer.question.title, filename)


def save_article(url):
    aid = url.split("/")[-1]
    article = client.article(int(aid))
    article.save(article.title, "%s_%s" % (article.title, aid))


def main(url):
    if 'question' in url:
        save_answer(url)
    elif 'zhuanlan' in url:
        save_article(url)
    else:
        print("can't recongize url: %s" % url)


if __name__ == '__main__':
    client = ZhihuClient()
    client.load_token('token.pkl')
    if len(sys.argv) < 2:
        print("python save_by_question.py answer_url")
        sys.exit(-1)
    main(sys.argv[1])
