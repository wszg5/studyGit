from tkinter import *
def cut(event=None):
    texteditor.event_generate("<<Cut>>")
def copy(event=None):
    texteditor.event_generate("<<Copy>>")
def paste(event=None):
    texteditor.event_generate('<<Paste>>')
root=Tk()
texteditor=Text(root)
texteditor.pack(fill=BOTH)
menubar=Menu(root)
filemenu=Menu(menubar)
root.config(menu=menubar)
filemenu.add_command(label="Cut",command=cut)
filemenu.add_command(label="Copy",command=copy)
filemenu.add_command(label="Paste",command=paste)
menubar.add_cascade(label="File",menu=filemenu)
root.mainloop()