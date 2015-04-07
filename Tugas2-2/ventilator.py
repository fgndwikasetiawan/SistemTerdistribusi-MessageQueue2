import zmq
import os
from PIL import Image
import StringIO

os.chdir('C:/Users/Wik/Documents/Kuliah/Sistem Terdistribusi/urgh/sister dataset(1)')
context = zmq.Context()
#buat (zmq)socket yang terhubung ke worker
worker_socket = context.socket(zmq.PUSH)
worker_socket.bind('tcp://*:5555')
#buat (zmq)socket yang terhubung ke sink
sink = context.socket(zmq.PUSH)
sink.connect('tcp://localhost:5556')

#ambil daftar nama gambar
list_file = os.listdir(os.getcwd())

#biar gak langsung mencolot
print("Tekan ENTER untuk memulai")
raw_input()
print("Mulai mengirim task ke worker")

i = 1 #index
#looping pengiriman file, satu iterasi satu file
for file in list_file:
    print("Mengirim task #%d" % i)
    data = StringIO.StringIO(open(file, 'rb').read())
    img_dict = {'nama': file, 'data': data}
    worker_socket.send_pyobj(img_dict)
    i += 1

#selesai :)
print("Selesai mengirim task")
