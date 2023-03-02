from bs4 import BeautifulSoup
import requests
import operator
#here I wrote a function to delete unnecessary symbols in the book
def symbols_Clean(all_words):
    no_symbol=[]
    symbols=",.é!'^+%&/()=?_<>£#$½{[]}\|@-*:;æß"+"1234567890"+chr(775)+chr(34)#symbols and numbers i want removed
    for word_ in all_words:
        for symbol in symbols:
            if symbol in word_:
                symbol_index=word_.index(symbol)
                word_=word_.replace(symbol,"")#I wanted to put a space instead of the removed symbol
                word_=word_[0:symbol_index]
        if (len(word_)>0):
            no_symbol.append(word_)#I added the new word to a file
    return no_symbol
# I wrote a function to count the most common words in the book
def dict(all_words):
    word_number={}

    for word_ in all_words:
        if word_ in word_number:
            word_number[word_]+=1#I increased the counter as I found the word
        else:
            word_number[word_]=1#If there is no word I did not increase
    return word_number
#I wrote a function to delete stopwords
def stopwords(all_words):
    clean_UP=[]
    stopwords={"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "some",
           "for", "its", "yours", "such", "into", "most", "itself", "other", "off", "who", "from", "him", "each", "the", "themselves",
           "until", "below", "are", "these", "your", "his", "through", "don", "nor", "were", "her", "more", "himself", "this", "down", "should", "our", "their",
           "while", "above", "both", "ours", "had", "she", "all", "when", "any", "before", "them", "same", "and", "been", "have", "will", 
           "does", "yourselves", "then", "that", "because", "what", "over", "why", "can", "did", "not", "now", "under", "you", "herself", "has", "just", "where",
           "too", "only", "myself", "which", "those", "after","few", "whom", "being", "theirs", "against", "doing", "how", "further", "was", "here", "than"}
    for word_ in all_words:
        for i in stopwords:
            if i in word_:
                word_=word_.replace(i,"")#I removed the stopwords
        if (len(word_)>2):#I only added the words larger than 2 letters, I counted the words less than 2 letters as meaningless
            clean_UP.append(word_)
    return clean_UP
#I wrote a function to find words in first book but not in the second book
def Diff1(all_words):
    li_dif = [i for i in all_words if i not in all_words2 ]
    return li_dif
#I wrote a function to find words in second book but not in the first book
def Diff2(all_words2):
    li_dif = [i for i in all_words2 if i not in all_words ]
    return li_dif
#I got the name of the book from the user
inputa=int(input("Please enter how many results you want:"))
b=0
c=0
d=0
e=0
f=0
#I got the name of the first book from the user
a = str(input("Book1: ")).replace(" ","_")
a =  a.replace("'", "%27")
##I got the name of the second book from the user
a2 = str(input("Book2: ")).replace(" ","_")
a2 =  a2.replace("'", "%27") 
#Kullanıcıdan aldığım kitapların isimlerini uygun formlarla değiştirdim.
r = ("https://en.wikibooks.org/wiki/" + a + "/Print_version")or("https://en.wikibooks.org/wiki/" + a + "/print_version")
r2 = ("https://en.wikibooks.org/wiki/" + a2 + "/Print_version")or("https://en.wikibooks.org/wiki/" + a2 + "/print_version")

req_resp = requests.get(r)
all_words=[]

html_kodlari = req_resp.content
sayfa_yazilari = BeautifulSoup(html_kodlari,"html.parser")

#I downloaded the first book, put the html code into a txt file and converted it to the appropriate format.
with open ("book.txt","w", encoding = "UTF-8") as dosya:
   for word_grupları in sayfa_yazilari.find_all("div",{"mw-parser-output"}):
       dosya.write(word_grupları.text)
       content=word_grupları.text
       wordS=content.lower().split()#I separated the words from each other

       for word_ in wordS:
           all_words.append(word_)
#I called the functions I wrote above respectively
all_words=symbols_Clean(all_words)
all_words=stopwords(all_words)
word_number=dict(all_words)

req_resp2 = requests.get(r2)
all_words2=[]

html_kodlari2 = req_resp2.content
sayfa_yazilari2 = BeautifulSoup(html_kodlari2,"html.parser")

#I downloaded the second book, put the html code into a txt file and converted it to the appropriate format.
with open ("book2.txt","w", encoding = "UTF-8") as dosya:
   for word_grupları2 in sayfa_yazilari2.find_all("div",{"mw-parser-output"}):
       dosya.write(word_grupları2.text)#I added the words of the book to a file
       content2=word_grupları2.text
       wordS2=content2.lower().split()

       for word_2 in wordS2:
           all_words2.append(word_2)
#I called the functions I wrote above respectively
all_words2=symbols_Clean(all_words2)
all_words2=stopwords(all_words2)
word_number2=dict(all_words2)

print("firstbook")
print("NO WORD","  FREQ_1")
for key,value in sorted(word_number.items(),key=operator.itemgetter(1),reverse=True):#I sorted the words according to their number again
    b+=1
    print(b,"-",key,value)
    if (b==inputa):#When it reached the number I received from the user, I made it exit the loop
        break

print("secondbook")
print("NO WORD  "," FREQ_2")
for key2,value in sorted(word_number2.items(),key=operator.itemgetter(1),reverse=True):
    c+=1
    print(c,"-",key2,value)
    if (c==inputa):
        break


all_wordssum=all_words+all_words2 #I combined the words of the first book and the second book

all_wordssum=symbols_Clean(all_wordssum)
all_wordssum=stopwords(all_wordssum)
word_numbersum=dict(all_wordssum)
print("sum")
print("NO WORD","FREQ_1","FREQ_2","FREQ_SUM")
for keysum,value in sorted(word_numbersum.items(),key=operator.itemgetter(1),reverse=True):
    d+=1
    print(d,"-",keysum,word_number[keysum],word_number2[keysum],value)
    if (d==inputa):
        break

#additionally I called the diff functions
distinct1=Diff1(all_words)
distinct1=symbols_Clean(distinct1)
distinct1=stopwords(distinct1)
distinct1number=dict(distinct1)
print("\nBook1:",a)
print("distinct1")
for distinct1,value in sorted(distinct1number.items(),key=operator.itemgetter(1),reverse=True):
    f+=1
    print(f,"-",distinct1,value)
    if (f==inputa):
        break



distinct2=Diff2(all_words2)
distinct2=symbols_Clean(distinct2)
distinct2=stopwords(distinct2)
distinct2number=dict(distinct2)
print("\nBook2:",a2)
print("distinct2")
for distinct2,value in sorted(distinct2number.items(),key=operator.itemgetter(1),reverse=True):
    e+=1
    print(e,"-",distinct2,value)
    if (e==inputa):
        break










        



    




