#https://www.youtube.com/watch?v=ZNrteLp_SvY
import cv2
import numpy as np
import pytesseract
import argparse
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #don't want to mess around with PATH

#--------------------------------------------------------------------------------------------------------------------------------
def run(image_path):        
    if args.denoise and args.gray and args.adapt:
        imageG = get_grayscale(image_path)
        imageT = get_adaptive_threshold(imageG)
        imageN = cv2.medianBlur(imageT,5)
        cv2.imshow('Result', imageN)
        cv2.waitKey(0)
        postprocessing(post = imageN)
    elif args.gray and args.adapt:
        imageG = get_grayscale(image_path)
        imageT = get_adaptive_threshold(imageG)
        cv2.imshow('Result', imageT)
        cv2.waitKey(0)
        postprocessing(post = imageT)
    elif args.adapt and args.gray == False:
        print("Error pass in --gray before attempting to use Adaptive Thresholding ")
    elif args.gray:
        imageG = get_grayscale(image_path)
        cv2.imshow('Result', imageG)
        cv2.waitKey(0)
        postprocessing(post = imageG)
    elif args.denoise: 
        imageB = cv2.medianBlur(image_path,5)
        cv2.imshow('Result', imageB)
        cv2.waitKey(0)
        postprocessing(post = imageB)
    else: 
        postprocessing(image_path)
    if args.box: 
        bounding_box_words_only(image_path) #can't add gray/thresholded image, boxing needs 3 values
#--------------------------------------------------------------------------------------------------------------------------------        
def get_adaptive_threshold(imageG):
    blurred = cv2.GaussianBlur(imageG, (7, 7), 0) #slightly blur image
    threshO = cv2.adaptiveThreshold(imageG, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 91, 11) #original thresholding values
    threshM = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10) #adaptive thresholding using mean
    threshG = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4) #gaussian thresholding 
    return threshO
#--------------------------------------------------------------------------------------------------------------------------------
def get_grayscale(image_path):
    return cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
#--------------------------------------------------------------------------------------------------------------------------------
def postprocessing(post):
    conf = r'--oem 3 --psm 2'
    result = pytesseract.image_to_string(post, lang='eng') #convert image to string
    #, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.:, " 
    print("\n" "RESULT ---------------------------------------------------------- \n"+ result + "\n-----------------------------------------------------------------") #beautify this later with GUI
#--------------------------------------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------------------------------------
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
#--------------------------------------------------------------------------------------------------------------------------------
# Create the command line parser
parser = argparse.ArgumentParser(description='This program may have to be run multiple times with different arguments to get the desired output') 
#--------------------------------------------------------------------------------------------------------------------------------
#arguments with help statements (accessed by -h or -help)
parser.add_argument('-i','--image', type=str, help='Path to the image to be scanned')
parser.add_argument('-g','--gray', help='Turn image gray for better detection', action='store_true')
parser.add_argument('-at','--adapt', help='Adaptive thresholding on grayscale image (requires --gray)', action='store_true')
parser.add_argument('-d','--denoise', help='Denoise the image for better detection', action='store_true')
parser.add_argument('-p','--pdf', type=str, help='Convert pdf to images')
parser.add_argument('-b','--box', help="Bounding box around words (Doesn't work with any image modifications, trying to fix this)", action='store_true')
parser.add_argument('-tb','--extractable', help="Extract table(s) from image", action='store_true')
#--------------------------------------------------------------------------------------------------------------------------------
args = parser.parse_args()
if args.pdf:
    pages = convert_from_path(args.pdf, 350, poppler_path=r'C:/Program Files/poppler-0.68.0/bin') #screw env variables
    i = 1
    for page in pages: #loop through all pages and magically convert them into jpegs
        image_name = "Page_" + str(i) + ".jpg"  
        page.save(f"frompdf/{image_name}", "JPEG")
        image_path = cv2.imread(f"frompdf/{image_name}") 
        run(image_path)
        i = i+1
else:
    image_path = cv2.imread(args.image)
    run(image_path)
#--------------------------------------------------------------------------------------------------------------------------------
