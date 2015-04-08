import zmq
import os
from PIL import Image
import StringIO
import time

os.chdir('C:/Users/Wik/Documents/Kuliah/Sistem Terdistribusi/urgh/sister dataset(1)')
context = zmq.Context()
#buat (zmq)socket yang terhubung ke worker
worker_socket = context.socket(zmq.PUSH)
worker_socket.bind('tcp://*:5555')
#(zmq)socket yang terhubung dengan sink untuk menerima pesan pekerjaan selesai
sink_socket = context.socket(zmq.PULL)
sink_socket.bind('tcp://*:5557')

#ambil daftar nama gambar
list_file = os.listdir(os.getcwd())

#biar gak langsung mencolot
print("Tekan ENTER untuk memulai")
raw_input()
print("Mulai mengirim task ke worker")

start_time = time.time()

i = 1 #index
#looping pengiriman file, satu iterasi satu file
for file in list_file:
    print("Mengirim task #%d" % i)
    data = StringIO.StringIO(open(file, 'rb').read())
    img_dict = {'nama': file, 'data': data}
    worker_socket.send_pyobj(img_dict)
    i += 1
print("Selesai mengirim task, menunggu hasil...")
#selesai mengirim, sekarang terima pesan selesai dari sink
for file in list_file:
    msg = sink_socket.recv_string()
    print(msg)
#selesai :)
print("Semua file telah terproses! Waktu: %f" % (time.time() - start_time))
raw_input()