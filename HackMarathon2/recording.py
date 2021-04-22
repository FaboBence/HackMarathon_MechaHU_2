import cv2, time, numpy

fps = 25
filename = "recordedvideo.avi"

def record(filename1):#,filename2,filename3):
	vid = cv2.VideoCapture(0)
	re,fram = vid.read()
	out = cv2.VideoWriter(filename1, cv2.VideoWriter_fourcc(*'DIVX'), fps, (numpy.shape(fram)[1],numpy.shape(fram)[0]))
	ti = 10 # recording length of video to be recorded
	while(vid.isOpened()):
		start = time.time()
		ret,frame = vid.read()
		if ret == True:
			out.write(frame)
			cv2.imshow("RECORDING  Press 'q' to stop",frame)
			key = cv2.waitKey(1) & 0xFF
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
		out.release()
	vid.release()
	cv2.destroyAllWindows()
	
def play(filename1):#,filename2,filename3):
	videos = [cv2.VideoCapture(filename1)]#,cv2.VideoCapture(filename2),cv2.VideoCapture(filename3)]
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

record(filename)
play(filename)

