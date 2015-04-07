import zmq
import time
import json
import httplib

def get_rate(httpConnection, url) :
    print("Mengambil rate...")
    httpConnection.request('GET', url)
    response = httpConnection.getresponse()
    print("Selesai mengambil rate...")
    return json.loads(response.read())

#-----------------------------------------------

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

API_KEY = 'jr-0cf248d7f90998a620d4b77f7c086395'
rate = {}
try:
    httpCon = httplib.HTTPConnection('jsonrates.com')
except:
    print("Tidak bisa membuat koneksi ke jsonrates.com")
    quit()

shouldSleep = True
while True:
    if (shouldSleep):
        time.sleep(5)
    try:
        rate = get_rate(httpCon, '/get/?from=IDR&to=USD&apiKey=' + API_KEY)
        socket.send_json(rate)
        shouldSleep = True
    except:
        print("Gagal mengambil rate")
        shouldSleep = False
