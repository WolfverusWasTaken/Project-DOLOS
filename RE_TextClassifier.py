from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
from tkinter import *
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from time import sleep
import nltk
from transformers import pipeline

'''
[NOTE: THIS PROJECT IS STILL IN WORK. SOME UPCOMING FEATURES INCLUDE:        ]

[- UPLOADING SUMMARIZING NLP AI INTO A SERVER TO REDUCE STRAIN ON DEVICE     ]

[- A PROPER WORKING GUI TO IMPLEMENT SMOOTH USAGE INSTEAD OF MANUALLY        ]
[  COMMENTING AND UNCOMMENTING OR ADDING LINKS.]

[- A FEATURE TO AD LINKS INTO A QUEUE. THIS WILL ALLOW CONTINOUS AND CONSTANT]
[  SUMMARIZING. ALLOWING USERS TO SIT BACK AND RELAX.]

[- MAKING A PERSONALIZED AI WITH MY OWN DATASET.(A little hard to source out data.)]

<AUTHOR: WOLFVERUS>
<DATE OF CREATION: NOV 2020>
<PROJECT STATUS: WORK-IN-PROGRESS>

<FEEL FREE TO USE MY CODE GIVING REFERENCE TO THIS LINK WOULD BE EXTREMELY APPRECIATED.>
'''

#Cleans Grabbed Text completely of HTML Tags/Elements
def RemoveHTMLElem(): #removes all HTML tags
    global WebString

    WebString = re.sub(r'<a.+?a>', '', WebString)

    WebString = re.sub(r'<b.+?b>', '', WebString)

    WebString = re.sub(r'<i.+?i>', '', WebString)

    WebString = re.sub(r'<a href.+?a>', '', WebString)

    WebString = re.sub(r'<p class.+?>', '', WebString)

    WebString = re.sub(r'<img.+?/>', '', WebString)

    WebString = re.sub(r'\([^)]*\)', '', WebString)

    WebString = WebString.replace('<p> </p>', '<p></p>')

    WebString = WebString.replace('<p></p>', '')

    WebString = WebString.replace('<p>', '<p> ')

    WebString = WebString.replace('</p>', ' </p>')

    WebString = WebString.replace('<p> ', '')

    WebString = WebString.replace(' </p>', '')

    WebString = re.sub(r'<.+?>', '', WebString)

    WebString = WebString.replace('<', '')

    WebString = WebString.replace('>', '')

    if "©" in WebString:
        WebString = ''

    if "align=\"center\"" in WebString:
        WebString = ''

    WebString = " ".join(WebString.split())

#Final Cleaning Of Grabbed Text
def TextCleaner(): #Removes unwanted symbols. commas, apostrophe, brackets etc.
    global WebString

    WebString = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', WebString)

    WebString = WebString.replace('(', '')
    WebString = WebString.replace(')', '')

    """if "e.g.:" in WebString:
        WebString = ''

    if "Example:" in WebString:
        WebString = ''"""

    WebString = re.sub(r'[^\w]', ' ', WebString)
    WebString = WebString.replace(' s ', ' ')

    WebString = " ".join(WebString.split())

#Filters out cleaned text with lemmatization, stemming etc.
def Filterer(): #filters cleaned raw website data. Lemmatization etc.
    global FilteredList
    global FinalWebString
    words = set(nltk.corpus.words.words())

    print("====================Filtering====================")

    FinalWebString = " ".join(w for w in nltk.wordpunct_tokenize(FinalWebString) \
                    if w.lower() in words or not w.isalpha())


    lemmatizer=WordNetLemmatizer()

    tokens = word_tokenize(FinalWebString)
    stop_words = set(stopwords.words('english'))

    FilteredList = [i for i in tokens if not i in stop_words]
    FilteredList = [lemmatizer.lemmatize(word) for word in FilteredList]


    for i in range(9):
        FilteredList = ' '.join(FilteredList).replace(str(i), '').split()

    for word in FilteredList:
        if len(word) < 3:
            FilteredList.remove(word)

    print(FilteredList)


    sleep(1)

#Cleans lemmatized/stemmed text a final time before finding synonyms/summarizing
def FilteredCleaner(): #cleans filtered website data.
    global FilteredList
    TFilt = 0


    print("==================Filt.Cleaning==================")
    sleep(1)
    for i in range(5):
        print("-----------------[Iteration: " + str(i + 1) + "]------------------")
        sleep(0.5)

        for word in FilteredList:

            if len(word) < 3:
                FilteredList.remove(word)
                TFilt += 1

            if len(word) < 3:
                print(word +" [length:"+ str(len(word)) + "]")

        print("[Total Removed: " + str(TFilt) + "]")

    print("==================Finalized Set==================")
    print(FilteredList)

#Prints out all formats of scarped website data [With HTML tags, lemmatized/stemmed data etc.]
def PrintAllTypes(): #To check various formats of scraped website. Prints out HTML, cleaned and phrased versions of text.
    global PhrasedWebString
    global WebString
    global element


    print(str(element))
    print("\n"
          + "Clean HTML:\n" + WebString
          + "\n\nPhrased HTML: " + PhrasedWebString)

    print("\n[Words: " + str(len(WebString.split())) + "]"
          + "\n"
          + "==========================================================================")

#Finds synonym of each word in the data.
#[NOTE: AT THE CURRENT MOMENT THIS PROCESS/FEATURE IS NOT IN USE. WILL WORK ON IT IN THE FUTURE.]
def SynFind(): #find synonyms of words. [CURRENTLY NOT IN USE]
    global FilteredList
    global FilteredString

    print("=================Finding Synonym=================")

    FilteredString = ''

    print("------------------Array to Text------------------")
    FilteredString = ' '.join([str(elem) for elem in FilteredList])

    print(FilteredString)

    #doc = nlp(FilteredString)
    #print([(X.text, X.label_) for X in doc.ents])

#Summarizing of cleaned and filtered website data.
def summarize(): #summarises cleaned web data here and prints it out.
    global FinalWebString
    global Arr

    Arr = nltk.sent_tokenize(FinalWebString)
    for sentence in Arr:
        to_tokenize = sentence

        summarizer = pipeline("summarization")
        summarized = summarizer(to_tokenize, min_length=75, max_length=300)

        print(summarized)

#Overall process runs within this function.
def process(): #Runs all defined processes in this function.
    global FilteredList
    global WebString
    global FinalWebString
    global cmd
    global element

    line = 0
    FinalWebString = ''

    link = "https://www.tesla.com/about" #state link here.
    print(link)

    #================================================SETTING UP================================================#
    response = requests.get(link)
    #==========================================================================================================#
    soup = BeautifulSoup(response.text, 'html.parser')
    #==========================================================================================================#
    x = soup.find_all('p')
    #==========================================================================================================#
    for element in x:
        line += 1
        WebString = str(element)
        RemoveHTMLElem()        #Cleans Grabbed Text completely of HTML Tags/Elements
        #TextCleaner()           #Final Cleaning Of Grabbed Text
        FinalWebString += " " + WebString

    #==========================================================================================================#
    #[UNCOMMENT AND USE RESPECTIVE PROCESS ACCORDINGLY. THIS PROJECT IS STILL WORK IN PROGRESS.]
    #Filterer()
    #FilteredCleaner()
    #SynFind()
    #summarize()
    #==========================================================================================================#



process()