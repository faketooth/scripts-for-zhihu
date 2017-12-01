from __future__ import print_function
from zhihu_oauth import ZhihuClient
import sys
import time
import random

def main(question_id):
    question = client.question(int(question_id))
    print("start to save answers of {}".format(question.title.encode('utf-8')))

    answer_cache = set()
    for answer in question.answers:
        if answer.id in answer_cache:
            continue
        print(answer.author.name, answer.voteup_count)
        filename = "%s_%s" % (answer.author.name, answer.id)
        try:
            answer.save(question.title, filename)
        except GetDataErrorException:
            client.login()
        answer_cache.add(answer.id)
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)



if __name__ == '__main__':
    client = ZhihuClient()
    client.load_token('token.pkl')
    if len(sys.argv)<2:
        print("python save_by_question.py question_id")
        sys.exit(-1)
    main(sys.argv[1])
