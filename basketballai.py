import math
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture('Videos/vid (4).mp4')  # Replace with your video path

# Define ball color values (replace with appropriate values for your ball)
hsvVals = (0, 150, 100), (10, 255, 255)  # Example for a green ball

# Create color finder object
myColorFinder = ColorFinder(hsvVals)

posListX = []
posListY = []

while True:
   success, img = cap.read()

   if not success:
       break  # End of video

   # Find ball mask (replace missing part with actual ball detection code)
   imgColor, mask = ...  # Code to create mask based on ball color

   # Update color finder and find contours
   myColorFinder.update(img, hsvVals)
   imgContours, contours = cvzone.findContours(img, mask, minArea=500)

   for cnt in contours:
       posListX.append(contours[0]['center'][0])
       posListY.append(contours[0]['center'][1])

   # Display results
   imgContours = cv2.resize(imgContours, (800, 600), None, 0.7, 0.7)
   cv2.imshow("Image", imgContours)
   cv2.waitKey(1)

# Release resources
cap.release()
cv2.destroyAllWindows()
