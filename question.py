from __future__ import print_function
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import GetDataErrorException
import sys
import time
import random
import os


def get_cache(dir):
    cache_file = os.path.join(dir, 'cache')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            lines = f.readlines()
        return set([int(line) for line in lines])
    os.mkdir(dir)
    return set()


def main(question_id):
    if question_id[:4] == 'http':
        question_id = question_id.split("/")[-1]
    question = client.question(int(question_id))
    print("start to save answers of {}".format(question.title.encode('utf-8')))

    answer_cache = get_cache(question.title)
    cache_file = open(os.path.join(question.title, 'cache'), 'a')
    print("consinder {} of {} answers have been saved.".format(
        len(answer_cache), question.answer_count))
    for answer in question.answers:
        if answer.id in answer_cache:
            print("%s's answer has been saved." % answer.author.name)
            time.sleep(1)
            continue
        print(answer.author.name, answer.id, answer.voteup_count)
        filename = "%s_%s_voteup%s" % (answer.author.name,
                                       answer.id,
                                       answer.voteup_count)
        try:
            answer.save(question.title, filename)
        except GetDataErrorException:
            client.login()
            answer.save(question.title, filename)
        cache_file.write("%s\n" % answer.id)
        cache_file.flush()
        answer_cache.add(answer.id)
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)
    cache_file.close()


if __name__ == '__main__':
    client = ZhihuClient()
    client.load_token('token.pkl')
    if len(sys.argv) < 2:
        print("python save_by_question.py question_id")
        sys.exit(-1)
    main(sys.argv[1])
