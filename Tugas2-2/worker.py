#!/usr/bin/python

import zmq
import os
from PIL import Image
import StringIO

#fungsi untuk mengambil format gambar dari suatu file
#--format gambar dilihat dari ekstensinya (.png, .jpg, dan lain-lain)
def get_format(filename):
    img_format = filename[filename.rfind('.')+1:].upper()
    if (img_format == 'JPG'):
        img_format = 'JPEG'
    return img_format

context = zmq.Context()
#agar dapat menerima task, buat (zmq)socket yang terhubung ke ventilator
ventilator_socket = context.socket(zmq.PULL)
ventilator_socket.connect('tcp://localhost:5555')
#hasil pemrosesan akan diberikan ke sink, maka buat (zmq)socket yang terhubung ke sink
sink_socket = context.socket(zmq.PUSH)
sink_socket.connect('tcp://localhost:5556')

#infinite loop! worker senantiasa menunggu kerjaan
while True:
    #terima data gambar (dan nama file gambar) yang bertipe dictionary dari ventilator
    #img_dict mempunyai dua elemen yang diakses dengan img_dict['nama'] dan img_dict['data']
    #img_dict['nama'] adalah nama file gambar, sedangkan img_dict['data'] adalah objek StringIO yang menyimpan data gambar
    img_dict = ventilator_socket.recv_pyobj();
    print("Menerima file %s, mulai mengkonversi..." % img_dict['nama'])
    try:
        #ambil format gambar
        img_format = get_format(img_dict['nama'])
        #baca data gambar dari img_dict['data']
        img = Image.open(img_dict['data'])
        #convert ke grayscale
        img = img.convert('L')
        #simpan data gambar yang baru tersebut ke img_dict['data']
        data = StringIO.StringIO()
        img.save(data, img_format)
        img_dict['data'] = data
        print("Konversi selesai, mengirim...")
        #kirim ke sink
        sink_socket.send_pyobj(img_dict)
        print("Pengiriman file %s selesai" % img_dict['nama'])
    except Exception as e:
        print("Error! %s" % e)
        #selesai memproses satu gambar :)
