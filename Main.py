from Tkinter import *
from popup import popupWindow
import ttk
import tkMessageBox
from tempfile import mkstemp
import data
import tkFileDialog as tfgiag
import json
import random
from string import maketrans
import tkFont

#destorying the gui elegantly 
def ask_quit(root):
    if tkMessageBox.askokcancel("Quit", "You want to quit now? *sniff*"):
        root.destroy()

def loaddata(df, dfnumber, button, listbox, root):
    mynewdata = tfgiag.askopenfilename(title='Choose a file',filetypes=[('Excel files', '.xlsx'), ('CSV files', '.csv')]).strip().lower()
    if mynewdata:
        fileExtension = data.getfiletype(mynewdata)
        if fileExtension == '.xlsx':
            worksheets = data.getworksheets(mynewdata)
            
            w=popupWindow(root, worksheets)
            root.wait_window(w.top)
            try:
                worksheets = w.value
            except:
                print "No value from worksheet selector"
                return
            df.loaddata(dfnumber, mynewdata, worksheets)
        else:
            df.loaddata(dfnumber, mynewdata)
        button.config(text=mynewdata.split("/")[-1:])
        listbox.delete(0, listbox.size())
        for item in df.getcolumns(dfnumber):
            listbox.insert(END, item)     
    else:
        print "Cancelled"
    
#this probably needs error checking in the future    
def loadlinks(lboxlink):
    filename = tfgiag.askopenfilename(title='Choose link file',filetypes=[('link file', '.txt')])
    if (len(filename) == 0):
        return
    with open(filename) as data_file:    
        data = json.load(data_file)    
    lboxlink.delete(0, END)
    for link in data:
        lboxlink.insert(END, link)  
    #print data
    
def savelinks(lboxlink):
    filename = tfgiag.asksaveasfilename(title='Save links as',defaultextension="*.txt", filetypes=[('txt', '*.txt')]).encode('ascii','ignore').strip()
    if (len(filename) == 0):
        print "Error, missing filename"
        return
    data = lboxlink.get(0, END)
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    

def linkdata(list1, list2, mylist):
    val1 = map(int, list1.curselection())
    val2 = map(int, list2.curselection())
    if len(val1) and len(val2):
        item = " > ".join([list1.get(val1[0]),list2.get(val2[0])]) 
        mylist.insert(END, item)  
    
    
    
def removedata(mylist):
    for idx in reversed(list(mylist.curselection())):     
        idx = int(idx)
        mylist.delete(idx)   
    #idx = map(int, list.curselection())
    #if len(idx):
    #    list.delete(idx[0])


def running(df, myID1, myID2, commonIDtext, lboxlink):
    ids = [myID1.get(1.0, END).encode('ascii','ignore').strip(), myID2.get(1.0, END).encode('ascii','ignore').strip()]
    commonID = commonIDtext.get(1.0, END).encode('ascii','ignore').strip()
    cols = lboxlink.get(0, END)
    if ((len(ids[0]) == 0) or (len(ids[1]) == 0)):
        print "Error, must have ID's filled out"
        return
    if (len(cols) == 0):
        print "Error, must have linked columns to compare"
        return
    if ((ids[0] != ids[1]) and (len(commonID) == 0)):
        print "Error, if ID's do not match you must enter a common ID name"
        return
    
    filename = tfgiag.asksaveasfilename(title='Save changelog as',defaultextension="*.CSV", filetypes=[('CSV', '*.csv')]).encode('ascii','ignore').strip()
    if (len(filename) == 0):
        print "Error, missing filename"
        return
     
    if (len(commonID) == 0):
        commonID = ids[0]
    df.betterrun(filename, ids, cols, commonID)

def getID(mytextbox, mylistbox):
    val1 = map(int, mylistbox.curselection())
    text = mylistbox.get(val1[0])
    mytextbox.delete(1.0, END)
    mytextbox.insert(END, text)

       
