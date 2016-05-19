from Tkinter import *

class popupWindow(object):
    def __init__(self,master, items):
        self.top=Toplevel(padx=5, pady=5)
        self.top.resizable(0,0)
        self.top.grab_set()
        
        self.l=Label(self.top,text="Please pick your worksheet") 
        yscroll = Scrollbar(self.top)       
        xscroll = Scrollbar(self.top, orient=HORIZONTAL)  
        self.e = Listbox(self.top, yscrollcommand = yscroll.set, xscrollcommand = xscroll.set)
        yscroll.config( command = self.e.yview )       
        xscroll.config( command = self.e.xview )   

        for item in items:
            self.e.insert(END, item)
        self.e.pack()
        self.b=Button(self.top,text='Ok',command=self.cleanup)
        
        self.l.grid(column=0, row=0, columnspan=2, sticky=(N,S,E,W))
        self.e.grid(column=0, row=1, rowspan=5, sticky=(N,S,E,W))
        yscroll.grid(column=1, row=1, rowspan=5, sticky=(N,S))
        xscroll.grid(column=0, row=6, columnspan=2, sticky=(E,W))    
        self.b.grid(column=0, row=7, columnspan=2, sticky=(E,W))

    
    def cleanup(self):
        item = map(int, self.e.curselection())
        if len(item):
            self.value=self.e.get(item[0])
        else:
            return
        self.top.grab_release()
        self.top.destroy()
