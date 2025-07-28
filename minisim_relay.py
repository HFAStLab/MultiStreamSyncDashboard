# # minisim_relay.py  --------------------------------------------
# # 1. Opens a UDP or TCP socket to miniSim (replace IP & PORT)
# # 2. Pushes each received packet into an LSL stream called
# #    "miniSim_Frame" (type "Marker", 1 channel, irregular)
 
# import socket, struct, argparse
# from pylsl import StreamInfo, StreamOutlet

 
# def main(ip: str, port: int, proto: str):
#     # ---- create LSL outlet -----------------------------------
#     info = StreamInfo(name="miniSim_Frame",
#                       type="Marker",
#                       channel_count=1,
#                       nominal_srate=0,          # irregular/event
#                       channel_format="int32",
#                       source_id="msim_relay_01")
#     outlet = StreamOutlet(info)
 
#     # ---- open socket to miniSim ------------------------------
#     sock_type = socket.SOCK_DGRAM if proto == "udp" else socket.SOCK_STREAM
#     # sock = socket.socket(socket.AF_INET, sock_type)
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(("", port))   # listen on all interfaces, port 1230
#     print(f"[relay] Listening for miniSim on UDP port {port}")
#     sock.connect((ip, port))
#     print(f"[relay] Connected to miniSim {ip}:{port} via {proto.upper()}")
 
#     while True:
#         if proto =="udp":
#             pkt, _ = sock.recvfrom(1024)
#             print(f"[relay] Raw Packet ({len(pkt)} bytes): {pkt!r}")
#             if len(pkt) < 4:
#                 print("[relay] Warning: packet too small to unpack frame number")
#                 continue
#         else:
#             pkt = sock.recv(1024)
#             print(f"[relay] Raw TCP Packet ({len(pkt)} bytes): {pkt!r}")
#             if not pkt:
#                 break
        
        
#         frame, = struct.unpack('<I', pkt[:4])
#         print(f"[relay] Parsed frame: {frame}")
#         outlet.push_sample([frame])  # PC-clock timestamp added automatically
 
# if __name__ == "__main__":
#     p = argparse.ArgumentParser()
#     p.add_argument("--ip",   required=True, help="miniSim IP")
#     p.add_argument("--port", type=int, required=True, help="miniSim port")
#     p.add_argument("--proto", choices=["udp","tcp"], default="udp")
#     args = p.parse_args()
#     main(args.ip, args.port, args.proto)

# # ip  192.168.20.45
# # port = 1230
# # python minisim_relay.py --ip 192.168.20.45 --port 1230 --proto udp






import socket
import struct
import argparse
from pylsl import StreamInfo, StreamOutlet
 
 
def main(ip: str, port: int, proto: str):
    # ---- create LSL outlets --------------------------------
    # Frame number stream (int32)
    info_frame = StreamInfo(name="FrameNum",
                             type="Marker",
                             channel_count=1,
                             nominal_srate=0,
                             channel_format="int32",
                             source_id="msim_frame_01")
    outlet_frame = StreamOutlet(info_frame)
 
    # Steering wheel angle stream (float32)
    info_angle = StreamInfo(name="SW_Angle",
                             type="Sensor",
                             channel_count=1,
                             nominal_srate=0,
                             channel_format="float32",
                             source_id="msim_angle_01")
    outlet_angle = StreamOutlet(info_angle)
 
    # ---- open socket to miniSim ------------------------------
    sock_type = socket.SOCK_DGRAM if proto == "udp" else socket.SOCK_STREAM
    sock = socket.socket(socket.AF_INET, sock_type)
    sock.bind(("", port))   # listen on all interfaces
    print(f"[relay] Listening for miniSim on {proto.upper()} port {port}")
 
    # For UDP, sock.connect helps set default target for recv
    sock.connect((ip, port))
    print(f"[relay] Connected to miniSim {ip}:{port} via {proto.upper()}")
 
    while True:
        # receive packet
        if proto == "udp":
            pkt, _ = sock.recvfrom(1024)
        else:
            pkt = sock.recv(1024)
            if not pkt:
                break
 
        # We expect at least 8 bytes: 4 bytes for FrameNum, 4 bytes for SW_Angle
        if len(pkt) < 8:
            print(f"[relay] Warning: packet too small ({len(pkt)} bytes)")
            continue
 
        # Unpack: little-endian unsigned int then float
        frame, angle = struct.unpack('<If', pkt[:8])
        print(f"[relay] Parsed FrameNum: {frame}, SW_Angle: {angle:.3f}")
 
        # push to LSL streams
        outlet_frame.push_sample([frame])
        outlet_angle.push_sample([angle])
 
 
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="miniSim to LSL relay")
    p.add_argument("--ip",   required=True, help="miniSim IP")
    p.add_argument("--port", type=int, required=True, help="miniSim port")
    p.add_argument("--proto", choices=["udp","tcp"], default="udp")
    args = p.parse_args()
    main(args.ip, args.port, args.proto)

# ip  192.168.20.45
# port = 1230
# python minisim_relay.py --ip 192.168.20.45 --port 1230 --proto udp
