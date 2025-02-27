import cv2
import time

def display(queue, windowTitle):
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
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

            rows, cols = map(int, frame.shape[:2])

            # Perform transformation           
            ratio = 0.2
            modifiedFrame = cv2.resize(frame,
                (0,0),
                fx=ratio, 
                fy=ratio, 
                interpolation=cv2.INTER_NEAREST)
            


            # Add fps to frame
            cv2.putText(modifiedFrame, f"FPS: {fps}", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)

            cv2.imshow(f'{windowTitle}', modifiedFrame)
            cv2.resizeWindow(windowTitle, cols, rows) # There's a bug here if we close the window without ending the application.
            
            # Press ESC key or close window to stop consumer.
            if cv2.waitKey(1) == 27:
                break
            if cv2.getWindowProperty(windowTitle ,cv2.WND_PROP_VISIBLE) < 1:
                break

    cv2.destroyAllWindows()
    print("Downsample Closed")