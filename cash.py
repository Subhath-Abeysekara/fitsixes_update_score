import queue
import time

pq = queue.PriorityQueue()
movements = queue.PriorityQueue()
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
    return pq.get()[1]

# ******** Movements *******

def set_movement(move):
    global movements
    time_ = time.time()
    movements.put((time_, move))
    return

def get_movement_empty():
    global movements
    return movements.empty()

def get_movement(id):
    global movements
    moves = []
    while True:
        move = movements.get()
        if move[1]['id'] == id:
            for i in moves[::-1]:
                set_movement(i)
            return move[1]
        else:
            moves.append(move)