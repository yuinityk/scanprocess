import numpy as np
import cv2

def main():
    read = cv2.imread('test.jpg',1)
    h, w, ch = read.shape
    
    # create margin
    img = np.zeros((h+20,w+20,ch))
    img[10:10+h,10:10+w] = read

    # thresholding
    thresh = 127
    img_gray = cv2.imread('test.jpg',0)
    th = np.zeros((h+20,w+20),dtype=np.uint8)
    th[10:10+h,10:10+w] = img_gray
    ret, th2 = cv2.threshold(th,127,255,cv2.THRESH_BINARY)

    # get paper area
    contours, hierarchy = cv2.findContours(th,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxarea = 0
    for c in contours:
        if cv2.contourArea(c) > maxarea:
            maxc = c
            maxarea = cv2.contourArea(c)
    cv2.drawContours(img,maxc,-1,(0,0,255),4)

    cv2.imwrite('output.jpg',img)


if __name__ == '__main__':
    main()
