import cv2, time, numpy, pickle
vid = cv2.VideoCapture(0)
re,fram = vid.read()
out = cv2.VideoWriter("recordedvideo.avi", cv2.VideoWriter_fourcc(*'DIVX'),20,(numpy.shape(fram)[1],numpy.shape(fram)[0]))
recording = []
while(vid.isOpened()):
	start = time.time()
	ret,frame = vid.read()
	if ret == True:
		recording.append(frame)
		out.write(frame)
		cv2.imshow("RECORDING  Press 'q' to stop",frame)
		key = cv2.waitKey(1) & 0xFF
		if key ==ord('q'):
			break
	else:
		break
	t = 0.05-(time.time()-start)
	if t>0:
		time.sleep(t)
vid.release()
out.release()
cv2.destroyAllWindows()
with open("recordedvideo.pkl","wb") as f:
	pickle.dump(recording,f)
