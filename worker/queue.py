from queue import Queue

queue = Queue()

def push(item):
    queue.put(item)

def pop():
    return queue.get()
