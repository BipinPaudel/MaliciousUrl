from urllib.parse import urlparse
from functools import reduce
import re
import pandas as pd
import numpy as np
import csv



class Preprocess(object):

 
    def __init__(self,mainUrl):
        self.mainUrl= mainUrl
        if not self.mainUrl.startswith('http'):               
            self.mainUrl='http://'+mainUrl
        self.lengthFeatures=[]
        self.countFeatures=[]
        self.ratioFeatures=[]
        self.binaryFeatures=[]
        self.hostName=''
        self.path=''
        self.parameter=''
        print(self.mainUrl)

    def separateIntoThree(self):
        

        parse_object=urlparse(self.mainUrl)
        self.hostName= parse_object.netloc
        self.path=parse_object.path
        self.parameter=parse_object.query
   
        
        self.addLengthFeatures()
        self.addCountFeatures()
        self.addRatioFeatures()
        self.addBinaryFeatures()
        ##print(self.hostName)
        ##print(self.path)
        ##print(self.parameter)

    def addLengthFeatures(self):
        ## We will add URL length feature
        self.addToLenFeat(len(self.mainUrl))

        ## We will add length of hostname
        self.addToLenFeat(len(self.hostName))

        ##we will add first directory length
        self.addToLenFeat(self.getFirstDirectoryLength())

        ## we will add parameter length
        self.addToLenFeat(len(self.parameter))

        ##we will add path length
        self.addToLenFeat(len(self.path))

        
        ## we will call function to calculate length of tld and sld
        self.addTldSldLength()

        ##we call function to add longest tokens in all
        self.addLongestTokens()
        
        

    def getFirstDirectoryLength(self):
        splitBySlash= self.path.split('/')
        ##print(len(splitBySlash))
        if len(splitBySlash)>1 :
            return len(splitBySlash[1])
        else:
            return 0



    def addTldSldLength(self):
        dotSplit=self.hostName.split('.')
        lenMap= list(map(lambda word: len(word),dotSplit))
        ## we add tld length
        
        self.addToLenFeat(lenMap[0])
        if len(dotSplit) > 2:
            ##we add sld
            c= reduce(lambda x,y : x+y, lenMap[1:])
            self.addToLenFeat(c)
        else:
        ## we add sld
            self.addToLenFeat(lenMap[1])

    def addToLenFeat(self,value):
        self.lengthFeatures.append(value)

    def addLongestTokens(self):
        splitHostName= re.split(r'[/?.=-_]',self.hostName)
        splitPath=re.split(r'[/?.=-_]',self.path)
        splitParameter=re.split(r'[/?.=-_]',self.parameter)
        splitUrl=re.split(r'[/?.=-_]',self.mainUrl)
        maxHostTokenLength111= max(list(map(lambda x : len(x), splitUrl)))
        maxHostTokenLength= max(list(map(lambda x : len(x), splitHostName)))
        maxPathTokenLength=max(list(map(lambda x : len(x), splitPath)))
        maxParameterTokenLength=max(list(map(lambda x : len(x), splitParameter)))
        maxUrlTokenLength=max(maxHostTokenLength,maxPathTokenLength,maxParameterTokenLength)
        self.addToLenFeat(maxHostTokenLength) ## adding length of longest host token
        self.addToLenFeat(maxPathTokenLength)##length of longest path token
        self.addToLenFeat(maxParameterTokenLength)##length of longest parameter token
        self.addToLenFeat(maxUrlTokenLength)##length of longest url token

    def getLengthFeatures(self):
        ##print(self.lengthFeatures)
        return self.lengthFeatures

    

    ## count features
        ## starts now
    
    def addCountFeatures(self):
        #1
        dashInUrl=re.findall('[-]',self.mainUrl)
        self.addToCountFeat(len(dashInUrl))##add - in url count
#2
        dashInHostName=re.findall('[-]',self.hostName)
        self.addToCountFeat(len(dashInHostName)) ##add - in hostname
