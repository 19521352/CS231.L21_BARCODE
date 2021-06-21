import numpy as np
import cv2


img_path = "images5.jpg"

def detect(img_path):
    # load the image and convert it to grayscale
    image = cv2.imread(img_path)
    out = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #cv2.imshow("Input", image)
    
    # compute the Scharr gradient magnitude representation of the images
    gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
    gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
    
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    
    
    
    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    
    
    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    
    # perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations = 4)
    closed = cv2.dilate(closed, None, iterations = 4)
    
    # find the contours in the thresholded image, then sort the contours
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
    
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    
    #drawContours
    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
    #cv2.imshow("ImageWithContours", image)
    
    
    # Create mask where white is what we want, black otherwise
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [box], -1, 255, 3)
    #cv2.imshow("mask", mask)
    
    
    
    
    # Now crop
    (y, x) = np.where(mask == 255)
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))
    out = out[topy:bottomy+1, topx:bottomx+1]
    
    
    out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    (_, out) = cv2.threshold(out, 200, 255, cv2.THRESH_BINARY)
    
    
    #cv2.imshow('Output', out)
    cv2.imwrite('ROI.png', out)
    cv2.imwrite('ImageWithContours.png', image)
    imgout_path="./ROI.png"
    imgout_path2="./ImageWithContours.png"
    cv2.waitKey(0)
    return imgout_path,imgout_path2
    
#detect(img_path)