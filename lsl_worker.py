# lsl_worker.py -----------------------------------------------------------
import time, threading
from pylsl import StreamInlet, resolve_byprop
from PyQt5.QtCore import QObject, pyqtSignal
 
 # DEBUG: List available LSL streams
from pylsl import resolve_streams

print("\n[INFO] Listing all available LSL streams:\n")
for s in resolve_streams():
    print(f"Name: {s.name()}, Type: {s.type()}, Source ID: {s.source_id()}")

class LSLWorker(QObject):
    gazeSig  = pyqtSignal(float, float, float)    # ts, gx, gy
    hrSig    = pyqtSignal(float, float)           # ts, bpm
    frameSig = pyqtSignal(int)                    # frame #
 
    def __init__(self, parent=None):
        super().__init__(parent)
        self._run = False
 
    # ---------------------------------------------------------------------
    def start(self):
        self._run = True
        threading.Thread(target=self._loop, daemon=True).start()
 
    def stop(self):
        self._run = False
 
    # ---------------------------------------------------------------------
    def _open(self, prop):
        results = resolve_byprop(*prop, timeout=30)
        if not results:
            print(f"[!!] LSL stream not found: {prop}")
            return None
        return StreamInlet(results[0], max_buflen=60)
 
 
    def _loop(self):
        gaze  = self._open(('name', 'Neon Companion_Neon Gaze'))
        hr    = self._open(('name', 'Polar H10 E8988D20'))
        #frame = self._open(('name', 'miniSim_Frame'))

        while self._run:
            if gaze:
                samp, ts = gaze.pull_sample(0.0)
                if samp: self.gazeSig.emit(ts, *samp[:2])

            if hr:
                samp, ts = hr.pull_sample(0.0)
                if samp: self.hrSig.emit(ts, samp[0])

            # if frame:
            #     samp, _ = frame.pull_sample(0.0)
            #     if samp: self.frameSig.emit(int(samp[0]))
            # if frame:
            #       samp, _ = frame.pull_sample(0.0)
            #       if samp:
            #          # print(f"[FRAME LSL] Got frame: {samp[0]}")
            #          print(f"[DEBUG] FRAME: {samp[0]}")
            #          self.frameSig.emit(int(samp[0]))

            time.sleep(0.002)