#3
        undScoreInUrl = re.findall('[_]',self.mainUrl)
        self.addToCountFeat(len(undScoreInUrl))##add _ in url count
#4
        undScoreInHostName=re.findall('[_]',self.hostName)
        self.addToCountFeat(len(undScoreInHostName)) ##add _ in hostname
#5
        atInUrl = re.findall('[@]',self.mainUrl)
        self.addToCountFeat(len(atInUrl))##add @ in url count
#6
        questionInUrl = re.findall('[?]',self.mainUrl)
        self.addToCountFeat(len(questionInUrl))##add ? in url count
#7        
        dotInUrl= re.findall('[.]',self.mainUrl)
        self.addToCountFeat(len(dotInUrl)) ##add . in url count
#8
        equalsInUrl= re.findall('[=]',self.mainUrl)
        self.addToCountFeat(len(equalsInUrl)) ## add = in url count
#9
        percentInUrl = re.findall('[%]',self.mainUrl)
        self.addToCountFeat(len(percentInUrl)) ## add % in url count
#10
        digitsInUrl = re.findall('\d',self.mainUrl) ##\d denotes digits
        self.addToCountFeat(len(digitsInUrl)) ## add number of digits in url
#11
        digitsInHostName = re.findall(r'\d',self.hostName) ##\d denotes digits
        self.addToCountFeat(len(digitsInHostName)) ## add number of digits in url
