'''
Turn a list into a binary tree made of tuples.
Module has multiple implementations.
For small lists the overhead of a queue doesn't improve performance.
'''

import json
from queue import Queue


def using_list(values):
    return using_list_inplace(values.copy())


def using_list_inplace(values):
    while len(values) > 1:
        pair = (values.pop(0), values.pop(0))
        values.append(pair)
    return values[0]


def using_queue(values):
    queue = Queue()
    for x in values:
        queue.put(x)
    while queue.qsize() > 1:
        pair = (queue.get(), queue.get())
        queue.put(pair)
    return queue.get()


if __name__ == '__main__':
    values = [x for x in range(0, 5)]
    tree = using_list(values)
    print('List:', values)
    print('Tree:', tree)
    print('Pretty:')
    print(json.dumps(tree, indent=4))