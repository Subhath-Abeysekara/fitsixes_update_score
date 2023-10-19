import queue
import time

pq = queue.PriorityQueue()
movements = []
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

def next_move_no(id):
    global movements
    filter_key = "id"
    filter_value = id
    filtered_data = [d for d in movements if d.get(filter_key) == filter_value]
    print(filtered_data)
    sort_key = "no"
    sorted_data = sorted(filtered_data, key=lambda x: x[sort_key])
    if sorted_data != []:
        last_no = sorted_data.pop()['no']
    else:
        last_no = 0
    return last_no+1

def last_move_get(id):
    global movements
    filter_key = "id"
    filter_value = id
    filtered_data = [d for d in movements if d.get(filter_key) == filter_value]
    other_data = [d for d in movements if d.get(filter_key) != filter_value]
    sort_key = "no"
    sorted_data = sorted(filtered_data, key=lambda x: x[sort_key])
    data =  sorted_data.pop()
    for move in sorted_data:
        other_data.append(move)
    movements = other_data
    return data
def set_movement(move):
    global movements
    move['no'] = next_move_no(move['id'])
    movements.append(move)
    return
def get_movement_empty(id):
    global movements
    filter_key = "id"
    filter_value = id
    filtered_data = [d for d in movements if d.get(filter_key) == filter_value]
    sort_key = "no"
    sorted_data = sorted(filtered_data, key=lambda x: x[sort_key])
    if sorted_data == []:
        return True
    return False

def get_movement(id):
    global movements
    last_move = last_move_get(id)
    return last_move