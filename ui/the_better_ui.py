from tkinter import *
from tkinter import filedialog#For file explorer
from tkinter import scrolledtext
import tkinter#For scroll bar text box
from PIL import ImageTk, Image
import maingui
import re

window = Tk()
window.title("PY_OCR")
window.state('zoomed')
window.config(bg= "#ffffe3")


def browse():
    global file
    global imgI
    file = str(filedialog.askopenfile(filetypes = (("Image Files","*.jpg .png .jpeg .tiff .pdf",),("All Files ","*.*")))).split()
    print(file)
    regex = re.findall(r'.*?\'(.*)\'.*', file[1]) #regex to find everything in quotes
    regex = re.sub(r"[\[\]]",'', regex[0]) #regex to remove sqaure brackets
    file = str(regex)
    if file.endswith(".pdf"):
        #couldn't get this part to work due to circular imports
        pass
            
    else:
        imgI = ImageTk.PhotoImage(Image.open(str(file))) #open image
        imgI = imgI._PhotoImage__photo.subsample(2) #resize it to make it 2x smaller
        input_placeholder.configure(image=imgI) #configure the image to the input placeholder
    print(str(file))
    
    
def extract():
    
    print(str(file))
    fname = file
    maingui.default_settings(fname) #use imported backend
    txtsave = maingui.get_result()
    print(txtsave)
    Output_text_txt.insert(tkinter.INSERT, txtsave )
    
def savetxt():
    file = filedialog.asksaveasfile(filetypes = (("Text files","*.txt"),("All Files","*.*")),initialfile = 'ocr_save.txt',initialdir='ui')
    
input_img = Label(window, text="Input Image (Note: pdf's will not be shown here)", bg= "#ffffe3")
output_img = Label(window, text="Output Image will open in a new window... ", bg= "#ffffe3")
output_text = Label(window, text="Output Text [The text in the window below can be edited]", bg= "#ffffe3")
input_img.place(x= 250 , y= 5)
output_img.place(x= 250, y=600)
output_text.place(x= 1100, y=5)

imgI = ImageTk.PhotoImage(Image.open("ui/assets/placeholder.jpg"))
imgO = ImageTk.PhotoImage(Image.open("ui/assets/placeholder2.jpg"))

input_placeholder = Label(window, image=imgI, bg= "#ffffe3")
input_placeholder.pack(side="bottom", fill="both", expand="yes")
input_placeholder.place(x=250 , y=50)

output_placeholder = Label(window, image=imgO, bg= "#ffffe3")
output_placeholder.pack(side="bottom", fill="both", expand="yes")
output_placeholder.place(x=250 , y=650)

Extract = Button(window, text="EXTRACT", bg= "Red", font=("Times",15), width= 12,command = extract )
Extract.place(x=200 , y= 500)


Browseimg = Button(window, text="Browse", command = browse, width= 12, font=("Times",15))
Browseimg.place(x=500 , y=500)


Output_text_txt = scrolledtext.ScrolledText(window,width=40,height=45)
Output_text_txt.place(x=1080 ,y=25)


Savetxt = Button(window, text="Save TXT", command = savetxt, width= 12,font=("Times",15) )
Savetxt.place(x= 1350, y=780 )




window.mainloop()