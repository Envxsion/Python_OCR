#https://www.youtube.com/watch?v=ZNrteLp_SvY
import cv2
import numpy as np
import pytesseract
import argparse


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #remember to find executable before run it

def command_line():
    # Create the parser
    parser = argparse.ArgumentParser()
    
    #arguments with help statements
    parser.add_argument('--image', type=str, help='Path to the image to be scanned', required=True)
    parser.add_argument('--gray', help='Turn image gray for better detection', action='store_true')
    parser.add_argument('--at', help='Adaptive thresholding on grayscale image (requires --gray)', action='store_true')
    parser.add_argument('--denoise', help='Denoise the image for better detection', action='store_true')
    args = parser.parse_args()
    image_path = cv2.imread(args.image)
    if args.denoise and args.gray and args.at:
        imageG = get_grayscale(image_path)
        imageT = cv2.adaptiveThreshold(imageG, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11)
        imageN = cv2.medianBlur(imageT,5)
        cv2.imshow('Result', imageN)
        cv2.waitKey(0)
        post = imageN
        postprocessing(post)
    elif args.gray and args.at:
        imageG = get_grayscale(image_path)
        imageT = cv2.adaptiveThreshold(imageG, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11)
        cv2.imshow('Result', imageT)
        cv2.waitKey(0)
        post = imageT
        postprocessing(post)
    elif args.at and args.gray == False:
        print("Error pass in --gray before attempting to use Adaptive thresholding ")
    elif args.gray:
        imageG = get_grayscale(image_path)
        cv2.imshow('Result', imageG)
        cv2.waitKey(0)
        post = imageG
        postprocessing(post)
    elif args.denoise: 
        imageb = cv2.medianBlur(image_path,5)
        cv2.imshow('Result', imageb)
        cv2.waitKey(0)
        post = imageb
        postprocessing(post)
    else: 
        postprocessing(image_path)
    #bounding_box_words_only(image_path) #can't add gray/thresholded image, boxing needs 3 values

# get grayscale image
def get_grayscale(image_path):
    return cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)


def postprocessing(post):
    result = pytesseract.image_to_string(post, lang='eng') #convert image to string
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

def bounding_box_words_only(image_path): #add to cmd
    hImg,wImg,_ = image_path.shape
    box_coords = pytesseract.image_to_data(image_path) #length, width, diagonal 1, diagonal 2
    #print(box_coords) 
    for x,box in enumerate(box_coords.splitlines()):
        if x!= 0:
            box = box.split()
            if len(box) == 12: #any list with length of 12 is a word
                x,y,d1,d2 = int(box[6]),int(box[7]),int(box[8]),int(box[9])
                cv2.rectangle(image_path, (x,y), (d1+x,d2+y), (3, 252, 28), int(1.5)) #bruh they have different xy formats for characters and words :/
                cv2.putText(image_path, box[11], (x,y+35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (19, 104, 240), int(1.5), cv2.LINE_AA) #image, text, xy, font, size, color, thickness, line type
    cv2.imshow('Result', image_path)
    cv2.waitKey(0)


command_line()
#bounding_box_characters_only(image)
