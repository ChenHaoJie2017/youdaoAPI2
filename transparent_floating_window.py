import sys
import tkinter
import win32clipboard as w
import win32con
import requests
from tkinter import *
import requests
import hashlib
import tkinter
import json
import urllib
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
import time
import re

root = tkinter.Tk()
root.overrideredirect(True)
root.attributes("-alpha", 0.8)
root.wm_attributes('-topmost',1)
root.geometry("300x200+10+10")
canvas = tkinter.Canvas(root)
canvas.configure(width = 300)
canvas.configure(height = 200)
canvas.configure(bg = "blue")
canvas.configure(highlightthickness = 0)
canvas.pack()
x, y = 0, 0
def move(event):
    global x,y
    new_x = (event.x-x)+root.winfo_x()
    new_y = (event.y-y)+root.winfo_y()
    s = "300x200+" + str(new_x)+"+" + str(new_y)
    root.geometry(s)

def button_1(event):
    global x,y
    x,y = event.x,event.y

def button_2(event):
    root.destroy()
    sys.exit()
def writeText(text):
    canvas.delete('all')
    canvas.create_text('100','100',text=text,font = "time 10 bold underline", tags = "string")
def button_3(text):
    w.OpenClipboard()
    t = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    if type(t)==str:
        text=t.decode('utf-8')
        word=translate(text)
        writeText(word)
    else:
        text=t.decode('utf-8')
        word=translate(text)
        writeText(word)        

def translate(words):
    From='auto'
    To='auto'
    string=<Appkey>+words+'2'+<key>
    string=string.encode('utf-8')
    m = hashlib.md5()
    m.update(string)
    sign = m.hexdigest()
    url='http://openapi.youdao.com/api?q='+words+'&from='+From+'&to='+To+'&appKey=<appkey>&salt=2&sign='+sign
    response=requests.get(url)
    if response.status_code==200:
        webdic=json.loads(response.text)
        if webdic['errorCode']=='0':
            query=webdic['query'] if 'query' in webdic.keys() else words
            translation=webdic['translation']
            basic=webdic['basic'] if 'basic' in webdic.keys() else ''
            web=webdic['web'] if 'web' in webdic.keys() else ''
            result='Query words:'+query+'\n'
            result+='Result:'+''.join(translation)+'\n'
            return result
        else:
            result='No result of '+words
            return result
    else:
        newWordFile=open(r'newWords.txt','r')
        result='Broken network\n'
        for i in newWordFile.readlines():
            if 'Query words:'+words in i:
                result+=i
        return result
    
    
    
canvas.bind("<B1-Motion>",move)
canvas.bind("<Button-1>",button_1)
canvas.bind('<Double-Button-1>',button_2)
canvas.bind('<Button-3>',button_3)
root.mainloop()
