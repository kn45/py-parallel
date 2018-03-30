#!/usr/bin/env python

import time
from multiprocessing import Pool, Queue, Process


def foo1(pref, inp):
    inp = foo(inp)
    out_queue.put(pref + str(inp))


def foo2(inp):
    out_queue.put('foo2' + str(inp))


def foo(d):
    return 'foo' + str(d)


def consume():
    out_file = open('./output_sample', 'w')
    while True:
        if out_queue.empty():
            time.sleep(2)
        else:
            item = out_queue.get()
            if item == 'ALLDONE':
                break
            else:
                print >> out_file, item
    out_file.close()


class GlobalVar(object):
    def __init__(self):
        self.pref = 'GlobalVar'


out_queue = Queue()

if __name__ == '__main__':
    p_output = Process(target=consume)
    p_output.start()  # start flush
    gv = GlobalVar()

    data = xrange(100)
    my_pool = Pool(processes=4)
    for d in data:
        my_pool.apply_async(foo1, args=(gv.pref, d))
    # my_pool.imap(foo2, data, chunksize=10)  # start produce
    # my_pool.imap(lambda x: foo1(gv.pref, x), data, chunksize=10)  # not work

    my_pool.close()
    my_pool.join()
    out_queue.put('ALLDONE')  # send ending signal after producing done
    p_output.join()
