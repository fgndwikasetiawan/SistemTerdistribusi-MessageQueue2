import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    rate = socket.recv_json()
    print("1 IDR = %s USD" % rate['rate'])