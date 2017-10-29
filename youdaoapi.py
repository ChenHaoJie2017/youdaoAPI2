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
import itertools

'''
+-----------+----+----------------+---------------------------+
|   �ֶ���  |����|       ����     |         ��ע              |
+-----------+----+----------------+---------------------------+
|errorCode  |text|���󷵻���      |һ������                   |
+-----------+----+----------------+---------------------------+
|query      |text|Դ����          |��ѯ��ȷʱ��һ������       |
+-----------+----+----------------+---------------------------+
|translation|text|��������        |��ѯ��ȷʱ,һ������        |
+-----------+----+----------------+---------------------------+
|basic      |text|����            |�����ʵ�,����ʱ����        |
+-----------+----+----------------+---------------------------+
|web        |text|����            |�������壬�ý�����һ������ |
+-----------+----+----------------+---------------------------+
|l          |text|Դ���Ժ�Ŀ������|һ������                   |
+-----------+----+----------------+---------------------------+
|dict       |text|�ʵ�deeplink    |��ѯ����Ϊ֧������ʱ������ |
+-----------+----+----------------+---------------------------+
|webdict    |text|webdeeplink     |��ѯ����Ϊ֧������ʱ������ |
+-----------+----+----------------+---------------------------+
'''
lanuage_code={
    '����':'zh-CHS',
    '����':'ja',
    'Ӣ��':'EN',
    '����':'ko',
    '����':'fr',
    '����':'ru',
    '��������':'pt',
    '��������':'es'        
}


errorCode={
    '101':'ȱ�ٱ����Ĳ�������������������������et��ֵ��ʵ�ʼ��ܷ�ʽ����Ӧ',
    '102':'��֧�ֵ���������',
    '103':'�����ı�����',
    '104':'��֧�ֵ�API����',
    '105':'��֧�ֵ�ǩ������',
    '106':'��֧�ֵ���Ӧ����',
    '107':'��֧�ֵĴ�����������',
    '108':'appKey��Ч��ע���˺ţ� ��¼��̨����Ӧ�ú�ʵ�������ɰ󶨣� �ɻ���Ӧ��ID����Կ����Ϣ������Ӧ��ID����appKey�� ע�ⲻ��Ӧ����Կ��',
    '109':'batchLog��ʽ����ȷ',
    '110':'�����ط�������Чʵ��',
    '111':'�������˺���Ч���������˺�ΪǷ��״̬',
    '201':'����ʧ�ܣ�����ΪDES,BASE64,URLDecode�Ĵ���',
    '202':'ǩ������ʧ��',
    '203':'����IP��ַ���ڿɷ���IP�б�',
    '301':'�ǵ���ѯʧ��',
    '302':'������ѯʧ��',
    '303':'�����˵������쳣',
    '401':'�˻��Ѿ�Ƿ��ͣ'        
    }


class Translator(tkinter.Frame):
    def __init__(self,master=None): 
        super().__init__(master)
        self.pack()
        self.label1 = Label(self, text = '�������ı�:')
        self.words = StringVar()
        self.entry1 = Entry(self, textvariable = self.words)
        self.button = Button(self, text = '����',command = self.processButton)
        self.button1 = Button(self, text = '���ӵ����ʱ�',command = self.addNewWords)
        self.button2 = Button(self, text = '�������ʱ�',command = self.viewNewWords)
        self.label2 = Label(self, text = '����:')
        self.text = ScrolledText(self,background='#ffffff')
        wordList=[]
        database=open(r'C:\Users\jyjh\Desktop\words.txt','r')
        for i in database.readlines():
            temp=i.split('\t')
            wordList.append(temp[0]+':'+temp[1])
        database.close()
        wordLists=StringVar(value=wordList)
        self.listbox=Listbox(self,listvariable=wordLists,selectmode='browse')
        self.choosed=StringVar()
        self.chooses=ttk.Combobox(self, width=12, textvariable=self.choosed)
        chooseList=['-'.join(i) for i in itertools.combinations(lanuage_code.keys(),2)]
        chooseList.extend(['Auto'])
        self.chooses['values']=chooseList
        self.chooses.current(len(chooseList)-1)
        
        
        
        self.label1.grid(row = 1, column = 1)
        self.entry1.grid(row = 1, column = 2)
        self.button.grid(row = 1, column = 3)
        self.chooses.grid(row = 1, column = 4)
        self.label2.grid(row = 2, column = 1)
        self.text.grid(row = 2, column = 2)
        self.listbox.grid(row = 2, column = 4)
        self.button1.grid(row = 3, column = 3)
        self.button2.grid(row=3,column=4)

        
    def processButton(self):
        if self.words.get()!='':
            self.translate()
               
    def translate(self):
        From=''
        To=''
        if self.choosed.get()=='Auto':
            From='auto'
            To='auto'
        else:
            choosing=self.choosed.get().split('-')
            From=self.lanuage_code[choosing[0]]
            To=self.lanuage_code[choosing[1]]
        self.text.delete('1.0',END)
        string=<APIkey>+self.words.get()+'2'+<keys>
        string=string.encode('utf-8')
        m = hashlib.md5()
        m.update(string)
        sign = m.hexdigest()
        words=self.words.get()
        url='http://openapi.youdao.com/api?q='+words+'&from='+From+'&to='+To+'&appKey=<APPID>&salt=2&sign='+sign
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
                self.text.insert(END,result)
            else:
                result='No result of '+words
                self.text.insert(END,result)
        else:
            newWordFile=open(r'newWords.txt','r')
            result='Broken network\n'
            for i in newWordFile.readlines():
                if 'Query words:'+words in i:
                    result+=i
            self.text.insert(END,result)
            
    def addNewWords(self):
        newWordFile=open(r'newWords.txt','a')
        if len(self.text.get('1.0',END))!=1:
            infomation=self.text.get('1.0',END).strip().split('\n')
            timeStamp=time.strftime("%Y-%m-%d %X", time.localtime(time.time()))
            weight=str(int(10000*time.time()))
            newWordFile.write(infomation[0]+'\t'+infomation[1]+'\t'+timeStamp+'\t'+weight+'\n')
            showinfo('Ok', 'Word has been saved!')
            newWordFile.close()
            newWordFile=open(r'newWords.txt','r')
            data=[]
            for i in newWordFile.readlines():
                data.append(i.strip().split('\t'))
            sortData=sorted(data,key=lambda d:int(d[3]),reverse=True)
            wordList=[]
            for i in sortData:
                wordList.append(re.search(r'(?<=:).*',i[0]).group()+' '+re.search(r'(?<=:).*',i[1]).group())
            wordLists=StringVar(value=wordList)
            print(wordList)
            self.listbox=Listbox(self,listvariable=wordLists,selectmode='browse')
            self.listbox.grid(row = 2, column = 4)
            newWordFile.close()
                
        else:
            showinfo('Ok', 'No word has been saved!')
            newWordFile.close()
    
    def viewNewWords(self):
        newWordFile=open(r'newWords.txt','r')
        self.text.delete('1.0',END)
        self.text.insert(END,newWordFile.read())
        newWordFile.close()
        


t=Translator()
t.master.title('Translator')
t.mainloop()
