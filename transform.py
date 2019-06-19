import numpy as np
import cv2

def order_points(pts):
  # list of coordinates where 
  # first entry is top-left
  # second entry is top-right
  # third bottom-right
  # fourth bottom-left
  rect = np.zeros((4,2), dtype = "float32")

  # top-left point will have smallest sum, bottom-right largest
  s = pts.sum(axis=1)
  rect[0] = pts[np.argmin(s)]
  rect[2] = pts[np.argmax(s)]

  #compute difference between points
  diff = np.diff(pts, axis = 1)
  rect[1] = pts[np.argmin(diff)]
  rect[3] = pts[np.argmax(diff)]

  return rect

def get_birds_eye_view(maxWidth, maxHeight):
  return np.array([
    [0, 0], #top left
    [maxWidth - 1, 0], #top right
    [maxWidth - 1, maxHeight - 1], #bottom right
    [0, maxHeight - 1] #bottom left
  ], dtype="float32")

def four_point_transform(image, pts):
  rect = order_points(pts)
  (tl, tr, br, bl) = rect

  #compute width of new image, will be max distance between br and bl x-coordiantes or tr and tl using pythagoras
  widthBottom = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  widthTop = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWidth = max(int(widthBottom), int(widthTop))

  #compute height of new image
  heightRight = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  heightLeft = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHeight = max(int(heightRight), int(heightLeft))

  destination_pts = get_birds_eye_view(maxWidth, maxHeight)

  #compute perspective transform matrix and apply
  perspective_transform_matrix = cv2.getPerspectiveTransform(rect, destination_pts)
  warped_img = cv2.warpPerspective(image, perspective_transform_matrix, (maxWidth, maxHeight))

  return warped_img

  