#https://www.youtube.com/watch?v=ZNrteLp_SvY
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #remember to find executable before ru
#image = cv2.imread('images/ocr-test-1.png')
#image = cv2.imread('images/test2.png')
image = cv2.imread('images/Inkedtest1.jpg')

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,5)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

def fix_image(image):
    gray = get_grayscale(image) #any option
    cv2.imshow('Result', gray) #show result
    cv2.waitKey(0) #inf loop to see image until closed | WARNING: Close image to see result of postprocessing

def postprocessing(image):
    result = pytesseract.image_to_string(image, lang='eng') #convert image to string
    print(result) #beautify this later with GUI

def bounding_box_characters_only(image):
    hImg,wImg,_ = image.shape
    box_coords = pytesseract.image_to_boxes(image) #length, width, diagonal 1, diagonal 2
    #print(box_coords) 
    for box in box_coords.splitlines():
        box = box.split(' ')
        x,y,d1,d2 = int(box[1]),int(box[2]),int(box[3]),int(box[4])
        cv2.rectangle(image, (x,hImg-y), (d1,hImg-d2), (3, 252, 28), int(1.5)) #image, xy, diagonals, color of box, thickness of box
        cv2.putText(image, box[0], (x,hImg-y+12), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
    cv2.imshow('Result', image)
    cv2.waitKey(0)

def bounding_box_words_only(image): 
    hImg,wImg,_ = image.shape
    box_coords = pytesseract.image_to_data(image) #length, width, diagonal 1, diagonal 2
    #print(box_coords) 
    for x,box in enumerate(box_coords.splitlines()):
        if x!= 0:
            box = box.split()
            if len(box) == 12: #any list with length of 12 is a word
                x,y,d1,d2 = int(box[6]),int(box[7]),int(box[8]),int(box[9])
                cv2.rectangle(image, (x,y), (d1+x,d2+y), (3, 252, 28), int(1.5)) #bruh they have different xy formats for characters and words :/
                cv2.putText(image, box[11], (x,y+40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
    cv2.imshow('Result', image)
    cv2.waitKey(0)

fix_image(image)
postprocessing(image)
#remember to comment out either the characters or words, as they will overwrite the same image if run together (make a switch statement for this later in GUI stage)
#bounding_box_characters_only(image)
bounding_box_words_only(image)