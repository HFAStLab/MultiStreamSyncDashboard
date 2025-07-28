# import socket
# import struct
# import pandas as pd

# #Listens to SCC_Custom2
# ##SCC_Custom2 == i -> send task_i -> SCC_Custom1

# UDP_IP = "192.168.20.45"
# UDP_PORT = 1230


# sock_listen = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock_listen.bind((UDP_IP, UDP_PORT))## listens to port 1230 FrameNo
# print("hi")
# while True:
#     print("*")

#     data, addr = sock_listen.recvfrom (1024)
#     fields = struct.unpack_from("=i", data)
#     recv_data = fields [0]
#     print ("received message: " , data)
#     print (fields[0])


import socket
import struct
from pylsl import StreamInfo, StreamOutlet
import time
 
# Setup LSL outlet to send frame numbers
info = StreamInfo(name='FrameNum', type='Marker', channel_count=1,
                  channel_format='int32', source_id='msim_frame_01')
outlet = StreamOutlet(info)
print("[LSL] Stream outlet created for FrameNum")
 
# Setup UDP socket to receive frame numbers from D-Lab
UDP_IP = "192.168.20.45"
UDP_PORT = 1230
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}...")
 
while True:
    try:
        data, addr = sock.recvfrom(1024)
        fields = struct.unpack_from("=i", data)
        frame_num = fields[0]
        print(f"[RECV] Frame: {frame_num}")
 
        # Send frame number via LSL
        outlet.push_sample([frame_num])
        print(f"[LSL] Sent frame number: {frame_num}")
 
    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(0.5)