from consumer import Consumer
import cv2
import numpy as np

class DetectionConsumer(Consumer):
    def __init__(self, name):
        super().__init__(name,)

    # Detect circles by shifting the frame to grayscale, applying blur and searching with the HoughCircles method.
    def process_frame(self, frame):
        modifiedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

                # Draw center point.
                cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

                # Add some useful text.
                text = f"(x={a}, y={b}, r={r})"
                cv2.putText(frame, text, (a+r, b-r), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        return frame