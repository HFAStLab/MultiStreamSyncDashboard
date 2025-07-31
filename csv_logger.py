import csv, os, errno

from datetime import datetime
 
class CSVLogger:

    def __init__(self, output_dir="records", prefix="session"):

        # ensure output folder exists

        try:

            os.makedirs(output_dir)

        except OSError as e:

            if e.errno != errno.EEXIST:

                raise
 
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.filepath = os.path.join(output_dir, f"{prefix}_{ts}.csv")

        # line buffering

        self.csv_file = open(self.filepath, "w", newline="", buffering=1)

        self.writer   = csv.writer(self.csv_file)

        # header

        self.writer.writerow(["Time","Event","gx","gy","bpm","frame"])

    def log(self, time_str, event, gx=None, gy=None, bpm=None, frame=None):

        self.writer.writerow([time_str, event, gx, gy, bpm, frame])

        self.csv_file.flush()            # Python buffer → OS

        os.fsync(self.csv_file.fileno()) # OS buffer → disk
 
    def close(self):

        self.csv_file.close()

 