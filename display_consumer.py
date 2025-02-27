import cv2
import time

def display(queue, windowTitle):
    prevFrameTime = 0
    frameTime = 0

    while True:
        if not queue.empty():
            frame = queue.get()

            # Determine FPS.
            frameTime = time.time()
            deltaTime = frameTime-prevFrameTime
            prevFrameTime = frameTime
            fps = int(1/deltaTime)

            # Add fps to frame
            cv2.putText(frame, f"FPS: {fps}", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)

            cv2.imshow(f'{windowTitle}', frame)
            
            # Press ESC key or close window to stop consumer.
            if cv2.waitKey(1) == 27:
                break
            if cv2.getWindowProperty(windowTitle ,cv2.WND_PROP_VISIBLE) < 1:
                break
    
    cv2.destroyAllWindows()
    print("Display Closed")