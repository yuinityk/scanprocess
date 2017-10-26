import numpy as np
import cv2

def transform_by4(img,points):
    #input: img:array of image, points: array[4]
    #output: array of image
    # https://blanktar.jp/blog/2015/07/python-opencv-crop-box.html

    points = sorted(points, key=lambda x:x[1])
    top = sorted(points[:2], key=lambda x:x[0])
    bottom = sorted(points[2:], key=lambda x:x[0], reverse=True)
    points = np.array(top+bottom, dtype='float32')

    width = max(np.sqrt(((points[0][0]-points[2][0])**2)*2), np.sqrt(((points[1][0]-points[3][0])**2)*2))
    height = max(np.sqrt(((points[0][1]-points[2][1])**2)*2), np.sqrt(((points[1][1]-points[3][1])**2)*2))

    dst = np.array([
        np.array([0,0]),
        np.array([width-1,0]),
        np.array([width-1,height-1]),
        np.array([0,height-1]),
        ], np.float32)

    trans = cv2.getPerspectiveTransform(points,dst)
    return cv2.warpPerspective(img, trans, (int(width), int(height)))


def main():
    read = cv2.imread('test.png',1)
    h, w, ch = read.shape
    
    # create margin
    img = np.zeros((h+20,w+20,ch))
    img[10:10+h,10:10+w] = read

    # thresholding
    thresh = 200
    img_gray = cv2.imread('test.png',0)
    th = np.zeros((h+20,w+20),dtype=np.uint8) #should be np.uint8 to avoid error
    th[10:10+h,10:10+w] = img_gray
    ret, th2 = cv2.threshold(th,thresh,255,cv2.THRESH_BINARY)
    cv2.imwrite('th2.png',th2)

    # get paper area
    contours, hierarchy = cv2.findContours(th2,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    paperContour = sorted(contours,key=cv2.contourArea,reverse=True)[0]
    epsilon = 0.1*cv2.arcLength(paperContour,True)
    approx = cv2.approxPolyDP(paperContour,epsilon,True)
    cv2.drawContours(img,approx,-1,(0,0,255),10)
    warped = transform_by4(img, approx[:,0,:])
    cv2.imwrite('warp.png',warped)
    cv2.imwrite('output.png',img)


if __name__ == '__main__':
    main()
