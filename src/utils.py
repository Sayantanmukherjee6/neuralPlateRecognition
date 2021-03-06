import cv2
import numpy as np
from os import listdir
from os.path import isdir, isfile, join

######################################
#			   CLASSES				 #
######################################

class Image(object):
	def __init__(self, image, f = "", key = None, descriptor = None):
		self.img = image
		self.fileName = f
		self.k = key
		self.d = descriptor
		self.cars = []

	def addCar(self, car):
		self.cars.append(car)



class Rectangle(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		
######################################
#			   FUNCTIONS			 #
######################################
def printOK():
    print "\033[92mOK!\033[0m" 
def printErrorMsg(text):
	""" Prints text to STDERR """
	print >> stderr, text
def getInput(text):
	return (raw_input(text)).strip()

#def writeToFile(file, text):
#    f = open(file, 'w')
#    f.write(text)

def showImage(img):
	cv2.imshow('Matched Features', img)
	cv2.waitKey(0)
	cv2.destroyWindow('Matched Features')
def loadImgs(path):
	""" Given a Path, converts all images to grey scale and returns a list of Image objects """
	return [Image(cv2.imread(join(path, f),0), f) for f in listdir(path) if (isfile(join(path, f)) and f.endswith('.jpg'))]
def convertTupleListToRectangleList(l_xywh):
    """ Receives a list of tuples (x,y,w,h) defining rectangles
        Returns a list of Rectangle objects
    """
    l = []
    for (x,y,w,h) in l_xywh:
        l.append(Rectangle(x,y,w,h))
    return l

#Custom drawMatches (it is not included in prior versions to 3.0 of OpenCV)
#https://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python
def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out