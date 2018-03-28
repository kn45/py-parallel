#!/usr/bin/env python

import time
from multiprocessing import Pool, Queue, Process


def foo(inp):
    out_queue.put('foo_' + str(inp))


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


out_queue = Queue()

if __name__ == '__main__':
    p_output = Process(target=consume, args=())
    p_output.start()  # start flush

    data = xrange(10000)
    my_pool = Pool(processes=4)
    my_pool.imap(foo, data, chunksize=10)  # start produce

    my_pool.close()
    my_pool.join()
    out_queue.put('ALLDONE')  # send ending signal after producing done
    p_output.join()
