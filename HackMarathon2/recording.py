import cv2, time, numpy, pickle

fps = 20
filename = "recordedvideo.avi"

def record(filename):
	ti = 3 # recording length
	vid = cv2.VideoCapture(0)
	re,fram = vid.read()
	out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, (numpy.shape(fram)[1],numpy.shape(fram)[0]))
	recording = []
	while(vid.isOpened()):
		start = time.time()
		ret,frame = vid.read()
		if ret == True:
			recording.append(frame)
			out.write(frame)
			#cv2.imshow("RECORDING  Press 'q' to stop",frame)
			#key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break
		else:
			break
		t = 1/fps-(time.time()-start)
		if t>0:
			ti -= 1/fps
			time.sleep(t)
		if ti <=0:
			break
	vid.release()
	out.release()
	cv2.destroyAllWindows()
	#with open("recordedvideo.pkl","wb") as f:
	#	pickle.dump(recording,f)
def play(filename1,filename2,filename3):
	videos = [cv2.VideoCapture(filename1),cv2.VideoCapture(filename2),cv2.VideoCapture(filename3)]
	for vid in videos:
		while(vid.isOpened()):
			start = time.time()
			ret,frame = vid.read()
			if ret:
				cv2.imshow("Playing "+str(filename),frame)
				key = cv2.waitKey(1) & 0xFF
				if key == ord('q'):
					break
			else:
				break
			t = 1/fps-(time.time()-start)
			if t>0:
				time.sleep(t)

#for i in range(3):
#	record("recordedvideo_"+str(i)+".avi")
#for i in range(3):
play("recordedvideo_0.avi","recordedvideo_1.avi","recordedvideo_2.avi")