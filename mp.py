import cv2
import mediapipe as mp
import helper


def track_human_motion():
    # Initialize MediaPipe pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    # Open video capture (0 for webcam, or provide video file path)
    cap = cv2.VideoCapture(0)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    FaceTop = frame_height

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )  # face data set

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Face Recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        # Draw rectangles around the detected faces
        for x, y, w, h in faces:
            # detect current face
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            FaceTop = int(y - (0.25 * h))  # adjust slightly for forehead and hair

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            # Extract landmarks for pose estimation
            landmarks = results.pose_landmarks.landmark

            # Do something with the detected landmarks (e.g., track motion or draw on the frame)
            # Example: Draw landmarks on the frame
            image_with_landmarks = frame.copy()

            coordinates = []

            xtotal = 0
            ytotal = 0
            count = 0

            for landmark in landmarks:
                h, w, _ = image_with_landmarks.shape
                x, y = int(landmark.x * w), int(landmark.y * h)

                # Only append the coordinate if it falls within the specified range
                if 0 <= x <= 1280 and 0 <= y <= 720:
                    count += 1
                    xtotal += x
                    ytotal += y
                    cv2.circle(image_with_landmarks, (x, y), 5, (0, 255, 0), -1)
                    coordinates.append((x, y))

            top_left_corner, bottom_right_corner = helper.closest_coordinates(
                coordinates, frame_width, frame_height
            )

            if top_left_corner[1] > FaceTop:
                top_left_corner = (
                    top_left_corner[0],
                    FaceTop,
                )  # adjust top corner to include top of head

            # Calculate center point
            # center_x = (top_left_corner[0] + bottom_right_corner[0]) // 2
            # center_y = (top_left_corner[1] + bottom_right_corner[1]) // 2

            if not count == 0:
                center_point = (xtotal // count, ytotal // count)

                # Draw circle at the center point of large box
                cv2.circle(image_with_landmarks, center_point, 10, (0, 255, 0), -1)

            # Draw rectangle at the center point oflarge box
            cv2.rectangle(
                image_with_landmarks,
                top_left_corner,
                bottom_right_corner,
                (0, 255, 0),
                3,
            )

            # Show the image with landmarks
            cv2.imshow("Motion Tracking", image_with_landmarks)
        else:
            cv2.imshow("Motion Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def video_human_motion(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    # Open video file
    cap = cv2.VideoCapture(video_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Draw landmarks on the frame
            image_with_landmarks = frame.copy()
            for landmark in landmarks:
                h, w, _ = image_with_landmarks.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(image_with_landmarks, (x, y), 5, (0, 255, 0), -1)

            cv2.imshow("Motion Tracking", image_with_landmarks)
        else:
            cv2.imshow("Motion Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # video_human_motion("Soccer.MOV")
    track_human_motion()
