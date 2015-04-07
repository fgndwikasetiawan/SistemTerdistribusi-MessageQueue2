import zmq
import StringIO
import os

os.chdir('C:/Users/Wik/Documents/Kuliah/Sistem Terdistribusi/urgh/output')

context = zmq.Context()
worker_socket = context.socket(zmq.PULL)
worker_socket.bind('tcp://*:5556')

while True:
    img_dict = worker_socket.recv_pyobj()
    print("Menerima file %s" % img_dict['nama'])
    f = open(img_dict['nama'], 'wb')
    f.write(img_dict['data'].getvalue())
    f.close()
    print("Selesai menyimpan %s" % img_dict['nama'])


