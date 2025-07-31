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

#============================================================================================
# import socket
# import struct
# from pylsl import StreamInfo, StreamOutlet
# import time
 
# # Setup LSL outlet to send frame numbers
# info = StreamInfo(name='FrameNum', type='Marker', channel_count=1,
#                   channel_format='int32', source_id='msim_frame_01')
# outlet = StreamOutlet(info)
# print("[LSL] Stream outlet created for FrameNum")
 
# # Setup UDP socket to receive frame numbers from D-Lab
# UDP_IP = "192.168.20.45"
# UDP_PORT = 1230
 
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((UDP_IP, UDP_PORT))
# print(f"[UDP] Listening on {UDP_IP}:{UDP_PORT}...")
 
# while True:
#     try:
#         data, addr = sock.recvfrom(1024)
#         fields = struct.unpack_from("=i", data)
#         frame_num = fields[0]
#         print(f"[RECV] Frame: {frame_num}")
 
#         # Send frame number via LSL
#         outlet.push_sample([frame_num])
#         print(f"[LSL] Sent frame number: {frame_num}")
 
#     except Exception as e:
#         print(f"[ERROR] {e}")
#         time.sleep(0.5)

# test.py — listen on 1230, forward to 1231
 
import socket
import struct
 
# 1) Where the simulator is sending its frame numbers
RECV_IP   = "0.0.0.0"    # listen on all interfaces
RECV_PORT = 1230        # port simulator uses
 
# 2) Where *your dashboard* is now listening
DST_IP    = "192.168.20.45"
DST_PORT  = 1231
 
# — Receiver socket —
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((RECV_IP, RECV_PORT))
print(f"[RELAY] Listening for simulator frames on {RECV_IP}:{RECV_PORT}")
 
# — Sender socket —
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
while True:
    data, addr = recv_sock.recvfrom(1024)      # block until a packet arrives
    if len(data) < 4:
        continue
    # unpack the same way your dashboard does:
    frame_num = struct.unpack('<I', data[:4])[0]
    print(f"[RELAY] Got frame {frame_num} from {addr}")
 
    # forward the *exact same* 4-byte payload to dashboard
    send_sock.sendto(data, (DST_IP, DST_PORT))
    # no need to repack—the bytes are already in '<I' format
    print(f"[RELAY] Forwarded frame {frame_num} to {DST_IP}:{DST_PORT}")







# import socket
# import struct
# import time
 
# # ← set this to your dashboard’s IP (or "127.0.0.1" if local)
# UDP_IP   = "192.168.20.45"
# UDP_PORT = 1230
 
# # create a socket (no bind!)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
# frame_num = 0
# print(f"[UDP SEND] Targeting {UDP_IP}:{UDP_PORT}")
# while True:
#     frame_num += 1
#     # pack into 4 bytes little-endian
#     data = struct.pack('<I', frame_num)
#     sock.sendto(data, (UDP_IP, UDP_PORT))
#     print(f"[UDP SEND] Frame → {frame_num}")
#     time.sleep(0.033)   # ~30 Hz; adjust as needed