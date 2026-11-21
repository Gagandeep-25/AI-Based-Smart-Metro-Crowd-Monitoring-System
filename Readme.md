
# 🚇 AI-Based Metro Crowd Monitoring System

An AI-powered crowd monitoring system that detects and estimates passenger occupancy inside metro compartments using CCTV footage and displays real-time crowd information at the upcoming metro station.

The main objective is to help passengers identify less crowded compartments before boarding, improve passenger distribution, and reduce overcrowding inside metro trains.

---

## 📌 1. Project Overview

During peak hours, metro compartments often experience overcrowding. Passengers waiting at stations generally have no information about the occupancy level of individual compartments.

This project proposes an automated solution using **Computer Vision, Object Detection, Embedded Systems, and Serial Communication**.

A camera installed inside a metro compartment captures live video. A Raspberry Pi processes the video using an object detection model to detect and count passengers. Based on the estimated passenger count, the system classifies the crowd level and transmits the information to an ESP32.

The ESP32 receives the information and displays the passenger count and crowd status on an LCD installed at the next station.

### Example Output

| Passenger Count | Crowd Status |
|---|---|
| 0–20 | LOW |
| 21–40 | MEDIUM |
| 41–60 | HIGH |
| Above 60 | OVERLOAD |

*Note: These are initial prototype thresholds. They must be calibrated according to the actual compartment capacity and camera coverage.*

---

## 🎯 2. Project Objectives

- Detect passengers inside metro compartments using computer vision.
- Estimate the number of passengers in each compartment.
- Classify crowd density into different categories.
- Transmit crowd information to the upcoming station.
- Display real-time passenger count and crowd status.
- Help passengers choose less crowded compartments.
- Develop a scalable system that can eventually monitor multiple compartments.

---

## 🏗️ 3. System Architecture

The system consists of two main processing units:

1. **Raspberry Pi 4:** Performs image processing, passenger detection, counting, and crowd classification.
2. **ESP32:** Receives the processed information and updates the LCD display.

### Block Diagram

```text
       METRO COMPARTMENT
              |
              v
        CCTV / CAMERA
              |
              v
       RASPBERRY PI 4
              |
       Live Video Feed
              |
              v
     IMAGE PROCESSING
       (Python + OpenCV)
              |
              v
      PERSON DETECTION
         (YOLO Model)
              |
              v
       PASSENGER COUNT
              |
              v
      CROWD CLASSIFICATION
       LOW / MEDIUM / HIGH
          / OVERLOAD
              |
              v
       UART COMMUNICATION
              |
              v
            ESP32
              |
              v
       I2C LCD DISPLAY
              |
              v
      NEXT METRO STATION
```

### Data Flow

```text
Camera → Raspberry Pi → YOLO Detection
       → Passenger Count → Crowd Classification
       → UART → ESP32 → LCD Display
```

---

## 🔧 4. Hardware Requirements

| Component | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 4 (1GB RAM) | 1 | Image processing and AI inference |
| ESP32 Development Board | 1 | Communication and display control |
| USB Webcam / Camera | 1 | Captures compartment footage |
| 16x2 I2C LCD | 1 | Displays passenger count and crowd status |
| Jumper Wires | As required | Hardware connections |
| MicroSD Card | 1 | Raspberry Pi operating system and files |
| Power Supply | As required | Powers the Raspberry Pi and ESP32 |

---

## 💻 5. Software Requirements

| Software / Library | Purpose |
|---|---|
| Python | Main image-processing program |
| OpenCV | Capturing and processing video frames |
| YOLO | Detecting people in video frames |
| PySerial | UART communication from Raspberry Pi |
| Arduino IDE | Programming the ESP32 |
| LiquidCrystal_I2C | Controlling the LCD |
| Wire Library | I2C communication |

### Technologies Used

- Python
- C++ (Arduino Framework)
- Computer Vision
- Object Detection
- YOLO
- OpenCV
- UART
- I2C
- Raspberry Pi OS

---

## 🧠 6. Working Principle

### Step 1: Video Acquisition

A camera installed inside the metro compartment captures live video of passengers.

The camera is connected to the Raspberry Pi through USB or a compatible camera interface.

OpenCV is used to access the camera and continuously capture frames.

### Step 2: Image Processing

The captured frames are passed to the YOLO object detection model.

YOLO identifies objects in each frame and assigns class labels to them.