#12
        lettersInUrl = re.findall('[a-zA-Z]',self.mainUrl) ##\D denotes letters
        self.addToCountFeat(len(lettersInUrl)) ## add number of letters in url

        #13
        smallLettersInUrl= re.findall("[a-z]",self.mainUrl)
        self.addToCountFeat(len(smallLettersInUrl))
        
        #14
        capitalLettersInUrl= re.findall("[A-Z]",self.mainUrl)
        self.addToCountFeat(len(capitalLettersInUrl))

        #15
        lettersInHostName = re.findall('[a-zA-Z]',self.hostName)
        self.addToCountFeat(len(lettersInHostName))
                                    
        #16
        smallLettersInHostName=re.findall("[a-z]",self.hostName)
        self.addToCountFeat(len(smallLettersInHostName))

        #17
        capitalLettersInHostName=re.findall("[A-Z]",self.hostName)
        self.addToCountFeat(len(capitalLettersInHostName))
        
        #18
        tokensInUrl= re.split(r'[/?.=-_]',self.mainUrl)
        self.addToCountFeat(len(tokensInUrl))

        #19
        tokensInHostName = re.split(r'[/?.=-_]',self.hostName)
        self.addToCountFeat(len(tokensInHostName))

        #20
        tokensInPath=re.split(r'[/?.=-_]',self.path)
        self.addToCountFeat(len(tokensInPath))
        
        #21
        tokensInParameter= re.split(r'[/?.=-_]',self.path)
        self.addToCountFeat(len(tokensInParameter))
        
        #22
        nonAlphaCharacters= sum(not c.isalnum() for c in self.mainUrl)
        self.addToCountFeat(nonAlphaCharacters)

        #23
        directoriesSplit= self.path.split('/')
        if len(directoriesSplit) > 1:
            self.addToCountFeat(len(directoriesSplit)-1)
        else:
            self.addToCountFeat(0)

        #24
        parametersSplit=self.parameter.split('&')
        self.addToCountFeat(len(parametersSplit))
        

        

    def getCountFeatures(self):
        ##print(self.countFeatures)
        return self.countFeatures
        
    def addToCountFeat(self,value):
        self.countFeatures.append(value)


        ### this is the beginning of the ratio features
    def addRatioFeatures(self):
        
        
        vowelsInUrl = len(re.findall('[aeiouAEIOU]',self.mainUrl))
        consonantsInUrl=len(re.findall('[^aeiouAEIOU]',self.mainUrl))
        consonantsInUrl= 1 if consonantsInUrl==0 else consonantsInUrl
        vowelsInUrl = 1 if vowelsInUrl==0 else vowelsInUrl
        vowelByConsonantUrl= vowelsInUrl/consonantsInUrl
        ##1
        self.addToRatioFeat(vowelByConsonantUrl)
        
        vowelsInHostName= len(re.findall('[aeiouAEIOU]',self.hostName))
        consonantsInHostName=len(re.findall('[^aeiouAEIOU]',self.hostName))
        vowelsInHostName = 1 if vowelsInHostName==0 else vowelsInHostName
        consonantsInHostName=1 if consonantsInHostName else consonantsInHostName
        vowelByConsonantHostName=vowelsInHostName/consonantsInHostName
        #2
        self.addToRatioFeat(vowelByConsonantHostName)
        
        vowelsInPath= len(re.findall('[aeiouAEIOU]',self.path))
        consonantsInPath=len(re.findall('[^aeiouAEIOU]',self.path))
        vowelsInPath = 1 if vowelsInPath==0 else vowelsInPath
        consonantsInPath = 1 if consonantsInPath==0 else consonantsInPath
        vowelByConsonantPath= vowelsInPath/consonantsInPath
        ##3
        self.addToRatioFeat(vowelByConsonantPath)

        
        vowelsInParameter = len(re.findall('[aeiouAEIOU]',self.parameter))
        consonantsInParameter=len(re.findall('[^aeiouAEIOU]',self.parameter))
        vowelsInParameter=1 if vowelsInParameter ==0 else vowelsInParameter
        consonantsInParameter=1 if consonantsInParameter==0 else consonantsInParameter
        vowelByConsonantParameter= vowelsInParameter/consonantsInParameter
        ##4
        self.addToRatioFeat(vowelByConsonantParameter)

        lettersInUrl = len(re.findall('[a-zA-Z]',self.mainUrl))
        digitsInUrl= len(re.findall('[0-9]',self.mainUrl))
        lettersInUrl=1 if lettersInUrl==0 else lettersInUrl
        digitsInUrl=1 if digitsInUrl==0 else digitsInUrl
        digitByLetterUrl=digitsInUrl/lettersInUrl
        ##5
        self.addToRatioFeat(digitByLetterUrl)
        
        
        lettersInHostName= len(re.findall('[a-zA-Z]',self.hostName))
        digitsInHostName=len(re.findall('[0-9]',self.hostName))
        lettersInHostName=1 if lettersInHostName==0 else lettersInHostName
        digitsInHostName=1 if digitsInHostName==0 else digitsInHostName
        digitByLetterHostName=digitsInHostName/lettersInHostName
        ##6
        self.addToRatioFeat(digitByLetterHostName)
        
        lettersInPath = len(re.findall('[a-zA-Z]',self.path))
        digitsInPath= len(re.findall('[0-9]',self.path))
        lettersInPath=1 if lettersInPath==0 else lettersInPath
        digitsInPath=1 if digitsInPath==0 else digitsInPath
        digitByLetterPath = digitsInPath/lettersInPath
        ##7
        self.addToRatioFeat(digitByLetterPath)
                            
        lettersInParameter=len(re.findall('[a-zA-Z]',self.path))
        digitsInParameter=len(re.findall('[0-9]',self.parameter))
        lettersInParameter=1 if lettersInParameter==0 else lettersInParameter
        digitsInParameter=1 if digitsInParameter==0 else digitsInParameter
        digitByLetterParameter = digitsInParameter/lettersInParameter
        ##8
        self.addToRatioFeat(digitByLetterParameter)

        urlTokenSplit=re.split(r'[/?.=-_]',self.mainUrl)
        urlTokenSplit=1 if urlTokenSplit==0 else urlTokenSplit
        averageTokenLengthUrl=sum(list(map(lambda word:len(word),urlTokenSplit)))/len(urlTokenSplit)
        ##9
        self.addToRatioFeat(averageTokenLengthUrl)
        
        hostNameTokenSplit=re.split(r'[/?.=-_]',self.hostName)
        hostNameTokenSplit=1 if hostNameTokenSplit==0 else hostNameTokenSplit
        averageTokenLengthHostName=sum(list(map(lambda word:len(word),hostNameTokenSplit)))/len(hostNameTokenSplit)
        ##10
        self.addToRatioFeat(averageTokenLengthHostName)

        pathTokenSplit=re.split(r'[/?.=-_]',self.path)
        pathTokenSplit=1 if pathTokenSplit==0 else pathTokenSplit
        averageTokenLengthPath=sum(list(map(lambda word:len(word),pathTokenSplit)))/len(pathTokenSplit)
        ##11
        self.addToRatioFeat(averageTokenLengthPath)
        
        parameterTokenSplit=re.split(r'[/?.=-_]',self.parameter)
        parameterTokenSplit=1 if parameterTokenSplit==0 else parameterTokenSplit
        averageTokenLengthParameter=sum(list(map(lambda word:len(word),parameterTokenSplit)))/len(parameterTokenSplit)
        #12
        self.addToRatioFeat(averageTokenLengthParameter)

    def addToRatioFeat(self,value):
        self.ratioFeatures.append(value)

    def getRatioFeatures(self):
        ##print(self.ratioFeatures)
        return self.ratioFeatures


        ###this is the beginning of binary features
    def addBinaryFeatures(self):
        mainWords=['.com','google','facebook','ebay','amazon','youtube','baidu','yahoo',
                   'twitter','instagram','microsoft']
        for mWord in mainWords:
            self.checkMainWords(mWord)


    def checkMainWords(self,value):
        if value in self.path:
            self.addToBinaryFeat(1)
        else:
            self.addToBinaryFeat(0)

    def addToBinaryFeat(self,value):
        self.binaryFeatures.append(value)

    def getBinaryFeatures(self):
        ##print(self.binaryFeatures)
        return self.binaryFeatures

