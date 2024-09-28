import cv2
from deepface import DeepFace

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture('./videos/HY_2024_film_20.mp4')
emotions = []
face_frames = 0
multiple_faces = 0
frames_checked = 0
while True:
    # Capture frame-by-frame
    for i in range(10):
        ret, frame = cap.read()

    frames_checked += 1
    # Convert frame to grayscale
    try:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        break

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    if len(faces) > 0:
        face_frames += 1
        if len(faces) > 1:
            multiple_faces += 1

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        
        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
        print(result)
        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']

        # only recognize emotion if sufficienty confident
        if not result[0]['emotion'][emotion] > 70:
            emotion = "neutral"
        emotions.append(emotion)
        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

emotion_counts = {}
for e in ['happy', 'sad', 'angry', 'neutral', 'fear', 'suprise', 'disgust']:
    emotion_counts[e] = emotions.count(e)
    print(str(e) + ' : ' + str(emotions.count(e)))

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

print(emotion_counts)
print(max(emotion_counts.values()))

print()

print(face_frames, multiple_faces, frames_checked)