def main():   
    print "Starting!!"
    root = Tk()
    maindata = data.data() 
    #removing the Tkinter logo by creating a temp blank icon file
    ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
            b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
            b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            '\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

    _, ICON_PATH = mkstemp()
    with open(ICON_PATH, 'wb') as icon_file:
        icon_file.write(ICON)    
          
    root.iconbitmap(default=ICON_PATH)
    
    root.title("DataFrame Compare")
    root.protocol("WM_DELETE_WINDOW",lambda: ask_quit(root))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(0,0)
    content = Frame(root, padx=5, pady=5)
    content.grid(column=0, row=0, sticky=(N,S,E,W))
    
    #col1 = Frame(root)
    #col2 = Frame(root)
    #col3 = Frame(root)
    #col4 = Frame(root)
    #row2 = Frame(root)
    #col1.grid(column=0, row=0, sticky=(N,S))
    #col2.grid(column=1, row=0, sticky=(N,S))
    #col3.grid(column=2, row=0, sticky=(N,S))
    #col4.grid(column=3, row=0, sticky=(N,S))
    #row2.grid(column=0, row=1, columnspan=4)
    
    
    id1lbl = ttk.Button(content, text="ID 1", command= lambda: getID(myID1, lboxdf1)) 
    #ttk.Label(content, text="ID 1", width=10)
    myID1 = Text(content, width=20, height=1)
    id1lbl.grid(column=0, row=0, sticky=(W,N))
    myID1.grid(column=1, row=0, sticky=(E,N))

    id2lbl =  ttk.Button(content, text="ID 2", command= lambda: getID(myID2, lboxdf2))  
    #ttk.Label(content, text="ID 2", width=10)
    myID2 = Text(content, width=20, height=1)
    id2lbl.grid(column=0, row=1, sticky=(W,N))
    myID2.grid(column=1, row=1, sticky=(E,N))

    commonIDlbl = Label(content, text="Common ID name",)
    #ttk.Label(content, text="ID 2", width=10)
    commonIDtext = Text(content, width=20, height=1)
    commonIDlbl.grid(column=0, row=2, sticky=(W,N))
    commonIDtext.grid(column=1, row=2, sticky=(E,N))
           
    data1btn = ttk.Button(content, text="Load Data 1", command= lambda: loaddata(maindata, 0, data1btn, lboxdf1, root))
    data1btn.my_name = "df1"
    data1btn.grid(column=2, row=2)     
    
    sdf1 = Scrollbar(content, orient=VERTICAL)   
    sdf1x = Scrollbar(content, orient=HORIZONTAL)    
    lboxdf1 = Listbox(content, width=30, height=20, selectmode='BROWSE', exportselection=0, yscrollcommand = sdf1.set, xscrollcommand = sdf1x.set)  
    sdf1.config( command = lboxdf1.yview ) 
    sdf1x.config( command = lboxdf1.xview )    
    lboxdf1.grid(column=2, row=3, rowspan=5, sticky=(N,S,E,W))
    sdf1.grid(column=3, row=3, rowspan=5, sticky=(N,S))
    sdf1x.grid(column=2, row=8, sticky=(E,W))
      
    data2btn = ttk.Button(content, text="Load Data 2", command= lambda: loaddata(maindata, 1, data2btn, lboxdf2, root))
    data2btn.my_name = "df2"
    data2btn.grid(column=4, row=2)   
    
    
    sdf2 = Scrollbar(content, orient=VERTICAL)  
    sdf2x = Scrollbar(content, orient=HORIZONTAL)       
    lboxdf2 = Listbox(content, width=30, height=5, selectmode='BROWSE', exportselection=0, yscrollcommand = sdf2.set, xscrollcommand = sdf2x.set)
    sdf2.config( command = lboxdf2.yview ) 
    sdf2x.config( command = lboxdf2.xview )      
    lboxdf2.grid(column=4, row=3, rowspan=5, sticky=(N,S,E,W))
    sdf2.grid(column=5, row=3, rowspan=5, sticky=(N,S))    
    sdf2x.grid(column=4, row=8, sticky=(E,W))
    
    linkbtn = ttk.Button(content, text="Link Data", command= lambda: linkdata(lboxdf1, lboxdf2, lboxlink))
    linkbtn.grid(column=6, row=2)   
    removebtn = ttk.Button(content, text="Remove Data", command= lambda: removedata(lboxlink))
    removebtn.grid(column=7, row=2)    

    slink = Scrollbar(content, orient=VERTICAL)       
    slinkx = Scrollbar(content, orient=HORIZONTAL)  
    lboxlink = Listbox(content, width=30, height=5, selectmode='extended', exportselection=0, yscrollcommand = slink.set, xscrollcommand = slinkx.set)
    slink.config( command = lboxlink.yview )       
    slinkx.config( command = lboxlink.xview )   
    lboxlink.grid(column=6, row=3, rowspan=5, columnspan=2, sticky=(N,S,E,W))
    slink.grid(column=8, row=3, rowspan=5, sticky=(N,S))    
    slinkx.grid(column=6, row=8, columnspan=2, sticky=(E,W))
    
    de=("%02x"%random.randint(0,255))
    re=("%02x"%random.randint(0,255))
    we=("%02x"%random.randint(0,255))
    code = de+re+we
    colorbg="#"+code
    #inverse color
    table = maketrans('0123456789abcdef','fedcba9876543210')
    colorfg = "#"+code.translate(table)
    helv36 = tkFont.Font(family='Helvetica', size=16, weight='bold')
    runbtn = Button(content, background=colorbg, fg=colorfg, text="RUN!!1!", command= lambda: running(maindata, myID1, myID2, commonIDtext, lboxlink))
    runbtn['font'] = helv36
    runbtn.grid(column=0, row=9, columnspan=9, sticky=(N,S,E,W), pady=10)   

    #Adding Menu
    root.option_add('*tearOff', FALSE)
    menubar = Menu(root)
    root['menu'] = menubar
    menu_file = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menu_file.add_command(label='Save Links', command=lambda: savelinks(lboxlink))
    menu_file.add_command(label='Load Links', command=lambda: loadlinks(lboxlink))
     
    root.mainloop()
    
if __name__ == '__main__':
    main() 
