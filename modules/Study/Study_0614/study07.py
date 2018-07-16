# coding:utf-8
import tkMessageBox

from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.byeLabel = Label( self, text="Bye,Bye" )
        self.byeLabel.pack( )
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        self.inputText = Entry()
        self.inputText.pack()
        self.alertButton = Button( self, text='say', command=self.hello )
        self.alertButton.pack( )

    def hello(self):
        name = self.inputText.get() or "world"
        tkMessageBox.showinfo( 'Message', 'Hello, %s' % name )

app = Application()
# 设置窗口标题:
app.master.title('Hello')
# 主消息循环:
app.mainloop()
