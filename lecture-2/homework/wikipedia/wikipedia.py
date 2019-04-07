import pandas as pd
import jieba
import os
from multiprocessing import Process, Queue
import re
import time


database = '/../text/'
database_path = os.getcwd() + database
MAX_PROCESS = 4

print(database_path)


def get_wikipedia_dir(path):
    return [dir for dir in os.listdir(path) if dir != '.DS_Store']


print(get_wikipedia_dir(database_path))


def read_wikipedia_rawdata(id, q, dir):
    print("process {} loop for dir: {}".format(id, dir))
    for d in dir:
        for f in os.listdir(database_path + d):
            with open(database_path + d + '/' + f, 'r') as fs:
                print("process {} read file {}/{}".format(id, d, f))
                rawdata = fs.read()
                words = handle_rawdata(rawdata)

                while(q.full()):
                   time.sleep(0.5)

                q.put(words)
    # q.put('A')


def cut_wikipedia_rawddata(q):
    while(True):
        # blocking until get q message
        rawdata = q.get(True)
        print(rawdata[:10])


def handle_rawdata(rawdata):
    # remove '\n' and <doc id=.... and </doc>
    raw = [data for data in rawdata.split("\n") if data and re.match('(<doc)|(<\/doc>)', data) == None]

    # print(raw[:100])
    words = [list(jieba.cut(r)) for r in raw]
    # print(words[:100])
    return words



def start(path):

    dir = get_wikipedia_dir(path)

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

    # start a process to cut rawdata and counter it
    cut_process = Process(target=cut_wikipedia_rawddata, args=(rawdata_q,))
    cut_process.start()

    for i in range(process_num):
        # process_num[i] = Process(target=read_wikipedia_rawdata, args=(rawdata_q,))
        process_list[i] = Process(target=read_wikipedia_rawdata, args=(i, rawdata_q, total_dir[i]))
        process_list[i].start()


    for i in range(process_num):
        process_list[i].join()

    #cut_process.terminate()


# with open(database_path + 'AC/wiki_73', 'r') as f:
#     rawdata = f.read()
#     raw = [data for data in rawdata.split("\n") if data and re.match('(<doc)|(<\/doc>)', data) == None]
#     # print(raw[:100])
#     words = [list(jieba.cut(r)) for r in raw]
#     # print(words[:100])

start(database_path)
