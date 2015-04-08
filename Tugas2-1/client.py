#!/usr/bin/python

import zmq

alamat = raw_input("Alamat server: ")

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://" + alamat)
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    rate = socket.recv_json()
    print("1 IDR = %s USD" % rate['rate'])
