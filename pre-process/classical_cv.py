# Run using python3 classical_cv.py --image landsat.png, tap on any key to show the next window
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

# initialize OpenCV's static saliency spectral residual detector and compute 
# the saliency map
saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
(success, saliencyMap) = saliency.computeSaliency(image)
saliencyMap = (saliencyMap * 255).astype("uint8")
threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

edged = cv2.Canny(threshMap, 30, 200)
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cv2.imshow('Canny Edges After Contouring', edged) 
cv2.waitKey(0) 
  
print("Number of Contours found = " + str(len(contours)))

for i in range(len(contours)):
    if (True): 
        approx = cv2.approxPolyDP(contours[i], 0.009 * cv2.arcLength(contours[i], True), True)
        cv2.drawContours(image, [contours[i]], -1, (0, 255, 0), 3) 

        n = approx.ravel()
        i = 0

        for j in n:
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]

                # String containing the co-ordinates. 
                string = str(x) + " " + str(y)  
    
                if(i == 0): 
                    # text on topmost co-ordinate. 
                    cv2.putText(image, "Arrow tip", (x, y), 
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))  
                else: 
                    # text on remaining co-ordinates. 
                    cv2.putText(image, string, (x, y),  
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))  
            i = i + 1

# cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
  
cv2.imshow('Contours', image) 
cv2.waitKey(0) 

cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.imshow("Thresh", threshMap)
cv2.waitKey(0)

cv2.destroyAllWindows() 

# # initialize OpenCV's static fine grained saliency detector and
# # compute the saliency map
# saliency = cv2.saliency.StaticSaliencyFineGrained_create()
# (success, saliencyMap) = saliency.computeSaliency(image)

# # if we would like a *binary* map that we could process for contours,
# # compute convex hull's, extract bounding boxes, etc., we can
# # additionally threshold the saliency map
# threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,
# 	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# # show the images
# cv2.imshow("Image", image)
# cv2.imshow("Output", saliencyMap)
# cv2.imshow("Thresh", threshMap)
# cv2.waitKey(0)
