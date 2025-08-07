# import sys, collections, socket, threading, struct
# from PyQt5 import QtWidgets, QtGui, QtCore
# import pyqtgraph as pg
# import cv2
# from lsl_worker import LSLWorker

# class Dashboard(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Real Time Monitoring Dashboard")
#         self.setStyleSheet("background-color: #1e1e2f; color: white;")
#         self.resize(1400, 800)

#         pg.setConfigOptions(antialias=True)

#         central_widget = QtWidgets.QWidget()
#         self.setCentralWidget(central_widget)
#         grid = QtWidgets.QGridLayout(central_widget)
#         grid.setContentsMargins(10, 10, 10, 10)
#         grid.setSpacing(2)

#         # -------------------- WIDGETS ------------------------
#         self.gaze_plot = pg.PlotWidget(title="EYE TRACKING")
#         self._setup_plot(self.gaze_plot)
#         self.gaze_curve = self.gaze_plot.plot(pen=pg.mkPen('#fdd835', width=1.5), name="gx vs gy")

#         self.bpm_plot = pg.PlotWidget(title="BPM")
#         self._setup_plot(self.bpm_plot)
#         self.bpm_curve = self.bpm_plot.plot(pen=pg.mkPen('#00bcd4', width=1.5))

#         self.frame_label = QtWidgets.QLabel("FRAME 000")
#         self.frame_label.setAlignment(QtCore.Qt.AlignCenter)
#         self.frame_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
#         self.frame_label.setStyleSheet("color: white; background-color: #1e1e2f;")

#         self.cam_label = QtWidgets.QLabel()
#         self.cam_label.setMinimumSize(400, 300)
#         self.cam_label.setAlignment(QtCore.Qt.AlignCenter)
#         self.cam_label.setStyleSheet("background-color: black; border: 2px solid #333;")

#         self.event_table = QtWidgets.QTableWidget()
#         self.event_table.setColumnCount(2)
#         self.event_table.setHorizontalHeaderLabels(["Time", "Event"])
#         self.event_table.verticalHeader().setVisible(False)
#         self.event_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
#         self.event_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
#         self.event_table.setShowGrid(True)
#         self.event_table.setStyleSheet("""
#             QTableWidget {
#                 background-color: #1e1e2f;
#                 color: #b0bec5;
#                 gridline-color: #3e4a5a;
#                 font: 10pt 'Courier';
#                 border: none;
#             }
#             QHeaderView::section {
#                 background-color: #263238;
#                 color: white;
#                 padding: 4px;
#                 border: none;
#             }
#             QTableWidget::item {
#                 selection-background-color: #1e1e2f;
#                 selection-color: #b0bec5;
#             }
#         """)
#         self.event_table.horizontalHeader().setStretchLastSection(True)
#         self.event_table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

#         # -------------------- LAYOUTS ------------------------
#         plot_layout = QtWidgets.QVBoxLayout()
#         plot_layout.addWidget(self.gaze_plot)
#         plot_layout.addWidget(self.bpm_plot)

#         camera_layout = QtWidgets.QVBoxLayout()
#         camera_layout.addWidget(self.frame_label)
#         camera_layout.addWidget(self.cam_label, stretch=3)
#         camera_layout.addWidget(self.event_table, stretch=2)

#         grid.addLayout(plot_layout, 0, 0)
#         grid.addLayout(camera_layout, 0, 1)
#         grid.setColumnStretch(0, 3)
#         grid.setColumnStretch(1, 2)

#         # -------------------- BUFFERS ------------------------
#         self.gaze_buffer = collections.deque(maxlen=1000)
#         self.bpm_buffer = collections.deque(maxlen=1000)

#         # -------------------- LSL ----------------------------
#         self.lsl = LSLWorker()
#         self.lsl.gazeSig.connect(self.on_gaze)
#         self.lsl.hrSig.connect(self.on_hr)
#         self.lsl.start()

#         # ------------------ FRAME UDP THREAD -----------------
#         threading.Thread(target=self._listen_for_frame_udp, daemon=True).start()

