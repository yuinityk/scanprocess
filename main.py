import numpy as np
import cv2

def transform_by4(img,points):
    #input: img:array of image, points: array[4]
    #output: array of image
    # https://blanktar.jp/blog/2015/07/python-opencv-crop-box.html

    points = sorted(points, key=lambda x:x[1])
    top = sorted(points[:2], key=lambda x:x[0])
    bottom = sorted(points[2:], key=lambda x:x[0], reverse=True)
    points = numpy.array(top+bottom, dtype='float32')

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
    read = cv2.imread('test.jpg',1)
    h, w, ch = read.shape
    
    # create margin
    img = np.zeros((h+20,w+20,ch))
    img[10:10+h,10:10+w] = read

    # thresholding
    thresh = 127
    img_gray = cv2.imread('test.jpg',0)
    th = np.zeros((h+20,w+20),dtype=np.uint8) #np.uint8じゃないとエラー吐く
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
