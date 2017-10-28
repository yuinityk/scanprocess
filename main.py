import os
import sys
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


def trans(path,fn,ind,digit):
    '''
    input:
        path  : String , where to save converted images which ends with '/'
        fn    : Integer, number which corresponds to the input filename
        ind   : Integer, number which corresponds t0 the output filename
        digit : Integer, digit of ind in the output filename
    '''
    dirpath = '/media/cookie/5C73-1BFD/DCIM/100MEDIA/'
    inputpath = dirpath + 'IMAG{0:04d}.jpg'.format(fn)
    read = cv2.imread(inputpath,1)
    h, w, ch = read.shape
    
    # create margin
    img = np.zeros((h+20,w+20,ch))
    img[10:10+h,10:10+w] = read

    # thresholding
    thresh = 200
    img_gray = cv2.imread(inputpath,0)
    th = np.zeros((h+20,w+20),dtype=np.uint8) #should be np.uint8 to avoid error
    th[10:10+h,10:10+w] = img_gray
    ret, th2 = cv2.threshold(th,thresh,255,cv2.THRESH_BINARY)

    # get paper area
    contours, hierarchy = cv2.findContours(th2,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    paperContour = sorted(contours,key=cv2.contourArea,reverse=True)[0]
    epsilon = 0.1*cv2.arcLength(paperContour,True)
    approx = cv2.approxPolyDP(paperContour,epsilon,True)
    warped = transform_by4(img, approx[:,0,:])
    cv2.imwrite(path+str(ind).zfill(digit)+'.jpg',warped)

if __name__ == '__main__':
    if os.path.exists('image'):
        while 1:
            m = raw_input('It\'ll delete the images already existing in the image folder.OK? [y/n]') 
            if m=='y':
                for root, dirs, files in os.walk('image/',topdown=False):
                    for name in files:
                        os.remove(os.path.join(root,name))
                break
            elif m=='n':
                print('Move those files anywhere else.')
                raw_input('press any key...')
                sys.exit()
            else:
                print('Enter \'y\' or \'n\'.')
    else:
        os.mkdir('image')
    dirpath = '/media/cookie/5C73-1BFD/DCIM/100MEDIA/'
    files = os.listdir(dirpath)
    num = len(files)
    if 0 < num < 10:
        digit = 1
    elif num < 100:
        digit = 2
    else:
        digit = 3
    count = 1
    al = 1
    while count < num+1:
        if os.path.exists(dirpath+'IMAG{0:04d}.jpg'.format(al)):
            trans('image/',al,count,digit)
            count += 1
        al += 1
