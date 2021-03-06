import pandas as pd
import jieba
import os
from multiprocessing import Process, Queue
import re
import time
from collections import Counter
import queue
from numba import jit


database = '/../text/'
database_path = os.getcwd() + database
MAX_PROCESS = 4


def get_wikipedia_dir(path):
    return [dir for dir in os.listdir(path) if dir != '.DS_Store']


def read_wikipedia_rawdata(id, q, dir):
    print("process {} loop for dir: {}".format(id, dir))

    for d in dir:

        for f in os.listdir(database_path + d):
            if '.DS_Store' in f:
                continue
            with open(database_path + d + '/' + f, 'r') as fs:
                print("process {} read file {}/{}".format(id, d, f))
                rawdata = fs.read()
                t1 = time.time()
                words = handle_rawdata(rawdata)
                t2 = time.time()
                print("process {} consume time {}".format(id, (t2 - t1)))

                while(q.full()):
                   time.sleep(0.5)

                q.put(words)
    # q.put('A')


words_count = Counter()
sum_words_count = 0
def count_wikipedia_rawdata(q):
    global words_count
    global sum_words_count
    while(True):
        # blocking with 30 until get q message
        try:
            t1 = time.time()
            rawdata = q.get(True, 10)

            sum_words_count = sum_words_count + len(rawdata)
            cur_count = Counter(rawdata)
            # words_count = words_count + cur_count
            words_count.update(cur_count)
            t2 = time.time()
            print("consume time {}".format(t2 - t1))
            print("sum words count %ld" % sum_words_count)
            print(words_count.most_common(10))
        except queue.Empty:
            print("-----------can't get rawdata from queue, exit")
            break

    # sum words count 75175309
    print("----------start testing probability")
    # 3.9884478889479566e-54
    print(one_gram_prob("今天晚上请你吃大餐，我们一起吃日料"))
    # 3.7073787613579593e-28
    print(one_gram_prob("这是一个关于维基百科的语言模型测试"))


def to_chunks(pat):
    ret = []
    for p in pat:
        if not isinstance(p, list):
            ret.append(p)
            continue
        for s in p:
            ret.append(s)
    return ret


def handle_rawdata(rawdata):
    raw = []

    # remove <doc> header and '\n'
    raw = [data for data in rawdata.split("\n") if data and re.match('(<doc)|(<\/doc>)', data) == None]

    # remove symbol like ','
    pattern = re.compile('[\w|\d]+')
    raw = [pattern.findall(r) for r in raw]

    raw = to_chunks(raw)

    # print(raw[:100])
    # jieba too slow
    words = [list(jieba.cut(r)) for r in raw]
    # print(words[:20])
    return to_chunks(words)


def cut(string):
    return list(jieba.cut(string))


def one_gram_prob(sentence):
    global words_count
    global sum_words_count
    prob = 1
    word = cut(sentence)
    for w in word:
        if words_count[w]:
            prob *= words_count[w] / sum_words_count
        else:
            prob *= 1 / sum_words_count
    return prob


def start(path):

    dir = get_wikipedia_dir(path)
    print(dir)


    process_num = MAX_PROCESS
    if len(dir) < process_num:
        process_num = len(dir)
    else:
        total_dir = []
        for i in range(MAX_PROCESS):
            dir_slice = []
            for j in range(len(dir)):
                if j % MAX_PROCESS == i:
                    dir_slice.append(dir[j])
            total_dir.append(dir_slice)


    process_list = [0] * process_num
    rawdata_q = Queue(2 * MAX_PROCESS)

    # start a process to count data after jieba
    count_process = Process(target=count_wikipedia_rawdata, args=(rawdata_q,))
    count_process.start()

    for i in range(process_num):
        # process_num[i] = Process(target=read_wikipedia_rawdata, args=(rawdata_q,))
        process_list[i] = Process(target=read_wikipedia_rawdata, args=(i, rawdata_q, total_dir[i]))
        process_list[i].start()

    for i in range(process_num):
        process_list[i].join()

    count_process.join()

    # read finished, write to file
    # global words_count
    # print("----------All process finished, write words_count to file")
    # with open('wikipedia_count.txt', 'w') as fs:
    #     for k, v in words_count.items():
    #         fs.write(f'{k} {v}\n')


def single_process_start(path):
    global words_count
    global sum_words_count
    dir = get_wikipedia_dir(path)
    print(dir)

    # jieba.enable_parallel()

    for d in dir:
        for f in os.listdir(database_path + d):
            if '.DS_Store' in f:
                continue
            with open(database_path + d + '/' + f, 'r') as fs:
                data = fs.read()
                rawdata = handle_rawdata(data)

                sum_words_count = sum_words_count + len(rawdata)
                cur_count = Counter(rawdata)
                # words_count = words_count + cur_count
                words_count.update(cur_count)
                print("sum words count %ld" % sum_words_count)
                print(words_count.most_common(10))

    print("----------start testing probability")
    # 3.9884478889479566e-54
    print(one_gram_prob("今天晚上请你吃大餐，我们一起吃日料"))
    # 3.7073787613579593e-28
    print(one_gram_prob("这是一个关于维基百科的语言模型测试"))


start(database_path)

#single_process_start(database_path)

