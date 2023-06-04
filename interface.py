import os
import dataParser
import rubricator
import visualizator
from tkinter import *
from tkinter import filedialog
from customtkinter import CTkComboBox, CTkButton
from tkinter.messagebox import showwarning, showinfo


file_path = ''
myColor = '#528CCA'
hoverColor = '#46719C'


def parserWindow():
    parsWindow = Toplevel()
    parsWindow.title("Article Rubrication System")
    parsWindow.geometry('400x200')
    parsWindow.iconphoto(False, icon)
    parsWindow.grab_set()
    parsWindow.iconphoto(False, icon)
    c = parseCB.get()
    if c == 'PDF-parsing':
        Label(parsWindow, text='Enter the full path to the folder you want to parse:', font=("Arial", 9)).pack(anchor=NW, pady=(20, 10), padx=20)
        path = Label(parsWindow, width=300, text='', justify=LEFT, background='white', font=("Arial", 9), borderwidth=1, relief="solid")
        path.pack(anchor=W, pady=(0, 10), padx=20)
        CTkButton(parsWindow, text='Select Folder...', command=lambda: chooseFile(path)).pack(anchor=SW, padx=20)
        Button(parsWindow, text="OK", font=("Arial", 11, 'bold'), border=0, padx=10, fg=myColor,
               command=lambda: checkParser(file_path), activeforeground=hoverColor).pack(side=RIGHT)
    elif c == 'Web-parsing':
        Label(parsWindow, text='Enter the link of the website to parse:', font=("Arial", 9)).pack(anchor=NW, pady=(20, 10), padx=20)
        link = Entry(parsWindow, width=300, text='', justify=LEFT, background='white', font=("Arial", 9), borderwidth=1, relief="solid")
        link.pack(anchor=W, pady=(0, 10), padx=20)
        Button(parsWindow, text="OK", font=("Arial", 11, 'bold'), border=0, padx=10, fg=myColor,
               command=lambda: checkParser(link.get()), activeforeground=hoverColor).pack(side=RIGHT)
    Button(parsWindow, text="CANCEL", font=("Arial", 11, 'bold'), border=0, padx=10, fg=myColor, activeforeground=hoverColor, command=parsWindow.destroy).pack(side=RIGHT)


def chooseFile(path):
    global file_path
    file_path = filedialog.askdirectory()
    path['text'] = file_path
    return 1


def checkParser(path):
    parserType = parseCB.get()
    res = dataParser.getRequest(parserType, path)
    if res == 1:
        showinfo(title='Information', message='Successfully')
    else:
        showwarning(title="Warning", message=res)
    return 1


def checkFile():
    if not os.path.exists('data.csv'):
        showwarning(title="Warning", message="Data file does not exist, please parse data first")
    else:
        clusterType = clCB.get()
        res = rubricator.rubrication(clusterType)
        if res == 1:
            showinfo(title='Information', message='Successfully')
        else:
            showwarning(title="Warning", message=res)
    return 1


def checkCluster():
    if not os.path.exists('website/data.json'):
        showwarning(title="Warning", message="Data file does not exist, please parse data before clustering")
    else:
        visType = visCB.get()
        res = visualizator.visualize(visType)
        if res == 1:
            showinfo(title='Information', message='Successfully')
        else:
            showwarning(title="Warning", message=res)
    return 1


window = Tk()
window.title("Article Rubrication System")
window.geometry('500x320')
icon = PhotoImage(file="icon.png")
window.iconphoto(False, icon)
window.configure(bg='white')

Label(window, text='Select the parsing type:', background='white', font=("Arial", 11)).grid(row=0, column=0, pady=(20, 10), padx=(0, 0))
parseCB = CTkComboBox(window, width=200, height=40, border_width=1, corner_radius=8, font=("Arial", 14), fg_color='white',
    text_color='black', values=['PDF-parsing', 'Web-parsing'], button_color=myColor, button_hover_color=hoverColor, dropdown_fg_color='white', dropdown_hover_color=myColor, dropdown_font=("Arial", 14))
parseCB.grid(row=1, column=0, padx=(30, 10), pady=(0, 0))
CTkButton(window, text="Start parsing", command=parserWindow, width=200, height=40, border_width=0, corner_radius=8, font=("Arial", 14))\
    .grid(row=1, column=1, padx=(10, 30), pady=(0, 0))

Label(window, text='Select the clustering algorithm:', background='white', font=("Arial", 11)).grid(row=2, column=0, pady=(20, 10), padx=(30, 0))
clCB = CTkComboBox(window, width=200, height=40, border_width=1, corner_radius=8, font=("Arial", 14), fg_color='white', text_color='black', values=['Hierarchical clustering', 'K-Means clustering'], button_color=myColor, button_hover_color=hoverColor, dropdown_fg_color='white', dropdown_hover_color=myColor, dropdown_font=("Arial", 14))
clCB.grid(row=3, column=0, padx=(30, 10), pady=0)
CTkButton(window, text="Start rubrication", command=checkFile, width=200, height=40, border_width=0, corner_radius=8, font=("Arial", 14)).grid(row=3, column=1, padx=(10, 30), pady=0)

Label(window, text='Select the visualization type:', background='white', font=("Arial", 11)).grid(row=4, column=0, pady=(20, 10), padx=(30, 0))
visCB = CTkComboBox(window, width=200, height=40, border_width=1, corner_radius=8, font=("Arial", 14), fg_color='white', text_color='black', values=['Article lists', 'Point diagram'], button_color=myColor, button_hover_color=hoverColor, dropdown_fg_color='white', dropdown_hover_color=myColor, dropdown_font=("Arial", 14))
visCB.grid(row=5, column=0, padx=(30, 10), pady=0)
CTkButton(window, text="Start visualization", command=checkCluster, width=200, height=40, border_width=0, corner_radius=8, font=("Arial", 14)).grid(row=5, column=1, padx=(10, 30), pady=0)
window.mainloop()
