import cv2
import os
import sys
from sys import platform
import numpy as np

# Import OpenPose Python module
try:
    # Change this path to the OpenPose python folder
    sys.path.append('/path/to/openpose/python')
    from openpose import pyopenpose as op
except ImportError as e:
    print(f"Error: OpenPose library could not be found. Check the OpenPose path. {e}")
    sys.exit(-1)

def process_frame(frame, net):
    # Process the frame and get the poses
    datum = op.Datum()
    datum.cvInputData = frame
    net.emplaceAndPop([datum])
    poses = datum.poseKeypoints

    return poses

def main():
    # Customizable OpenPose parameters
    params = dict()
    params["model_folder"] = "/path/to/openpose/models"  # Change this to the OpenPose model folder

    # Set OpenPose parameters
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Open the webcam (Change the index if you have multiple cameras)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame using OpenPose
        poses = process_frame(frame, opWrapper)

        # Draw the poses on the frame
        for pose in poses:
            for person in pose:
                for x, y, conf in person:
                    if conf > 0.2:  # Minimum confidence threshold to draw keypoints
                        cv2.circle(frame, (int(x), int(y)), 4, (0, 255, 255), -1)

        # Display the frame
        cv2.imshow("OpenPose - Multi-Person Pose Estimation", frame)

        # Exit the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
