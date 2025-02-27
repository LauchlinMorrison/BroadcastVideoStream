import cv2
import numpy as np
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

            # Detection pipeline
            modifiedFrame = frame
            modifiedFrame = cv2.cvtColor(modifiedFrame, cv2.COLOR_BGR2GRAY)
            modifiedFrame = cv2.blur(modifiedFrame, (10, 10))

            circles = cv2.HoughCircles(modifiedFrame, 
                cv2.HOUGH_GRADIENT, 
                1, 
                20, 
                param1=100, 
                param2=30, 
                minRadius=50, 
                maxRadius=100)


            if circles is not None:
                detected_circles = np.uint16(np.around(circles))

                for pt in detected_circles[0, :]:
                    a, b, r = pt[0], pt[1], pt[2]
            
                    # Draw OD
                    cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

                    #Draw center point.
                    cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

                    text = f"(x={a}, y={b}, r={r})"
                    cv2.putText(frame, text, (a+r, b-r), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
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