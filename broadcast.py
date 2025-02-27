import cv2

def capture_video(source, queue):
    capture = cv2.VideoCapture(source)
    
    if not capture.isOpened():
        print("Error: Camera unavailable.")
        return
    
    fps = capture.get(cv2.CAP_PROP_FPS)
    print("FPS:", fps)
    
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        queue.put(frame)
    
    capture.release()
