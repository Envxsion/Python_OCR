#https://www.youtube.com/watch?v=ZNrteLp_SvY
import cv2
import numpy as np
import pytesseract
import argparse


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #remember to find executable before run it
#image = cv2.imread('images/ocr-test-1.png')
#image = cv2.imread('images/test2.png')
#image = cv2.imread('images/Inkedtest1.jpg')

def command_line():
    # Create the parser
    parser = argparse.ArgumentParser()
    
    #arguments with help statements
    parser.add_argument('--image', type=str, help='Path to the image to be scanned', required=True)
    parser.add_argument('--gray', help='Turn image gray for better detection', action='store_true')
    parser.add_argument('--denoise', help='Denoise the image for better detection', action='store_true')
    args = parser.parse_args()
    image_path = cv2.imread(args.image)
    if args.denoise and args.gray:
        imageg = get_grayscale(image_path)
        imaged = remove_noise(imageg)
        cv2.imshow('Result', imaged)
        cv2.waitKey(0)
        postprocessing(imaged)
    elif args.gray:
        imagea = get_grayscale(image_path)
        cv2.imshow('Result', imagea)
        cv2.waitKey(0)
        postprocessing(imagea)
    elif args.denoise: 
        imageb = remove_noise(image_path)
        cv2.imshow('Result', imageb)
        cv2.waitKey(0)
        postprocessing(imageb)

# get grayscale image
def get_grayscale(image_path):
    return cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image_path):
    return cv2.medianBlur(image_path,5)


def postprocessing(image_path):
    result = pytesseract.image_to_string(image_path, lang='eng') #convert image to string
    print(result) #beautify this later with GUI

def bounding_box_characters_only(image): #add to cmd
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

def bounding_box_words_only(image): #add to cmd
    hImg,wImg,_ = image.shape
    box_coords = pytesseract.image_to_data(image) #length, width, diagonal 1, diagonal 2
    #print(box_coords) 
    for x,box in enumerate(box_coords.splitlines()):
        if x!= 0:
            box = box.split()
            if len(box) == 12: #any list with length of 12 is a word
                x,y,d1,d2 = int(box[6]),int(box[7]),int(box[8]),int(box[9])
                cv2.rectangle(image, (x,y), (d1+x,d2+y), (3, 252, 28), int(1.5)) #bruh they have different xy formats for characters and words :/
                cv2.putText(image, box[11], (x,y+35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
    cv2.imshow('Result', image)
    cv2.waitKey(0)



command_line()
#remember to comment out either the characters or words, as they will overwrite the same image if run together (make a switch statement for this later in GUI stage)
#bounding_box_characters_only(image)
#bounding_box_words_only(image)