For this project, the model is configured to detect only the `person` class.

### Step 3: Passenger Detection and Counting

The YOLO model returns bounding boxes around detected passengers.

Each bounding box represents a person detected in the current frame.

The number of detected person bounding boxes is used as the initial passenger count.

### Step 4: Crowd Classification

The estimated passenger count is compared against predefined thresholds.

Example:

```python
def get_crowd_status(count):

    if count <= 20:
        return "LOW"

    elif count <= 40:
        return "MEDIUM"

    elif count <= 60:
        return "HIGH"

    else:
        return "OVERLOAD"
```

The system generates one of four crowd categories:

- LOW
- MEDIUM
- HIGH
- OVERLOAD

### Step 5: UART Communication

The Raspberry Pi transmits the passenger count and crowd status to the ESP32 through UART serial communication.

Example transmitted message:

```text
35,MEDIUM
```

Here:

- `35` represents the estimated passenger count.
- `MEDIUM` represents the crowd classification.

A newline character (`\n`) marks the end of each message.

### Step 6: ESP32 Data Processing

The ESP32 receives the serial data and separates the passenger count from the crowd status.

It validates the received message and updates the LCD accordingly.

### Step 7: LCD Display

The LCD displays the latest available passenger count and crowd status.

Example:

```text
PASSENGERS: 35
STATUS: MEDIUM
```

This information can be displayed on a platform-side screen at the upcoming metro station.

---

## 🔌 7. Hardware Connections

### Raspberry Pi 4 to ESP32 (UART)

| Raspberry Pi 4 | ESP32 | Purpose |
|---|---|---|
| GPIO14 / TXD (Physical Pin 8) | GPIO16 / RX2 | Transmit serial data |
| GND (Physical Pin 6) | GND | Common ground |

**Communication Configuration:**

- Protocol: UART
- Baud Rate: 115200
- Data Bits: 8
- Parity: None
- Stop Bits: 1

The Raspberry Pi transmits data to the ESP32. For this one-way prototype, the ESP32 TX pin is not required.

### ESP32 to LCD (I2C)

| ESP32 | I2C LCD |
|---|---|
| GPIO21 | SDA |
| GPIO22 | SCL |
| 5V / suitable supply | VCC |
| GND | GND |

**Important:** Check the LCD backpack's I2C pull-up voltage. If SDA and SCL are pulled up to 5V, use a bidirectional I2C level shifter to protect the ESP32's 3.3V GPIO pins.

The LCD I2C address is commonly `0x27` or `0x3F`. Verify the address using an I2C scanner.

---

## 📂 8. Project Directory Structure

```text
Metro-Crowd-Monitoring/
│
├── raspberry_pi/
│   │
│   ├── metro_crowd.py
│   ├── requirements.txt
│   └── README.md
│
├── esp32/
│   │
│   └── metro_display/
│       └── metro_display.ino
│
├── hardware/
│   │
│   ├── circuit_diagram.png
│   └── block_diagram.png
│
├── results/
│   │
│   ├── detection_output.jpg
│   └── lcd_output.jpg
│
└── README.md
```

---

## ⚙️ 9. Installation and Setup

### A. Raspberry Pi Setup

Update the Raspberry Pi:

```bash
sudo apt update
sudo apt upgrade -y
```

Install the required system packages:

```bash
sudo apt install python3-opencv python3-venv python3-pip -y
```

Create the project directory:

```bash
mkdir metro-crowd-monitoring
cd metro-crowd-monitoring
```

Create and activate a virtual environment:

```bash
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install pyserial ultralytics
```

For initial development, it is recommended to test the YOLO implementation on a laptop before deploying it on the Raspberry Pi.

**Hardware limitation:** Raspberry Pi 4 with 1GB RAM has limited resources. The standard Ultralytics/PyTorch runtime may be too memory-intensive. A lightweight exported model and optimized inference runtime may be required for deployment.

### B. ESP32 Setup

1. Install Arduino IDE.
2. Install ESP32 board support.
3. Connect the ESP32 to your computer.
4. Install the `LiquidCrystal_I2C` library.
5. Open `metro_display.ino`.
6. Select the correct ESP32 board and COM port.
7. Upload the program.

---

## 📡 10. Communication Protocol

The Raspberry Pi sends data in the following format:

```text
PASSENGER_COUNT,CROWD_STATUS
```

