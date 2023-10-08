import queue
import time

pq = queue.PriorityQueue()
def set_pq(score):
    global pq
    time_ = time.time()
    pq.put((time_, score))
    return

def get_pq_empty():
    global pq
    return pq.empty()

def get_pq():
    global pq
    return pq.get()