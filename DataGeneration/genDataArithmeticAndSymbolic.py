from dataTemplate import Q, INPUT, numbers ,chars,lange,typeMapTemplate,charTypeMapTemplate,MAXNUM,STRLENMIN,STRLENMAX,SYMBOLICTURN
import json
import random
import math
resultPath="./data/"
TrainNum=500  # Number of training sets
TestNum=50 # Number of Testers
dataNum=TrainNum+TestNum
typeSet=['add','sub','mul','div','eq',"isotropic","isometric","sort"] # Types of math operations
symbolicTypeSet=['repeat','add','sub','replace'] # Types of symbolic operations
choiceMap={0:"A",1:"B",2:"C",3:"D"}

def testRule(nowtype,usedSet=None,Large=False): # Sample of generating a math data set
    a=random.randint(0,MAXNUM)
    b=random.randint(0,MAXNUM)
    if nowtype=='div' or nowtype=="mul":
        a=random.randint(0,int(math.sqrt(MAXNUM)*1.5))
        b=random.randint(0,int(math.sqrt(MAXNUM)*1.5))
    if Large and a<=b:
        a,b=b,a
    if (usedSet is not None and (a,b) in usedSet):
        return testRule(nowtype,usedSet)
    if nowtype=='add':
        if a+b>MAXNUM:
            return testRule(nowtype,usedSet)
        return str(a)+","+str(b),str(a+b),a,b
    elif nowtype=='sub':
        if a-b<0:
            return testRule(nowtype,usedSet)
        return str(a)+","+str(b),str(a-b),a,b
    elif nowtype=='mul':
        if a*b>MAXNUM:
            return testRule(nowtype,usedSet)
        return str(a)+","+str(b),str(a*b),a,b
    elif nowtype=='div':
        if a==0 or a*b>MAXNUM:
            return testRule(nowtype,usedSet)
        return str(a*b)+","+str(a),str(b),a,b
    elif nowtype=='eq':
        return str(a)+","+str(b),str(a)+","+str(b),a,b
    elif nowtype=='isotropic':
        d=random.randint(0,MAXNUM//2)
        if (usedSet is not None and (a,d) in usedSet) or a+2*d>MAXNUM:
            return testRule(nowtype,usedSet)      
        return str(a)+","+str(a+d),str(a+2*d),a,d
    elif nowtype=='isometric':
        q=random.randint(1,int(math.sqrt(MAXNUM)))
        if (usedSet is not None and (a,q) in usedSet) or a*q*q>MAXNUM:
            return testRule(nowtype,usedSet)
        return str(a)+","+str(a*q),str(a*q*q),a,q
    elif nowtype=='sort':
        if a>b:
            return str(a)+","+str(b),str(b)+","+str(a),a,b
        else:
            return str(a)+","+str(b),str(a)+","+str(b),a,b

def changeDataToLang(data,lang): # Convert data to language
    if isinstance(data,list):
        result=[]
        for i in data:
            result.append(changeDataToLang(i,lang))
        return result
    if data in typeSet:
        return typeMapTemplate[data+lang]
    elif "," in data:
        data=data.split(",")
        return numbers[lang][int(data[0])]+","+numbers[lang][int(data[1])]
    else:
        return numbers[lang][int(data)]


def changeTagToFullTag(tag,strLen): # Convert the tag to a full tag
    if tag=='add':
        tag=tag+','+str(random.randint(0,strLen-1))+','+str(random.randint(0,len(chars['EN'])-1))
    elif tag=='sub':
        tag=tag+','+str(random.randint(0,strLen-1))
    elif tag=='replace':
        while True:
            loc1=random.randint(0,strLen-1)
            loc2=random.randint(0,strLen-1)
            if loc1!=loc2:
                break
        tag=tag+','+str(loc1)+','+str(loc2)
    return tag

def repeatTestRuleSymbolic(tag,usedSet=None,input=None,strlen=3,n=3): # Sample of generating a symbolic data set
    inputSet=[]
    outputSet=[]
    for i in range(n):
        if input is not None:
            tinput,output,rule=testRuleSymbolic(tag,input=input[i])
        else:
            tinput,output,rule=testRuleSymbolic(tag,strlen=strlen,usedSet=usedSet)
        inputSet.append(tinput)
        outputSet.append(output)
    return inputSet,outputSet,rule

def changeDataToLangForSymbolic(data,lang): # Convert data to language for symbolic
    if isinstance(data[0],list):
        result=[]
        for i,item in enumerate(data):
            result.append(changeDataToLangForSymbolic(item,lang))
        return result
    result=[]
    for i in data:
        result.append(chars[lang][i])
    return ",".join(result)


def changeSigleRuleToLang(rule,lang): # Convert a single rule to a language
    if "," in rule:
        rule=rule.split(",")
        if 'add' in rule:
            loc=int(rule[1])
            repeatNum=int(rule[2])
            nowtype=rule[0]
            return charTypeMapTemplate[nowtype+lang].format(char=chars[lang][repeatNum],loc=loc)
        elif 'sub' in rule:
            loc=int(rule[1])
            nowtype=rule[0]
            return charTypeMapTemplate[nowtype+lang].format(loc=loc)
        elif 'replace' in rule:
            loc1=int(rule[1])
            loc2=int(rule[2])
            nowtype=rule[0]
            return charTypeMapTemplate[nowtype+lang].format(loc1=loc1,loc2=loc2)
    else:
        return charTypeMapTemplate[rule+lang]
        



def changeRuleToLang(rule,lang): # Convert the rule to a language
    if isinstance(rule,list):
        result=[]
        for i,item in enumerate(rule):
            result.append(changeRuleToLang(item,lang))
        return result
    if ";" in rule:
        rule=rule.split(";")
        for i in range(len(rule)):
            rule[i]=changeSigleRuleToLang(rule[i],lang)
        return ";".join(rule)
    else:
        return changeSigleRuleToLang(rule,lang)


def chartypeToTemplate(nowtype,lang):
    if nowtype=='repeat':
        return charTypeMapTemplate[nowtype+lang]
    elif 'add' in nowtype:
        loc=int(nowtype.split(',')[1])
        addNum=int(nowtype.split(',')[2])
        nowtype=nowtype.split(',')[0]
        return charTypeMapTemplate[nowtype+lang].format(char=chars[lang][addNum],loc=loc+1)
    elif 'sub' in nowtype:
        loc=int(nowtype.split(',')[1])
        nowtype=nowtype.split(',')[0]
        return charTypeMapTemplate[nowtype+lang].format(loc=loc+1)
    elif 'replace' in nowtype:
        loc1=int(nowtype.split(',')[1])
        loc2=int(nowtype.split(',')[2])
        nowtype=nowtype.split(',')[0]
        return charTypeMapTemplate[nowtype+lang].format(loc1=loc1+1,loc2=loc2+1)

def testRuleSymbolic(nowtype,strlen=None,input=None,usedSet=None): # Sample of generating a symbolic data set
    if input is not None:
        numLoc=input
    else:
        numLoc=random.sample(range(0,100),strlen)
    if (usedSet is not None and str(numLoc) in usedSet):
        return testRuleSymbolic(nowtype,strlen=strlen,input=input,usedSet=usedSet)
    elif usedSet is not None:
        usedSet.add(str(numLoc))
    if nowtype=='repeat':
        return numLoc,numLoc,nowtype
    elif 'add' in nowtype:
        loc=int(nowtype.split(',')[1])
        repeatNum=int(nowtype.split(',')[2])
        nowtype=nowtype.split(',')[0]
        newNumLoc=numLoc.copy()
        newNumLoc.insert(loc,repeatNum)
        return numLoc,newNumLoc,str(nowtype+","+str(loc+1)+","+str(repeatNum))
    elif 'sub' in nowtype:
        loc=int(nowtype.split(',')[1])
        nowtype=nowtype.split(',')[0]
        newNumLoc=numLoc.copy()
        newNumLoc.remove(newNumLoc[loc])
        return numLoc,newNumLoc,str(nowtype+","+str(loc+1))
    elif 'replace' in nowtype:
        loc1=int(nowtype.split(',')[1])
        loc2=int(nowtype.split(',')[2])
        nowtype=nowtype.split(',')[0]
        newNumLoc=numLoc.copy()
        temp=newNumLoc[loc1]
        newNumLoc[loc1]=newNumLoc[loc2]
        newNumLoc[loc2]=temp
        return numLoc,newNumLoc,str(nowtype+","+str(loc1+1)+","+str(loc2+1))

def getOtherChoice(nowtype,para=None,para2=None): # Get other choices for math
    result=[]
    while True:
        input1,output1,_,_=testRule(nowtype)
        if output1==para:
            continue
        result.append(output1)
        if len(result)==3:
            result.append(para)
            random.shuffle(result)
            return result,choiceMap[result.index(para)]            

def getSymbolicOutPut(output,turn,rule,isList=False): # Get the output of symbolic
    output1=output
    if isList:
        output1=output[0]
    for turnLoc in range(turn):
        tag=random.choice(symbolicTypeSet)
        while (len(output1)==1 and tag=='sub') or (len(output1)==1 and tag=='replace'):
            tag=random.choice(symbolicTypeSet)
        tag=changeTagToFullTag(tag,len(output1))
        if isList:
            _,output,rulet=repeatTestRuleSymbolic(tag,input=output)
            output1=output[0]
        else:
            _,output,rulet=testRuleSymbolic(tag,input=output)
            output1=output
        rule+=';'+rulet
    return output,rule

def getOtherChoiceSymbolic(input): # Get other choices for symbolic
    result=[input]
    while True:
        a=random.randint(0,99)
        loc=random.randint(0,len(input)-1)
        flag=False
        for i in range(len(result)):
            if result[i][loc]==a:
                flag=True
                break
        if flag:
            continue
        inputCopy=input.copy()
        inputCopy[loc]=a
        result.append(inputCopy)
        if len(result)==4:
            random.shuffle(result)
            choice=choiceMap[result.index(input)]
            return result,choice


def SplitTrainAndTest(data,TrainNum=500,TestNum=50):
    dataNum=TrainNum+TestNum
    train=[]
    test=[]
    for i in range(len(data)//dataNum):
        train.extend(data[i*dataNum:i*dataNum+TrainNum])
        test.extend(data[i*dataNum+TrainNum:i*dataNum+dataNum])
    return train,test


def Arithmetic():
    result={}
    for lang in lange:
        result[lang]=[]
    for i in typeSet:
        usedSet=set()
        for j in range(dataNum):
            input,output,a,b=testRule(i,usedSet)
            usedSet.add((a,b))
            outputSet,choice=getOtherChoice(i,output)
            for lang in lange:
                inputlang=changeDataToLang(input,lang)
                outputSetlang=changeDataToLang(outputSet,lang)
                result[lang].append({"prompt":Q["Arithmetic"+lang],"query":INPUT["Arithmetic"+lang].format(typeMapTemplate[i+lang],inputlang,outputSetlang[0],outputSetlang[1],outputSetlang[2],outputSetlang[3]),"response":choice})
    for lang in lange:
        resultlang=result[lang]
        trainData,testData=SplitTrainAndTest(resultlang)
        with open(resultPath+"Arithmetic"+lang+"train.json","w") as f:
            json.dump(trainData,f,indent=4,ensure_ascii=False)
        with open(resultPath+"Arithmetic"+lang+"test.json","w") as f:
            json.dump(testData,f,indent=4,ensure_ascii=False)

def Symbolic():
    result={}
    for lang in lange:
        result[lang]=[]
    for turn in range(SYMBOLICTURN):
        usedSet=set()
        for i in symbolicTypeSet:
            if turn == 0:
                usedSet=set()
            for j in range(dataNum):
                if turn>0:
                    i=random.choice(symbolicTypeSet)
                else:
                    i=i.split(',')[0]
                strlen=random.randint(STRLENMIN,STRLENMAX)
                i=changeTagToFullTag(i,strlen)
                input,output,rule=testRuleSymbolic(i,strlen=strlen,usedSet=usedSet)
                output,rule=getSymbolicOutPut(output,turn,rule)
                output,choice=getOtherChoiceSymbolic(input=output)
                for lang in lange:
                    outputlang=changeDataToLangForSymbolic(output,lang)
                    rulelang=changeRuleToLang(rule,lang)
                    inputlang=changeDataToLangForSymbolic(input,lang)
                    result[lang].append({"prompt":Q["Arithmetic"+lang],"query":INPUT["Arithmetic"+lang].format(rulelang,inputlang,outputlang[0],outputlang[1],outputlang[2],outputlang[3]),"response":choice})
    for lang in lange:
        resultlang=result[lang]
        trainData,testData=SplitTrainAndTest(resultlang)
        with open(resultPath+"Symbolic"+lang+"train.json","w") as f:
            json.dump(trainData,f,indent=4,ensure_ascii=False)
        with open(resultPath+"Symbolic"+lang+"test.json","w") as f:
            json.dump(testData,f,indent=4,ensure_ascii=False)

if __name__ == "__main__":
    Arithmetic()
    Symbolic() 
    print("ok")

    