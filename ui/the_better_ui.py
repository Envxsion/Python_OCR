from tkinter import *
from tkinter import filedialog#For file explorer
from tkinter import scrolledtext#For scroll bar text box
import maingui

window = Tk()
window.title("PY OCR")
window.state('zoomed')
window.config(bg= "#ffffe3")


input_img = Label(window, text="Input Image", bg= "#ffffe3")
output_img = Label(window, text="Output Image", bg= "#ffffe3")
output_text = Label(window, text="Output Text", bg= "#ffffe3")
input_img.place(x= 250 , y= 5)
output_img.place(x= 250, y=450)
output_text.place(x= 1200, y=5)

input_placeholder = Label(window, text="Input Image place holder", bg= "#ffffe3", font=("Times",19))
output_placeholder = Label(window, text="Output Image place holder", bg= "#ffffe3", font=("Times",19))
input_placeholder.place(x=250 , y=200)
output_placeholder.place(x=250 , y=650)

Extract = Button(window, text="EXTRACT", bg= "Red", font=("Times",15), width= 12)
Extract.place(x=200 , y= 340)
def file1():
    file = filedialog.askopenfile(filetypes = (("Image Files","*.jpg .png .jpeg .tiff .pdf",),("All Files ","*.*")))

Browseimg = Button(window, text="Browse", command = file1, width= 12, font=("Times",15))
Browseimg.place(x=500 , y=340)


Output_text_txt = scrolledtext.ScrolledText(window,width=40,height=45)
Output_text_txt.place(x=1080 ,y=25)

def file2():
    file = filedialog.asksaveasfile(filetypes = (("Text files","*.txt"),("All Files","*.*")))

Savetxt = Button(window, text="Save TXT", command = file2, width= 12,font=("Times",15) )
Savetxt.place(x= 1350, y=780 )




window.mainloop()