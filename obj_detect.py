
# ==========================================================
# PROJECT: AI-BASED SMART METRO CROWD MONITORING SYSTEM
# BOARD  : Raspberry Pi 4
# LANGUAGE: Python
#
# FUNCTION:
# 1. Capture video using camera
# 2. Detect people using YOLO
# 3. Estimate passenger count
# 4. Classify crowd density
# 5. Send information to ESP32 using UART
# ==========================================================


# ----------------------------------------------------------
# 1. IMPORT REQUIRED LIBRARIES
# ----------------------------------------------------------

import cv2                  # OpenCV: Camera and image processing
import serial               # PySerial: UART communication
import time                 # Time delays and timestamps
from ultralytics import YOLO  # YOLO object detection model


# ----------------------------------------------------------
# 2. PROJECT CONFIGURATION
# ----------------------------------------------------------

CAMERA_ID = 0

# UART configuration
SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 115200

# YOLO model file
MODEL_PATH = "yolo11n.pt"

# Camera resolution
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Crowd classification thresholds
LOW_LIMIT = 20
MEDIUM_LIMIT = 40
HIGH_LIMIT = 60

# Send data to ESP32 every 1 second
SEND_INTERVAL = 1.0

# Display camera window if a desktop is available
SHOW_WINDOW = True


# ----------------------------------------------------------
# 3. INITIALIZE YOLO MODEL
# ----------------------------------------------------------

print("Loading YOLO model...")

# Load pretrained YOLO nano model
# The model detects objects belonging to the COCO dataset

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully!")


# ----------------------------------------------------------
# 4. INITIALIZE CAMERA
# ----------------------------------------------------------

print("Connecting to camera...")

# Open the default camera
cap = cv2.VideoCapture(CAMERA_ID)

# Configure camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# Check whether camera is connected
if not cap.isOpened():

    raise RuntimeError("ERROR: Camera not detected!")

print("Camera connected successfully!")


# ----------------------------------------------------------
# 5. INITIALIZE UART COMMUNICATION
# ----------------------------------------------------------

print("Connecting to ESP32...")

# Open serial communication with ESP32
ser = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

# Allow serial connection to stabilize
time.sleep(2)

print("UART communication initialized!")


# ----------------------------------------------------------
# 6. CROWD CLASSIFICATION FUNCTION
# ----------------------------------------------------------

def get_crowd_status(count):

    # If passenger count is between 0 and 20
    if count <= LOW_LIMIT:

        return "LOW"

    # If passenger count is between 21 and 40
    elif count <= MEDIUM_LIMIT:

        return "MEDIUM"

    # If passenger count is between 41 and 60
    elif count <= HIGH_LIMIT:

        return "HIGH"

    # If passenger count exceeds 60
    else:

        return "OVERLOAD"


# ----------------------------------------------------------
# 7. MAIN PROGRAM
# ----------------------------------------------------------

print("\nSMART METRO CROWD MONITORING STARTED\n")

# Store the last transmission time
last_send_time = 0


try:

    # Continuously monitor the compartment
    while True:


        # --------------------------------------------------
        # STEP 1: CAPTURE CAMERA FRAME
        # --------------------------------------------------

        ret, frame = cap.read()

        # ret = True if frame is captured successfully
        # frame = actual image captured by camera

        if not ret:

            print("Camera frame unavailable!")

            time.sleep(0.2)

            continue


        # --------------------------------------------------
        # STEP 2: PERFORM YOLO PERSON DETECTION
        # --------------------------------------------------

        results = model.predict(

            frame,

            # Resize input for faster inference
            imgsz=320,

            # Minimum detection confidence = 35%
            conf=0.35,

            # COCO class 0 represents a person
            classes=[0],

            # Disable unnecessary terminal output
            verbose=False

        )


        # --------------------------------------------------
        # STEP 3: COUNT DETECTED PEOPLE
        # --------------------------------------------------

        # Extract number of detected bounding boxes
        count = len(results[0].boxes)

        # NOTE:
        # This is the number of detections in the current frame.
        # It is NOT a unique passenger count across video frames.


        # --------------------------------------------------
        # STEP 4: CLASSIFY CROWD DENSITY
        # --------------------------------------------------

        status = get_crowd_status(count)


        # --------------------------------------------------
        # STEP 5: SEND DATA TO ESP32 THROUGH UART
        # --------------------------------------------------

        current_time = time.time()

        # Send data once every SEND_INTERVAL seconds
        if current_time - last_send_time >= SEND_INTERVAL:

            # Create message in this format:
            # 35,MEDIUM
            #
            # '\n' marks the end of the message

            message = f"{count},{status}\n"

            # Convert Python string into bytes
            message_bytes = message.encode("utf-8")

            # Transmit bytes through UART
            ser.write(message_bytes)

            # Display transmitted information
            print("DATA SENT:", message.strip())

            # Update transmission timestamp
            last_send_time = current_time


        # --------------------------------------------------
        # STEP 6: DISPLAY DETECTION RESULTS
        # --------------------------------------------------

        # Draw bounding boxes around detected people
        output = results[0].plot()

        # Display passenger count
        cv2.putText(

            output,

            f"PASSENGERS: {count}",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 0),

            2

        )

        # Display crowd classification
        cv2.putText(

            output,

            f"CROWD STATUS: {status}",

            (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0, 255, 255),

            2

        )


        # Show camera window
        if SHOW_WINDOW:

            cv2.imshow(
                "METRO CROWD MONITORING",
                output
            )

            # Press Q to stop monitoring
            if cv2.waitKey(1) & 0xFF == ord('q'):

                break


# ----------------------------------------------------------
# 8. HANDLE PROGRAM INTERRUPTION
# ----------------------------------------------------------

except KeyboardInterrupt:

    print("\nMonitoring stopped by user!")


# ----------------------------------------------------------
# 9. RELEASE HARDWARE RESOURCES
# ----------------------------------------------------------

finally:

    # Release camera
    cap.release()

    # Close UART connection
    ser.close()

    # Close OpenCV windows
    cv2.destroyAllWindows()

    print("All resources released.")

