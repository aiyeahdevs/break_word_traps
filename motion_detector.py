import cv2, time
from datetime import datetime
import json
import sys

def detect(vid):

	static_back = None
	motion_list = [ None, None ]
	time = []

	video = cv2.VideoCapture(vid)

	# loop video frames
	motions = 0
	time0 = datetime.now()

	while True:
		# reading frame(image) from video
		check, frame = video.read()

		# initializing motion = 0(no motion)
		motion = 0

		try:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		except:
			break

		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		if static_back is None:
			static_back = gray
			continue

		diff_frame = cv2.absdiff(static_back, gray)
		thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
		thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

		cnts,_ = cv2.findContours(thresh_frame.copy(),
						cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# contouring the moving parts
		for contour in cnts:
			motions += 1
			if cv2.contourArea(contour) < 10000:
				continue
			motion = 1

			(x, y, w, h) = cv2.boundingRect(contour)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

		motion_list.append(motion)
		motion_list = motion_list[-2:]

		# appending Start time of motion
		if motion_list[-1] == 1 and motion_list[-2] == 0:
			time.append(datetime.now())

		# appending End time of motion
		if motion_list[-1] == 0 and motion_list[-2] == 1:
			time.append(datetime.now())


		key = cv2.waitKey(1)
		static_back = gray

	print(motions)

	if motions > 2000:
		value = {
			"result": "Wykryto rozpraszający ruch"
		}
	else:
		value = {
			"result": "Nie wykryto rozpraszającego ruchu"
		}

	return json.dumps(value, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python motion_detector.py <path to vid>")
        sys.exit(1)
    
    result = detect(sys.argv[1])
    print(result)
