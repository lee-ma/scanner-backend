from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

def scan(img):
  image = cv2.imread(img)
  ratio = image.shape[0] / 500.0
  original_img = image.copy()
  image = imutils.resize(image, height = 500)

  grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  grayscale_img = cv2.GaussianBlur(grayscale_img, (5, 5), 0)
  edged = cv2.Canny(grayscale_img, 75, 200)

  contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  #OpenCV 2.4, 3 and 4 return contours differently, so we have to process them with imutils
  contours = imutils.grab_contours(contours)
  # Sort contours by area, and then only keep the largest ones
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

  for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)

    print(len(approx))

    if len(approx) == 4:
      screenContours = approx
      break

  warped = four_point_transform(original_img, screenContours.reshape(4, 2) * ratio)

  warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
  threshold = threshold_local(warped, 11, offset=10, method="gaussian")
  warped = (warped > threshold).astype("uint8") * 255

  cv2.imshow("Original", imutils.resize(original_img, height=650))
  cv2.imshow("Scanned", imutils.resize(warped, height=650))
  cv2.waitKey(0)
