# import socket
# import json
# from pylsl import StreamInfo, StreamOutlet
# import time

# # === CONFIGURATION ===
# REMOTE_IP = "100.70.205.194"   # Replace with Neon Companion's IP
# REMOTE_PORT = 8080        # Replace with correct port
# BUFFER_SIZE = 4096

# # === LSL Stream Setup ===

# # Gaze stream
# gaze_info = StreamInfo(name='Neon_Companion_Gaze', type='Gaze', channel_count=3,
#                        channel_format='float32', source_id='neon_companion_gaze')
# gaze_info.desc().append_child_value("description", "Manual Neon gaze stream: ts, gx, gy")
# gaze_outlet = StreamOutlet(gaze_info)

# # Event stream
# event_info = StreamInfo(name='Neon_Companion_Events', type='Markers', channel_count=2,
#                         channel_format='string', source_id='neon_companion_event')
# event_info.desc().append_child_value("description", "Manual Neon event stream: ts, label")
# event_outlet = StreamOutlet(event_info)

# # === Socket Setup ===
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((REMOTE_IP, REMOTE_PORT))
# sock.settimeout(100)
# print(f"[INFO] Connected to Neon Companion at {REMOTE_IP}:{REMOTE_PORT}")

# try:
#     while True:
#         try:
#             data = sock.recv(BUFFER_SIZE)
#             if not data:
#                 continue

#             decoded = data.decode('utf-8').strip()
#             for line in decoded.split("\n"):
#                 try:
#                     entry = json.loads(line)
#                     topic = entry.get('topic')

#                     if topic == 'gaze':
#                         ts = entry['timestamp']
#                         gx = entry['gaze'][0]
#                         gy = entry['gaze'][1]
#                         gaze_outlet.push_sample([ts, gx, gy])
#                         print(f"[GAZE] ts={ts:.3f}, gx={gx:.3f}, gy={gy:.3f}")

#                     elif topic == 'event':
#                         ts = entry['timestamp']
#                         label = entry['label']
#                         event_outlet.push_sample([str(ts), label])
#                         print(f"[EVENT] ts={ts:.3f}, label='{label}'")

#                 except json.JSONDecodeError:
#                     continue
#         except socket.timeout:
#             continue

# except KeyboardInterrupt:
#     print("\n[INFO] Disconnected.")
#     sock.close()

##-------------------------------------------------------------------------------------

import socket
import json
from pylsl import StreamInfo, StreamOutlet

# === CONFIGURATION ===
UDP_IP = "0.0.0.0"       # Listen on all interfaces
UDP_PORT = 8080          # 🔁 REPLACE with the actual UDP port used by Neon Companion
BUFFER_SIZE = 4096

# === LSL STREAM SETUP ===

# Gaze Stream: ts, gx, gy
gaze_info = StreamInfo(name='Neon_Companion_Gaze', type='Gaze', channel_count=3,
                       channel_format='float32', source_id='neon_companion_gaze')
gaze_info.desc().append_child_value("description", "Manual Neon gaze stream: ts, gx, gy")
gaze_outlet = StreamOutlet(gaze_info)

# Event Stream: timestamp, label
event_info = StreamInfo(name='Neon_Companion_Events', type='Markers', channel_count=2,
                        channel_format='string', source_id='neon_companion_event')
event_info.desc().append_child_value("description", "Manual Neon event stream: ts, label")
event_outlet = StreamOutlet(event_info)

# === UDP SOCKET SETUP ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[INFO] Listening for UDP packets on port {UDP_PORT}...")

# === RECEIVE AND STREAM LOOP ===
while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    try:
        decoded = data.decode('utf-8').strip()
        for line in decoded.split("\n"):
            if not line:
                continue
            try:
                entry = json.loads(line)
                topic = entry.get('topic')

                if topic == 'gaze':
                    ts = entry['timestamp']
                    gx = entry['gaze'][0]
                    gy = entry['gaze'][1]
                    gaze_outlet.push_sample([ts, gx, gy])
                    print(f"[GAZE] ts={ts:.3f}, gx={gx:.3f}, gy={gy:.3f}")

                elif topic == 'event':
                    ts = entry['timestamp']
                    label = entry['label']
                    event_outlet.push_sample([str(ts), label])
                    print(f"[EVENT] ts={ts:.3f}, label='{label}'")

            except json.JSONDecodeError:
                continue

    except UnicodeDecodeError:
        print("[WARN] Received non-UTF8 data, skipping.")
        continue
