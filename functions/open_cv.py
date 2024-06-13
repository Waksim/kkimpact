import cv2 as cv
# import numpy as np

#
# template = cv2.imread('img/temp2.png', cv2.IMREAD_GRAYSCALE)
import numpy as np

img = cv.imread('../img/deck.jpeg')

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img = cv.Canny(img, 300, 300)

# kernel = np.ones((5, 5), np.uint8)

# img = cv.dilate(img, kernel, iterations=1)
# img = cv.erode(img, kernel, iterations=1)

cv.imshow('res', img)
cv.waitKey(0)