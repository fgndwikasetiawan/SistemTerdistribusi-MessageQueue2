import zmq
import StringIO
import os

os.chdir('C:/Users/Wik/Documents/Kuliah/Sistem Terdistribusi/urgh/output')

context = zmq.Context()
#buat (zmq)socket yang terhubung dengan worker
worker_socket = context.socket(zmq.PULL)
worker_socket.bind('tcp://*:5556')
#buat (zmq)socket yang terhubung dengan ventilator untuk mengirim pesan pekerjaan selesai
ventilator_socket = context.socket(zmq.PUSH)
ventilator_socket.connect('tcp://localhost:5557')

#looping selamanya untuk menerima hasil dari worker
while True:
    #ambil hasil dari worker (kalau ada)
    img_dict = worker_socket.recv_pyobj() #isinya nama file dan data; data tipenya SocketIO
    print("Menerima file %s" % img_dict['nama']) #nama file diakses dengan img_dict['nama']
    #buka file untuk menyimpan gambar
    f = open(img_dict['nama'], 'wb')
    #tulis isi img_dict['data'] ke file
    f.write(img_dict['data'].getvalue()) #karena img_dict['data'] tipenya SocketIO, maka kita harus memanggil getvalue() untuk mendapatkan stringnya
    f.close()
    print("Selesai menyimpan %s" % img_dict['nama'])
    ventilator_socket.send_string("Selesai memproses %s" % img_dict['nama'])
    #selesai menyimpan satu file :)