Example:

```text
25,MEDIUM
```

The ESP32 parses the message using the comma as a separator.

| Field | Example | Description |
|---|---|---|
| Passenger Count | 25 | Estimated number of passengers |
| Crowd Status | MEDIUM | Classified crowd level |

A newline character is used to identify the end of each message.

---

## 🧪 11. Testing and Validation

The project can be tested in separate stages.

### Test 1: Camera Testing

- Connect the camera to the Raspberry Pi.
- Verify that live video is being captured.
- Check the camera resolution and frame rate.

### Test 2: Object Detection

- Run the YOLO model on sample metro footage.
- Verify that people are detected correctly.
- Check the passenger count against manually counted passengers.

### Test 3: Crowd Classification

- Test different passenger counts.
- Verify that the correct crowd category is generated.
- Adjust thresholds based on compartment capacity.

### Test 4: UART Communication

- Send sample messages from the Raspberry Pi.
- Verify that the ESP32 receives the correct data.
- Test invalid and incomplete messages.

### Test 5: LCD Display

- Verify that the passenger count is displayed.
- Verify that the crowd status is updated.
- Check the display behavior when communication is interrupted.

### Test 6: End-to-End Testing

Run the complete system and verify:

- Camera captures video.
- YOLO detects passengers.
- Passenger count is estimated.
- Crowd status is classified.
- UART transfers the information.
- ESP32 updates the LCD.

---

## ⚠️ 12. Current Limitations

The initial prototype has some limitations that must be considered before real-world deployment.

1. **Occlusion:** Passengers standing behind one another may not be detected.
2. **Detection Fluctuations:** Passenger counts may vary between consecutive frames.
3. **Unique Passenger Counting:** Counting bounding boxes in a single frame does not guarantee unique passenger counts.
4. **Camera Placement:** Incorrect camera angles can reduce detection accuracy.
5. **Processing Limitations:** Raspberry Pi 4 with 1GB RAM may not support high-performance real-time inference using the standard YOLO runtime.
6. **Threshold Calibration:** Crowd thresholds must be determined based on actual compartment capacity.
7. **Communication:** UART is suitable for a local prototype, but a real metro deployment needs a reliable communication network between moving trains and stations.

---

## 🚀 13. Future Improvements

The project can be extended with the following features:

- **Multi-Object Tracking:** Integrate tracking algorithms such as ByteTrack to improve passenger tracking and reduce duplicate counting.
- **Crowd Density Estimation:** Estimate occupancy using compartment area and passenger distribution rather than relying only on raw counts.
- **Multiple Compartment Monitoring:** Install cameras in multiple compartments and aggregate their crowd information.
- **Wireless Communication:** Use Wi-Fi, MQTT, or a suitable train-to-ground communication system for transmitting data.
- **Station Display Integration:** Display crowd information for all compartments on a single platform-side screen.
- **Edge AI Optimization:** Deploy optimized models using lightweight inference runtimes.
- **Historical Data Analysis:** Store occupancy data to identify peak-hour crowd patterns.
- **Predictive Analytics:** Predict crowd levels at upcoming stations using historical occupancy and passenger movement data.

---

## 🔮 14. Expected Final Output

The final system is intended to display the occupancy status of multiple metro compartments at the upcoming station.

Example:

```text
================================
       METRO CROWD STATUS
================================

COMPARTMENT 1 : LOW
COMPARTMENT 2 : MEDIUM
COMPARTMENT 3 : HIGH
COMPARTMENT 4 : OVERLOAD
COMPARTMENT 5 : LOW

================================
  CHOOSE A LESS CROWDED COACH
================================
```

This information helps passengers make informed boarding decisions and can contribute to better passenger distribution across metro compartments.

---

## 👨‍💻 15. Project Contributors

**Project Name:** AI-Based Metro Crowd Monitoring System

**Domain:**
- Artificial Intelligence
- Computer Vision
- Embedded Systems
- IoT
- Object Detection

**Core Technologies:** Python, C++, YOLO, OpenCV, Raspberry Pi, ESP32, UART, I2C.

---

## 📜 16. Disclaimer

This repository contains an academic prototype intended for learning and demonstration purposes.

The prototype is not certified for operational deployment in public transportation systems. Real-world implementation requires extensive testing, privacy and security safeguards, hardware reliability validation, and integration with approved metro infrastructure.
