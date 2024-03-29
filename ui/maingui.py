#https://www.youtube.com/watch?v=ZNrteLp_SvY
import cv2
import numpy as np
import pytesseract
import argparse
from pdf2image import convert_from_path
import the_better_ui

image_path = ""

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #don't want to mess around with PATH

#--------------------------------------------------------------------------------------------------------------------------------
def run(image_path,gray, adapt, denoise, box, oem, psm): #mainloop for preprocessing
    if denoise and gray and adapt: 
        imageG = get_grayscale(image_path)
        imageT = get_adaptive_threshold(imageG)
        imageN = cv2.medianBlur(imageT,5)
        cv2.imshow('Result', imageN) #show image
        cv2.waitKey(0) #wait for keypress
        postprocessing(post = imageN, psm = psm, oem = oem) #send for postprocessing
        
        
    elif gray and adapt:
        imageG = get_grayscale(image_path)
        imageT = get_adaptive_threshold(imageG)
        cv2.imshow('Result', imageT)
        cv2.waitKey(0)
        postprocessing(post = imageT, psm = psm, oem = oem)
    elif adapt and gray == False:
        print("Error pass in --gray before attempting to use Adaptive Thresholding ")
    elif gray:
        imageG = get_grayscale(image_path)
        cv2.imshow('Result', imageG)
        cv2.waitKey(0)
        postprocessing(post = imageG, psm = psm, oem = oem)
    elif denoise: 
        imageB = cv2.medianBlur(image_path,5)
        cv2.imshow('Result', imageB)
        cv2.waitKey(0)
        postprocessing(post = imageB, psm = psm, oem = oem)
    else: 
        postprocessing(image_path, psm = psm, oem = oem)
    if box: 
        bounding_box_words_only(image_path) #can't add gray/thresholded image, boxing needs 3 values
#--------------------------------------------------------------------------------------------------------------------------------        
def get_adaptive_threshold(imageG): #3 different settings for adaptive thresholding 
    blurred = cv2.GaussianBlur(imageG, (7, 7), 0) #slightly blur image
    threshO = cv2.adaptiveThreshold(imageG, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11) #original thresholding values
    threshM = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10) #adaptive thresholding using mean
    threshG = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4) #gaussian thresholding 
    return threshO #return default thresholder 
#--------------------------------------------------------------------------------------------------------------------------------
def get_grayscale(image_path):#convert image to grayscale
    return cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
#--------------------------------------------------------------------------------------------------------------------------------
def postprocessing(post, psm, oem): #postprocessing for OCR
    conf = fr'--oem {oem} --psm {psm}'  #Legacy + LSTM engines with Automatic page segmentation with OSD.
    #start with psm 3 as a baseline
    #psm 13 is last resort where is randomly starts detecting everything
    global result
    result = pytesseract.image_to_string(post, lang='eng') #convert image to string\
    #, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.:, " 
    print("\n" "RESULT ---------------------------------------------------------- \n"+ result + "\n-----------------------------------------------------------------") #beautify this later with GUI

def get_result():
    return result
#--------------------------------------------------------------------------------------------------------------------------------
#def bounding_box_characters_only(image): #add to cmd
#    hImg,wImg,_ = image.shape
#    box_coords = pytesseract.image_to_boxes(image) #length, width, diagonal 1, diagonal 2
#    #print(box_coords) 
#    for box in box_coords.splitlines():
#        box = box.split(' ')
#        x,y,d1,d2 = int(box[1]),int(box[2]),int(box[3]),int(box[4])
#        cv2.rectangle(image, (x,hImg-y), (d1,hImg-d2), (3, 252, 28), int(1.5)) #image, xy, diagonals, color of box, thickness of box
#        cv2.putText(image, box[0], (x,hImg-y+12), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
#    cv2.imshow('Result', image)
#    cv2.waitKey(0)
#--------------------------------------------------------------------------------------------------------------------------------
def bounding_box_words_only(local_image_path): #bouding boxes around detected words only
    hImg,wImg,_ = local_image_path.shape
    box_coords = pytesseract.image_to_data(local_image_path) #length, width, diagonal 1, diagonal 2
    #print(box_coords) 
    for x,box in enumerate(box_coords.splitlines()):
        if x!= 0:
            box = box.split()
            if len(box) == 12: #any list with length of 12 is a word
                x,y,d1,d2 = int(box[6]),int(box[7]),int(box[8]),int(box[9])
                cv2.rectangle(local_image_path, (x,y), (d1+x,d2+y), (3, 252, 28), int(1.5)) #bruh they have different xy formats for characters and words :/
                cv2.putText(local_image_path, box[11], (x,y+35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
    cv2.imshow('Result', local_image_path)
    cv2.waitKey(0)
    
    
#--------------------------------------------------------------------------------------------------------------------------------
def default_settings(fname): #default settings for OCR
    image_input_path = fname
    gray = False
    adapt = False
    denoise = False
    box = True
    psm = 3
    oem = 1
    filecheck(image_input_path, gray, adapt, denoise, box, oem, psm)
    
def filecheck(image_input_path,gray, adapt, denoise, box, oem, psm):  #check if file exists
    if image_input_path.endswith('.pdf'):
        pages = convert_from_path(image_input_path, 350, poppler_path=r'C:/Program Files/poppler-0.68.0/bin') #screw env variables
        i = 1
        for page in pages: #loop through all pages and magically convert them into jpegs
            image_name = "Page_" + str(i) + ".jpg"  
            page.save(f"frompdf/{image_name}", "JPEG") #save image to folder
            image_path = cv2.imread(f"frompdf/{image_name}")  #read image
            run(image_path,gray, adapt, denoise, box, oem, psm) #run OCR on image
            i = i+1
    else:
        image_path = cv2.imread(image_input_path)
        run(image_path,gray, adapt, denoise, box, oem, psm)
#--------------------------------------------------------------------------------------------------------------------------------


