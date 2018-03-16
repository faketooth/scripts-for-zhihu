from __future__ import print_function
from zhihu_oauth import ZhihuClient
import sys
import time


if __name__ == '__main__':
    client = ZhihuClient()
    client.load_token('token.pkl')
    if len(sys.argv) != 3:
        print("python people <url|pid> <article|answer>")
        sys.exit(-1)
    pid = sys.argv[1]
    if pid[:4] == "http":
        pid = pid.split("/")[4]
    people = client.people(pid)

    task = sys.argv[2]
    print('start to process %s' % people.name)
    if task == 'article':
        for article in people.articles:
            article.save("%s_%s" % (people.name, 'article'),
                         "%s_%s" % (article.title, article._id))
            print("article %s has been saved." % article.title)
            time.sleep(1)
    if task == 'answer':
        for answer in people.answers:
            answer.save("%s_%s" % (people.name, 'answer'),
                        "%s_%s_%s" % (answer.id,
                                      answer.question.title,
                                      answer.voteup_count))
            print("answer %s has been saved." % answer.question.title)
            time.sleep(1)