url1='example_me.com/random/folder/path.html?a_b=234&b=456'
url2='example.com'
url3='https-paypal.verifications-updates.com/'
url4='pakistanifacebookforever.com/getpassword.php/'
url6='google.com/search=faizanahad'
url7='https://venturebeat.com/2016/08/16/facebook-will-waive-fees-for-account-kit-sms-confirmation-messages-through-august-2018/'
url8='belgravesoundandlight.com/'
url9='bioguide.congress.gov/scripts/bibdisplay.pl?index=P000003'
data= Preprocess(url9)

data.separateIntoThree()

lenFeature=data.getLengthFeatures()
countFeature=data.getCountFeatures()
ratioFeature=data.getRatioFeatures()
binaryFeature=data.getBinaryFeatures()
wholeSingleFeature=lenFeature+countFeature+ratioFeature+binaryFeature
print(wholeSingleFeature)
##data = pd.read_csv('final1.csv',encoding="ISO-8859-1", error_bad_lines=False)
##allUrlsData=pd.DataFrame(data)
##allUrlsData=np.array(allUrlsData)
##corpus=[d[0] for d in allUrlsData]
##y=[d[3] for d in allUrlsData]
##y=list(map(lambda a: 1 if a=='good' else 0,y))
####corpus= corpus[0:5]
##i=39214
##featureCorpus=[]
##for url in corpus[i:]:
##    print()
##    
##    print('index ',i)
##    data=Preprocess(url)
##    data.separateIntoThree()
##    lenFeature=data.getLengthFeatures()
##    countFeature=data.getCountFeatures()
##    ratioFeature=data.getRatioFeatures()
##    binaryFeature=data.getBinaryFeatures()
##    wholeSingleFeature=[y[i]]+lenFeature+countFeature+ratioFeature+binaryFeature
##    with open(r'featureCorpus.csv','a') as features:
##        wr=csv.writer(features)
##        wr.writerow(wholeSingleFeature)
##    ##featureCorpus.append(wholeSingleFeature)
##    i=i+1

##print(featureCorpus)
##for i in featureCorpus:
  ##  print(len(i))
