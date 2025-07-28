# MultiStreamSyncDashboard

# Developing a Dashboard for Real-Time Data Streaming towards Multimodal Driver Monitoring Systems

**Rima El Bagoury\***, **Audrey Wang\*\***, **Suzan Ayas\*\***, **Mattea Powell\*\***, **Fan Wang\*\***, **Prof. Birsen Donmez\*\***  
\*Division of Engineering Science, \*\*Department of Mechanical and Industrial Engineering, University of Toronto

---

Driver Monitoring Systems (DMS) analyze physiological signals, vehicle kinematics, and behavioral indicators to detect risky states (e.g., drowsiness or distraction) and keep drivers alert in real-time. Although DMS research is rapidly expanding, inconsistent findings hinder development of generalized models, limiting progress of intervention design and evaluation.

A unified tool that can simultaneously acquire, synchronize, and visualize multiple data modalities is needed for robust statistical and machine-learning modeling of suboptimal driver states. Currently available options are either disjointed or lack integrated data visualization tailored to DMS research. This project addresses this gap by integrating live data display and device communication into one interface for driving simulation research, streamlining DMS development.

Our research provides an open-source, low-latency dashboard integrated into PyQt5 that uses OpenCV libraries with lab streaming layer (LSL) and user datagram protocol (UDP) connections to link hardware and software. In addition to showing live webcam footage, the interface plots gaze position coordinates, raw electrocardiogram (ECG) data and derived heart rate, driving measures from the driving simulator, and event logs with timestamps. A modular, multithreaded architecture with bounded buffers ensures graphical user interface responsiveness at 100 Hz and sub-10 ms latency. The system also includes error handling that detects and recovers from device disconnections or other interruptions.

Next steps include evaluating the design and usability of the dashboard through pilot tests in collaboration with subject matter experts and identifying the best metrics representing different driver states from the literature for building appropriate visualizations. This dashboard enables DMS design and testing via controlled simulation studies by facilitating real-time monitoring and minimizing post-hoc synchronization efforts.

---

## Synchronization Instructions

### Prepare Workspace

1. **Launch LabRecorder**  
   a. On the DLab computer, open `LabRecorder.exe`.  
   b. *Do not open any DLab experiment software until directed below.*

2. **Open Code Base**  
   a. In Visual Studio Code, open the folder: `Documents/AudreyRima_work/`  (if you are on the Truck Simulator room's DLab computer, if not, download all the files in this repo and save it to your own directory folder)
   b. Verify that all required `.py` scripts are present.

---

### Neon Eye Tracker

3. **Set Up Phone Hotspot**  
   a. On the lab Nokia phone, connect to UofT Wi-Fi.  
   b. Enable the phone’s hotspot (SSID: `moto edge 40 pro_5189`).

4. **Connect DLab PC to Hotspot**  
   a. On the DLab computer, open Wi-Fi settings and join `moto edge 40 pro_5189`.

5. **Verify Stream in LabRecorder**  
   a. In LabRecorder, click **Update**.  
   b. You should see two green streams:  
      - `Neon Companion_Neon Gaze (localhost)`  
      - `Neon Companion_Neon Events (localhost)`

---

### Polar Heart Rate Band

6.  
   a. Open `Polar.GUI` on the DLab computer *after* the participant is wearing the band (snugly).  
   b. Click **Search for Device** and wait until `Polar H10 E8988D29` shows up, then click it.  
   c. In LabRecorder, click **Update**. You should now see a green stream:  
      - `Polar H10 E8988D29 (D-lab)`

---

### miniSim Simulator

7.  
   a. In VS Code, navigate to `test.py`.  
   b. Turn on the monitor in the driving simulator room **before** turning on the miniSim computer.  
   c. Open the miniSim software (ACC without videocap), select the event, and start the drive.  
      - *Make sure all rows in the miniSim system page are green before starting.*  
   d. Run `test.py` on the DLab computer.

8.  
   In LabRecorder, you should now see a green stream: `FrameNum`.  
   - Select all of them and change the participant number and event number on the right.  
   - Files will be saved to: `Documents/currentStudy`

9.  
   Launch the dashboard:  
   ```bash
   cd Documents/AudreyRima_work
   python dashboard.py
