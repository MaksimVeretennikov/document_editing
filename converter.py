from PyPDF2 import PdfFileReader, PdfFileWriter
import os
import sys

import tkinter as tk
from tkinter import filedialog

input_path = ''

def get_path():
    if getattr(sys, 'frozen', False) :
        caminho = os.path.abspath(sys.executable).replace('converter', '')
    else:
        caminho = os.path.abspath(__file__).replace('converter.py', '')
    return caminho

def convert(path):
    path_to_dir = get_path()
    white_path = path_to_dir + 'white_cover.pdf'
    nkdc_path = path_to_dir + 'merger.pdf'

    watermark = PdfFileReader(open(white_path, "rb")) # все белые фоны
    nkdc_description = PdfFileReader(open(nkdc_path, "rb")) # надписи и эмблемы

    input_file = PdfFileReader(path)
    output_file = PdfFileWriter()

    page_count = input_file.getNumPages()

    for page_number in range(page_count):
        print("Watermarking page {} of {}".format(page_number, page_count))
        # merge the watermark with the page
        input_page = input_file.getPage(page_number)
        input_page.mergePage(watermark.getPage(0))
        input_page.mergePage(nkdc_description.getPage(0))
        # add page from input file to output document
        output_file.addPage(input_page)

    output_path = path_to_dir + 'document-output.pdf'
    with open(output_path, "wb") as outputStream:
        output_file.write(outputStream)

def browseFiles():
    global input_path
    filename = filedialog.askopenfilename(initialdir = "Users/maksimveretennikov",
                                          title = "Select a File",
                                          filetypes = [('pdf file', '*.pdf')])
      
    # Change label contents
    convert(filename)
    
    label_file_explorer.configure(text="File Converted: "+filename)

# Create the root window
window = tk.Tk()
  
# Set window title
window.title('Меняем отчет')
  
# Set window size
window.geometry("700x500")
  
#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_file_explorer = tk.Label(window,
                            text = "Выбирайте файл, аспирантики",
                            width = 100, height = 4,
                            fg = "blue")
  
      
button_explore = tk.Button(window,
                        text = "Browse Files",
                        command = browseFiles)

label_file_explorer.pack()

button_explore.pack()

window.mainloop()
