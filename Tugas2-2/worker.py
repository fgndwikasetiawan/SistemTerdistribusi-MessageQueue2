__author__ = 'Wik'

import zmq
import os
from PIL import Image
import StringIO

def get_format(filename):
    img_format = filename[filename.rfind('.')+1:].upper()
    if (img_format == 'JPG'):
        img_format = 'JPEG'
    return img_format

context = zmq.Context()
ventilator_socket = context.socket(zmq.PULL)
ventilator_socket.connect('tcp://localhost:5555')
sink_socket = context.socket(zmq.PUSH)
sink_socket.connect('tcp://localhost:5556')

while True:
    img_dict = ventilator_socket.recv_pyobj();
    print("Menerima file %s, mulai mengkonversi..." % img_dict['nama'])
    try:
        img_format = get_format(img_dict['nama'])
        img = Image.open(img_dict['data'])
        img = img.convert('L')
        data = StringIO.StringIO()
        img.save(data,img_format)
        img_dict['data'] = data
        print("Konversi selesai, mengirim...")
        sink_socket.send_pyobj(img_dict)
        print("Pengiriman file %s selesai" % img_dict['nama'])
    except Exception as e:
        print("Error! %s" % e)