#         # -------------------- CAMERA -------------------------
#         self.cam = cv2.VideoCapture(0)

#         # -------------------- TIMER --------------------------
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.update_dashboard)
#         self.timer.start(10)

#     def _setup_plot(self, plot):
#         plot.setBackground('#1e1e2f')
#         plot.showGrid(x=True, y=True, alpha=0.2)
#         plot.getAxis('left').setPen(pg.mkPen('#ffffff'))
#         plot.getAxis('bottom').setPen(pg.mkPen('#ffffff'))
#         plot.addLegend()

#     def on_gaze(self, ts, gx, gy):
#         self.gaze_buffer.append((gx, gy))
#         self.insert_event_row(ts, "Gaze: gx vs gy")

#     def on_hr(self, ts, bpm):
#         self.bpm_buffer.append((ts, bpm))
#         self.insert_event_row(ts, "Heart rate")

#     def update_dashboard(self):
#         if self.gaze_buffer:
#             self.gaze_curve.setData([g[0] for g in self.gaze_buffer], [g[1] for g in self.gaze_buffer])
#         if self.bpm_buffer:
#             self.bpm_curve.setData(list(range(len(self.bpm_buffer))), [b[1] for b in self.bpm_buffer])
#         ret, frame = self.cam.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
#                                frame.strides[0], QtGui.QImage.Format_RGB888)
#             self.cam_label.setPixmap(QtGui.QPixmap.fromImage(img).scaled(
#                 self.cam_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

#     def insert_event_row(self, timestamp, message):
#         time_str = QtCore.QDateTime.currentDateTime().toString("HH:mm:ss")
#         self.event_table.insertRow(0)
#         self.event_table.setItem(0, 0, QtWidgets.QTableWidgetItem(time_str))
#         self.event_table.setItem(0, 1, QtWidgets.QTableWidgetItem(message))
#         if self.event_table.rowCount() > 100:
#             self.event_table.removeRow(100)

#     def _listen_for_frame_udp(self):
#         UDP_IP = "192.168.20.45"
#         UDP_PORT = 1230
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.bind((UDP_IP, UDP_PORT))
#         print(f"[D-LAB] Listening on {UDP_IP}:{UDP_PORT}...")

#         while True:
#             try:
#                 data, _ = sock.recvfrom(1024)
#                 if len(data) >= 4:
#                     frame_num = struct.unpack('<I', data[:4])[0]
#                     print(f"[D-LAB FRAME] {frame_num}")
#                     QtCore.QMetaObject.invokeMethod(
#                         self.frame_label,
#                         "setText",
#                         QtCore.Qt.QueuedConnection,
#                         QtCore.Q_ARG(str, f"FRAME {frame_num:03}")
#                     )
#             except Exception as e:
#                 print(f"[D-LAB ERROR] {e}")

#     def closeEvent(self, event):
#         self.lsl.stop()
#         self.cam.release()
#         event.accept()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     dash = Dashboard()
#     dash.show()
#     sys.exit(app.exec_())

##--------------------------------------------------------------------------------------
import os, csv 
from csv_logger import CSVLogger

import sys, collections, socket, threading, struct
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import cv2
from lsl_worker import LSLWorker

