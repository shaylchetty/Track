import cv2
import math
import Eucledian


# Create tracker object
tracker = Eucledian.EuclideanDistTracker()

# Open webcam capture
cap = cv2.VideoCapture(0)

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # width of screen
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # height of screen

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # face data set

previousFace = (-1, -1, 0, 0)  # Initialize previousFace with default values

previousPos = (-1, -1, 0, 0)  # Initialize previousPos with default values

previousPositions = [] # Array to store previous 5 positions

center_x = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #Face Recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        # detect current face
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        if([x,y,w,h] == [-1, -1, 0, 0]):
            break
        previousFace = [x, y, w, h]


    if len(faces) == 0:
        x, y, w, h = previousFace
        # capture of previous face location
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 3) 


    # Object detection
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    # Object tracking
    boxes_ids = tracker.update(detections)

    minSum = None
    minSumL = None

    farX = None
    farY = None
    farXL = None
    farYL = None


    for box_id in boxes_ids:
        x, y, w, h, _ = box_id
        

        # Calculate center coordinates
        cx = x + w // 2
        cy = y + h // 2

        # tiny green rectangles
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # tiny red circles at centers of rectangles
        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        sumR = math.sqrt((x**2 + y ** 2))

        sumL = math.sqrt((frame_width-(x + w))**2 + (frame_height-(y + h)) ** 2)

        if( minSum is None or minSum > sumR):
            minSum = sumR
            farX = x
            farY = y

        if( minSumL is None or minSumL > sumL):
            minSumL = sumL
            farXL = x + w
            farYL = y + h



    #center point
    if(not (farX is None or farY is None or farXL is None or farYL is None )):
        top_left_corner = (farX, farY)  # Example top-left corner coordinates
        bottom_right_corner = (farXL, farYL)  # Example bottom-right corner coordinates

        # Calculate center point
        center_x = (top_left_corner[0] + bottom_right_corner[0]) // 2
        center_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
        center_point = (center_x, center_y)

        # Draw circle at the center point of large box
        cv2.circle(frame, center_point, 10, (0, 0, 255), -1)

    if(center_x < 400):
        print("Pan Counter-Clockwise")
    elif(center_x > 880):
        print("Pan Clockwise")
    else:
        print("Stable")

    # large rectangle
    cv2.rectangle(frame, (farX, farY), (farXL, farYL), (0, 255, 0), 3)

    if not None in [farX, farY, farXL, farYL]:
        previousPositions.append([farX, farY, farXL, farYL])

    if len(previousPositions) > 5:
        previousPositions = previousPositions[-5:]  # Keep only the last 5 positions

    if None in  [farX, farY, farXL, farYL]:
        if not len(previousPositions) == 0:
            farX = sum(pos[0] for pos in previousPositions) // len(previousPositions)
            farY = sum(pos[1] for pos in previousPositions) // len(previousPositions)
            farXL = sum(pos[2] for pos in previousPositions) // len(previousPositions)
            farYL = sum(pos[3] for pos in previousPositions) // len(previousPositions)

            # draw rectangle over last recognized averaged over previous 5
            cv2.rectangle(frame, (farX, farY), (farXL, farYL), (255, 255, 0), 3)  

            top_left_corner = (farX, farY)  # Example top-left corner coordinates
            bottom_right_corner = (farXL, farYL)  # Example bottom-right corner coordinates

            # Calculate center point
            center_x = (top_left_corner[0] + bottom_right_corner[0]) // 2
            center_y = (top_left_corner[1] + bottom_right_corner[1]) // 2
            center_point = (center_x, center_y)

            # Draw circle at the center point of large box
            # cv2.circle(frame, center_point, 10, (0, 0, 255), -1)



    # Display the frame with tracked objects
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()


