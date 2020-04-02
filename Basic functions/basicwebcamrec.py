import cv2
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
foutput = cv2.VideoWriter('Recording.avi', fourcc, 24.0, (640,480))
while True:
    ret, color_recording = cap.read()
    foutput.write(color_recording)
    ('Color recording',color_recording)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      cap.release()
      break
foutput.release()
cv2.destroyAllWindows()