class Dashboard(QtWidgets.QMainWindow):
    frameUpdateSig = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.recording = False
        self.logger = None

        self.setWindowTitle("Real Time Monitoring Dashboard")
        self.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.resize(1400, 800)

        pg.setConfigOptions(antialias=True)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        grid = QtWidgets.QGridLayout(central_widget)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setSpacing(2)

        self.gaze_plot = pg.PlotWidget(title="EYE TRACKING")
        self._setup_plot(self.gaze_plot)
        self.gaze_curve = pg.PlotDataItem(
            pen=None,
            symbol='o',
            symbolSize=4,
            symbolPen=None,
            symbolBrush=pg.mkBrush("#fdd835")  # yellow
        )
        self.gaze_plot.addItem(self.gaze_curve)

        # If you want a legend, add this after:
        self.gaze_plot.addLegend()
    

        self.bpm_plot = pg.PlotWidget(title="BPM")
        self._setup_plot(self.bpm_plot)
        self.bpm_curve = self.bpm_plot.plot(pen=pg.mkPen('#00bcd4', width=1.5))

        self.frame_label = QtWidgets.QLabel("FRAME 000")
        self.frame_label.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_label.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.frame_label.setStyleSheet("color: white; background-color: #1e1e2f;")

        self.cam_label = QtWidgets.QLabel()
        self.cam_label.setMinimumSize(400, 300)
        self.cam_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.cam_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cam_label.setStyleSheet("background-color: black; border: 2px solid #333;")

        self.event_table = QtWidgets.QTableWidget()
        self.event_table.setColumnCount(2)
        self.event_table.setHorizontalHeaderLabels(["Time", "Event"])
        self.event_table.verticalHeader().setVisible(False)
        self.event_table.setShowGrid(True)
        self.event_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e2f;
                color: #b0bec5;
                gridline-color: #3e4a5a;
                font: 10pt 'Courier';
                border: none;
            }
            QHeaderView::section {
                background-color: #263238;
                color: white;
                padding: 4px;
                border: none;
            }
            QTableWidget::item {
                selection-background-color: #1e1e2f;
                selection-color: #b0bec5;
            }
        """)
        self.event_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.event_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.event_table.horizontalHeader().setStretchLastSection(True)
        self.event_table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        plot_layout = QtWidgets.QVBoxLayout()
        plot_layout.addWidget(self.gaze_plot)
        plot_layout.addWidget(self.bpm_plot)

        camera_layout = QtWidgets.QVBoxLayout()
        camera_layout.addWidget(self.frame_label)
        camera_layout.addWidget(self.cam_label, stretch=3)
        camera_layout.addWidget(self.event_table, stretch=2)

        grid.addLayout(plot_layout, 0, 0)
        grid.addLayout(camera_layout, 0, 1)
        grid.setColumnStretch(0, 3)
        grid.setColumnStretch(1, 2)

        self.gaze_buffer = collections.deque(maxlen=1000)
        self.bpm_buffer = collections.deque(maxlen=1000)

        self.lsl = LSLWorker()
        self.lsl.gazeSig.connect(self.on_gaze)
        self.lsl.hrSig.connect(self.on_hr)
        self.lsl.start()

        self.frameUpdateSig.connect(self._set_frame_label)
        threading.Thread(target=self._listen_for_frame, daemon=True).start()

        self.cam = cv2.VideoCapture(0)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(10)

        # — recording button bar —
        # btn_layout = QtWidgets.QHBoxLayout()
        # self.start_btn = QtWidgets.QPushButton("Start Recording")
        # self.stop_btn  = QtWidgets.QPushButton("Stop Recording")
        # self.stop_btn.setEnabled(False)
        # self.start_btn.clicked.connect(self.start_recording)
        # self.stop_btn.clicked.connect(self.stop_recording)
        # btn_layout.addWidget(self.start_btn)
        # btn_layout.addWidget(self.stop_btn)
        # — recording button bar —
        btn_layout = QtWidgets.QHBoxLayout()

        self.start_btn = QtWidgets.QPushButton("Start Recording")
        self.stop_btn  = QtWidgets.QPushButton("Stop Recording")
        self.stop_btn.setEnabled(False)

        # 🔥 STYLING HERE
        button_style = """
        QPushButton {
            background-color: #b71c1c;  /* light red */
            color: #ffffff;
            font: 10pt 'Segoe UI';
            padding: 8px 16px;
            border: 1px solid #d32f2f;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #c62828;
        }
        QPushButton:pressed {
            background-color: #8e0000;  /* deep red */
        }
        QPushButton:disabled {
            background-color: #2a2a2a;
            color: #777777;
            border: 1px solid #444;
        }
        """

        self.start_btn.setStyleSheet(button_style)
        self.stop_btn.setStyleSheet(button_style)

        # 🔗 Connections
        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        # place under row 0, span both columns
        grid.addLayout(btn_layout, 1, 0, 1, 2)




    def start_recording(self):
        # Ask once at start
        participant, ok1 = QtWidgets.QInputDialog.getText(self, "Participant", "ID (e.g., P001):")
        if not ok1: return
        session, ok2 = QtWidgets.QInputDialog.getText(self, "Session", "Session (e.g., S001):")
        if not ok2: return
        drive, ok3 = QtWidgets.QInputDialog.getText(self, "Drive/Block", "Drive/Block (optional):")
        if not ok3: drive = ""

        self.logger = CSVLogger(
            output_dir="records",
            prefix="multistream",
            participant=participant.strip(),
            session=session.strip(),
            drive=drive.strip()
        )
        self.recording = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

 
    def stop_recording(self):
        self.recording = False
        if self.logger:
            self.logger.close()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)





    def _setup_plot(self, plot):
        plot.setBackground('#1e1e2f')
        plot.showGrid(x=True, y=True, alpha=0.2)
        plot.getAxis('left').setPen(pg.mkPen('#ffffff'))
        plot.getAxis('bottom').setPen(pg.mkPen('#ffffff'))
        plot.addLegend()

    def on_gaze(self, ts, gx, gy):
        self.gaze_buffer.append((gx, gy))
        self.insert_event_row(ts, "Gaze: gx vs gy")

    def on_hr(self, ts, bpm):
        self.bpm_buffer.append((ts, bpm))
        self.insert_event_row(ts, "Heart rate")

    def update_dashboard(self):
        if self.gaze_buffer:
            x = [g[0] for g in self.gaze_buffer]
            y = [g[1] for g in self.gaze_buffer]
            self.gaze_curve.setData(x, y)
            self.gaze_plot.enableAutoRange()

        if self.bpm_buffer:
            self.bpm_curve.setData([i for i in range(len(self.bpm_buffer))], [b[1] for b in self.bpm_buffer])

        ret, frame = self.cam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
                            frame.strides[0], QtGui.QImage.Format_RGB888)
            self.cam_label.setPixmap(QtGui.QPixmap.fromImage(img).scaled(
                self.cam_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))


    def insert_event_row(self, timestamp, message):
        time_str = QtCore.QDateTime.currentDateTime().toString("HH:mm:ss")
        self.event_table.insertRow(0)
        self.event_table.setItem(0, 0, QtWidgets.QTableWidgetItem(time_str))
        self.event_table.setItem(0, 1, QtWidgets.QTableWidgetItem(message))
        if self.event_table.rowCount() > 100:
            self.event_table.removeRow(100)



        if self.recording and self.logger:
            # pull latest buffered values
            gx    = self.gaze_buffer[-1][0] if self.gaze_buffer else ""
            gy    = self.gaze_buffer[-1][1] if self.gaze_buffer else ""
            bpm   = self.bpm_buffer[-1][1] if self.bpm_buffer else ""
            frame = getattr(self, "current_frame", "")
            self.logger.log(time_str, message, gx, gy, bpm, frame)




    def _set_frame_label(self, text):
        self.frame_label.setText(text)
    
    def _listen_for_frame(self):
        import struct
        UDP_IP = "192.168.20.45"
        UDP_PORT = 1230

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        print(f"[D-LAB] Listening on {UDP_IP}:{UDP_PORT}...")

        while True:
            try:
                data, _ = sock.recvfrom(1024)
                if len(data) >= 4:
                    frame_num = struct.unpack('<I', data[:4])[0]
                    print(f"[D-LAB] Frame: {frame_num}")
                    self.current_frame = frame_num  #added
                    self.frameUpdateSig.emit(f"FRAME {frame_num:03}")
                    # self.frame_label.setText(f"FRAME {frame_num:03}")  # ✅ DIRECT UI CALL (SAFE)
            except Exception as e:
                print(f"[D-LAB ERROR] Could not parse frame number: {e}")


    def closeEvent(self, event):
        self.lsl.stop()
        self.cam.release()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dash = Dashboard()
    dash.show()
    sys.exit(app.exec_())
