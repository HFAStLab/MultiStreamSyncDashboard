import csv, os, errno, re
from datetime import datetime

def _slug(s: str) -> str:
    # safe for filenames
    return re.sub(r'[^A-Za-z0-9._-]+', '-', str(s)).strip('-')

class CSVLogger:
    def __init__(self, output_dir="records", prefix="session",
                 participant=None, session=None, drive=None):
        """
        participant: e.g. 'P001'
        session:     e.g. 'S001'
        drive:       e.g. 'D1' or 'Baseline' (optional)
        """

        # build folder structure: records/P001/S001
        parts = []
        if participant: parts.append(_slug(participant))
        if session:     parts.append(_slug(session))
        subdir = os.path.join(output_dir, *parts) if parts else output_dir

        try:
            os.makedirs(subdir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Canadian date format in filename: DD-MM-YYYY_HHMMSS
        ts = datetime.now().strftime("%d-%m-%Y_%H%M%S")

        # filename: <prefix>_<participant>_<session>_<drive>_<timestamp>.csv
        name_bits = [prefix]
        if participant: name_bits.append(_slug(participant))
        if session:     name_bits.append(_slug(session))
        if drive:       name_bits.append(_slug(drive))
        name_bits.append(ts)
        filename = "_".join(name_bits) + ".csv"

        self.filepath = os.path.join(subdir, filename)

        # line-buffered
        self.csv_file = open(self.filepath, "w", newline="", buffering=1)
        self.writer   = csv.writer(self.csv_file)

        # --- metadata header (comment lines) ---
        self.writer.writerow([f"# participant={participant or ''}"])
        self.writer.writerow([f"# session={session or ''}"])
        self.writer.writerow([f"# drive={drive or ''}"])
        self.writer.writerow([f"# started_at={datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"])
        # data header
        self.writer.writerow(["Time","Event","gx","gy","ECG","FrameNum"])

    def log(self, time_str, event, gx=None, gy=None, bpm=None, frame=None):
        self.writer.writerow([time_str, event, gx, gy, bpm, frame])
        self.csv_file.flush()
        os.fsync(self.csv_file.fileno())

    def close(self):
        self.csv_file.close()
