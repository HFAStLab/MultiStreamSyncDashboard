import pyxdf
import os
import numpy as np
import pandas as pd

# === SET PATH ===
xdf_path = r"C:\Users\hfast\Documents\CurrentStudy\sub-P001\ses-S001\eeg\sub-P001_ses-S001_task-Default_run-001_eeg.xdf"
# === LOAD XDF ===
streams, fileheader = pyxdf.load_xdf(xdf_path)
print(f"\n✅ Loaded XDF: {xdf_path}")
print(f"Found {len(streams)} streams.\n")

# === OUTPUT DIRECTORY ===
out_dir = os.path.dirname(xdf_path)

# === EXPORT EACH STREAM ===
for i, stream in enumerate(streams):
    name = stream['info']['name'][0].replace(" ", "_").replace("/", "_")
    stream_type = stream['info']['type'][0]
    ch_count = int(stream['info']['channel_count'][0])
    time_series = np.array(stream['time_series'])
    timestamps = np.array(stream['time_stamps'])

    # ✅ Skip empty streams to avoid DataFrame shape errors
    if time_series.shape[0] == 0:
        print(f"❌ Skipping stream {i+1} — empty time_series.")
        continue

    # Generate channel names (or fallback to generic)
    try:
        labels = [ch['label'][0] for ch in stream['info']['desc'][0]['channels'][0]['channel']]
    except:
        labels = [f"{stream_type}_Ch{i+1}" for i in range(ch_count)]

    # Build DataFrame
    df = pd.DataFrame(time_series, columns=labels)
    df.insert(0, 'Time (s)', timestamps)

    # Export
    csv_filename = f"{i+1}_{name}_{stream_type}.csv"
    out_path = os.path.join(out_dir, csv_filename)
    df.to_csv(out_path, index=False)

    print(f"✅ Exported stream {i+1} → {csv_filename} | {len(df)} rows, {len(df.columns)} columns")



# import pyxdf
# import os
# import numpy as np
# import pandas as pd
 
# # === SET PATH ===
# xdf_path = r"C:\Users\hfast\Documents\CurrentStudy\sub-P003\ses-S001\eeg\sub-P003_ses-S001_task-Default_run-001_eeg.xdf"
 
# # === LOAD XDF ===
# streams, fileheader = pyxdf.load_xdf(xdf_path)
# print(f"\n✅ Loaded XDF: {xdf_path}")
# print(f"Found {len(streams)} streams.\n")
 
# # === OUTPUT DIRECTORY ===
# out_dir = os.path.dirname(xdf_path)
 
# for i, stream in enumerate(streams, start=1):
#     # Basic info
#     name = stream['info']['name'][0]
#     stype = stream['info']['type'][0]
#     ch_count = int(stream['info']['channel_count'][0])
#     time_series = np.array(stream['time_series'])
#     timestamps = np.array(stream['time_stamps'])
 
#     print(f"Stream {i}: “{name}” ({stype}), channels={ch_count}, samples={len(time_series)}")
 
#     # If this is the frame number stream, peek at the first few values
#     if name.lower() in ("framenum", "frame_num", "frame-number"):
#         print(" → First 10 FrameNum samples:", time_series[:10].flatten())
#         print(" → First 10 timestamps  :", timestamps[:10].flatten())
#     # Skip empty streams
#     if len(time_series) == 0:
#         print(" → Skipping empty stream.\n")
#         continue
 
#     # Build labels (fallback to generic if missing)
#     try:
#         labels = [ch['label'][0]
#                   for ch in stream['info']['desc'][0]['channels'][0]['channel']]
#     except Exception:
#         labels = [f"{stype}_Ch{j+1}" for j in range(ch_count)]
 
#     # Make sure our label count matches
#     if len(labels) != ch_count:
#         print(f" → WARNING: channel_count={ch_count} but found {len(labels)} labels. Using generic labels.")
#         labels = [f"{stype}_Ch{j+1}" for j in range(ch_count)]
 
#     # Build DataFrame
#     df = pd.DataFrame(time_series, columns=labels)
#     df.insert(0, 'Time (s)', timestamps)
 
#     # Export
#     safe_name = name.replace(" ", "_").replace("/", "_")
#     csv_filename = f"{i:02d}_{safe_name}_{stype}.csv"
#     out_path = os.path.join(out_dir, csv_filename)
#     df.to_csv(out_path, index=False)
#     print(f" ✅ Exported → {csv_filename} ({len(df)} rows × {len(df.columns)} cols)\n")