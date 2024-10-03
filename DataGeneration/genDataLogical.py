from dataTemplate import Q, INPUT,lange,ruleEntity,ruleAtt,ruleTypeMapTemplate,ruleTypeTemplate,CASENUM
import json
import random

resultPath="./data/"
TrainNum=500  # Number of training sets
TestNum=50 # Number of Testers
dataNum=TrainNum+TestNum
choiceMap={0:"A",1:"B",2:"C",3:"D"}
ruleEntityNum=len(ruleEntity['EN'])
ruleAttNum=len(ruleAtt['EN'])
    
RULETYPESET= ["ModusPonens", "AndIntro", "AndElim", "OrIntro", "OrElim", "ProofByContra"]


def getRandomgLogicalInput(resultInput,n=3): # Generate corresponding entities for different rules
    for i in range(n):
        nowtype=random.choice(['is','any','so','or',"not"])
        entity=random.randint(0,ruleEntityNum-1)
        attList=random.sample(range(0,ruleAttNum),2)
        if nowtype=='is':
            resultInput.append([nowtype,entity,attList[0]])
        elif nowtype=='any':
            resultInput.append([nowtype,attList[0],attList[1]])
        elif nowtype=='so':
            resultInput.append([nowtype,entity,attList[0],attList[1]])
        elif nowtype=='or':
            resultInput.append(["is",entity,["or",attList[0],attList[1]]])
        elif nowtype=='not':
            resultInput.append(["is",entity,["not",attList[0]]])
    return resultInput

def check(resultInput,resultOutput,nowtype): # Check whether the generated data meets the requirements
    if nowtype=="ModusPonens":
        ismap={}
        anymap={}
        for i in range(2,len(resultInput)):
            if resultInput[i][0]=="is" and isinstance(resultInput[i][2],int):
                ismap[resultInput[i][1]]=resultInput[i][2]
            if resultInput[i][0]=="any":
                anymap[resultInput[i][1]]=resultInput[i][2]
        for iskey in ismap.keys():
            if ismap[iskey] in anymap.keys():
                return False
    elif nowtype=="AndIntro":
        tagentity=resultInput[0][1]
        ismap=set()
        for i in range(2,len(resultInput)):
            if resultInput[i][0]=="is" and isinstance(resultInput[i][2],int):
                if resultInput[i][1]==tagentity:
                    return False
                if resultInput[i][1] in ismap:
                    return False
                ismap.add(resultInput[i][1])
    elif nowtype=="AndElim":
        pass
    elif nowtype=="OrIntro":
        pass
    elif nowtype=="OrElim":
        soMap={}
        for i in range(3,len(resultInput)):
            if resultInput[i][0]=="so":
                if resultInput[i][1] not in soMap.keys():
                    soMap[resultInput[i][1]]=[]
                soMap[resultInput[i][1]].append([resultInput[i][2],resultInput[i][3]])
        itemMap=[]
        for i in soMap.keys():
            for iitem in soMap[i]:
                for jitem in soMap[i]:
                    if iitem!=jitem and iitem[1]==jitem[1]:
                        itemMap.append([iitem[0],jitem[0]])

        for i in range(3,len(resultInput)):
            if resultInput[i][0]=="or":
                for iitem in itemMap:
                    if (resultInput[i][1]==iitem[0] and resultInput[i][2]==iitem[1])or(resultInput[i][1]==iitem[1] and resultInput[i][2]==iitem[0]):
                        return False
    elif nowtype=="ProofByContra":
        soMap={}
        isMap={}
        for i in range(2,len(resultInput)):
            if resultInput[i][0]=="so":
                if resultInput[i][1] not in soMap.keys():
                    soMap[resultInput[i][1]]=[]
                soMap[resultInput[i][1]].append(resultInput[i][3])
            if resultInput[i][0]=="is" and isinstance(resultInput[i][2],list) and resultInput[i][2][0]=="not":
                if resultInput[i][1] not in isMap.keys():
                    isMap[resultInput[i][1]]=[]
                isMap[resultInput[i][1]].append(resultInput[i][2][1])
        for i in soMap.keys():
            for j in soMap[i]:
                if i in isMap.keys() and  j in isMap[i]:
                    return False
    return True

def testUsedSet(para,usedSet=None): # Test for conflicts
    if usedSet is not None:
        if para in usedSet:
            return True
        usedSet.add(para)
    return False

attUsedSet=set()
entityUsedSet=set()
def testLogical(nowtype,usedSet=None): # Generate data
    resultinput=[]
    resultoutput=[]
    ACCENTITY=random.randint(0,ruleEntityNum-1)
    ACCATTList=random.sample(range(0,ruleAttNum),2)
    if testUsedSet((ACCENTITY,str(ACCATTList)),usedSet) and nowtype!="OrElim":
        return testLogical(nowtype,usedSet)
    if nowtype=="ModusPonens":
        resultinput.append(["is",ACCENTITY,ACCATTList[0]])
        resultinput.append(["any",ACCATTList[0],ACCATTList[1]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-2)
        resultoutput.append(["is",ACCENTITY,ACCATTList[1]])
    elif nowtype=="AndIntro":
        resultinput.append(["is",ACCENTITY,ACCATTList[0]])
        resultinput.append(["is",ACCENTITY,ACCATTList[1]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-2)
        resultoutput.append(["is",ACCENTITY,["and",ACCATTList[0],ACCATTList[1]]])
    elif nowtype=="AndElim":
        resultinput.append(["is",ACCENTITY,["and",ACCATTList[0],ACCATTList[1]]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-1)
        resultoutput.append(["is",ACCENTITY,ACCATTList[0]])
    elif nowtype=="OrIntro":
        resultinput.append(["is",ACCENTITY,ACCATTList[0]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-1)
        resultoutput.append(["is",ACCENTITY,["or",ACCATTList[0],ACCATTList[1]]])

    elif nowtype=="OrElim":
        ACCATTList=random.sample(range(0,ruleAttNum),3)
        if testUsedSet((ACCENTITY,str(ACCATTList)),usedSet):
            return testLogical(nowtype,usedSet)
        resultinput.append(["is",ACCENTITY,["or",ACCATTList[0],ACCATTList[1]]])
        resultinput.append(["so",ACCENTITY,ACCATTList[0],ACCATTList[2]])
        resultinput.append(["so",ACCENTITY,ACCATTList[1],ACCATTList[2]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-3)
        resultoutput.append(["is",ACCENTITY,ACCATTList[2]])

    elif nowtype=="ProofByContra":
        resultinput.append(["so",ACCENTITY,ACCATTList[0],ACCATTList[1]])
        resultinput.append(["is",ACCENTITY,["not",ACCATTList[1]]])
        resultinput=getRandomgLogicalInput(resultinput,n=CASENUM-2)
        resultoutput.append(["is",ACCENTITY,["not",ACCATTList[0]]])

    if not check(resultinput,resultoutput,nowtype):
        return testLogical(nowtype,usedSet)
    attUsedSet.update(ACCATTList)
    entityUsedSet.add(ACCENTITY)
    random.shuffle(resultinput)
    return resultinput,resultoutput,nowtype

def getOtherChoiceLogical(nowtype,para): # Generating Interference Options
    result=[]
    while True:
        if  random.random()>0.5:
            input1,output1,_=testLogical(nowtype)
        else:
            tempENTITY=random.randint(0,ruleEntityNum-1)
            tempAttList=random.sample(range(0,ruleAttNum),2)
            if random.random()>0.3:
                tempENTITY=random.choice(list(entityUsedSet))
            if random.random()>0.3:
                tempAttList[0]=random.choice(list(attUsedSet))
            if random.random()>0.3:
                tempAttList[1]=random.choice(list(attUsedSet))
                while tempAttList[1]==tempAttList[0]:
                    tempAttList[1]=random.randint(0,ruleAttNum-1)
            if nowtype=="AndIntro":
                output1=["is",tempENTITY,["and",tempAttList[0],tempAttList[1]]]
            elif nowtype=="OrIntro":
                isMap={}
                for i in para[1]: # para[2]
                    if i[0]=="is" and isinstance(i[2],str):
                        if i[1] not in isMap.keys():
                            isMap[i[1]]=[]
                        isMap[i[1]].append(i[2])
                if tempENTITY in isMap.keys() and (tempAttList[0] in isMap[tempENTITY] or tempAttList[1]in isMap[tempENTITY]):
                    continue
                output1=["is",tempENTITY,["or",tempAttList[0],tempAttList[1]]]
            elif nowtype=="ProofByContra":
                output1=["is",tempENTITY,["not",tempAttList[0]]]
            else:
                output1=["is",tempENTITY,tempAttList[0]]
            output1=[output1]
        if str(output1)==str(para[0]):
            continue
        result.append(output1)
        if len(result)==3:
            result.append(para[0])
            random.shuffle(result)
            return result,choiceMap[result.index(para[0])]



def decodeitem(item,lang,entityFlag=False): # Decoding the generated data
    if isinstance(item,str) or isinstance(item,int):
        if entityFlag:
            return ruleEntity[lang][int(item)]
        return ruleAtt[lang][int(item)]
    if item[0]=='not':
        para1=decodeitem(item[1],lang,entityFlag)
        return ruleTypeMapTemplate[item[0]+lang].format(para1)
    elif item[0]=='or' or item[0]=='and':
        para1=decodeitem(item[1],lang,entityFlag)
        para2=decodeitem(item[2],lang,entityFlag)
        return ruleTypeMapTemplate[item[0]+lang].format(para1,para2)

def changeDataToLangLogical(data,lang): # into the output of the corresponding language
    
    if isinstance(data[0][0],list):
        result=[]
        for loc,item in enumerate(data):
            result.append(changeDataToLangLogical(data[loc],lang))
        return result
    if data[0] in RULETYPESET:
        result=[]
        for item in data:
            result.append(ruleTypeTemplate[item+lang])
        return result
    resultStrList=[]
    for item in data:
        if item[0]=="is":
            para1=decodeitem(item[1],lang,True)
            para2=decodeitem(item[2],lang)
            resultStrList.append(ruleTypeMapTemplate["is"+lang].format(para1,para2))
        elif item[0]=="any":
            para1=decodeitem(item[1],lang)
            para2=decodeitem(item[2],lang)
            resultStrList.append(ruleTypeMapTemplate["any"+lang].format(para1,para2))
        elif item[0]=="so":
            para1=decodeitem(item[1],lang,True)
            para2=decodeitem(item[2],lang)
            para3=decodeitem(item[3],lang)
            resultStrList.append(ruleTypeMapTemplate["so"+lang].format(para1,para2,para3))
    resultstr=""
    for item in resultStrList:
        resultstr+=item
    if lang =="ZH" and "是不是" in resultstr:
        resultstr=resultstr.replace("是不是","不是")
    return resultstr

def Logical():
    result={}
    for lang in lange:
        result[lang]=[]
    for i in RULETYPESET:
        usedSet=set()
        for j in range(dataNum):
            input,output,Logical=testLogical(i,usedSet)
            outputSet,choice=getOtherChoiceLogical(i,[output,input])
            for lang in lange:
                inputlang=changeDataToLangLogical(input,lang)
                outputSetlang=changeDataToLangLogical(outputSet,lang)
                result[lang].append({"prompt":Q["Arithmetic"+lang],"query":INPUT["Arithmetic"+lang].format(ruleTypeTemplate[i+lang],inputlang,outputSetlang[0],outputSetlang[1],outputSetlang[2],outputSetlang[3]),"response":choice})  
            global attUsedSet
            global entityUsedSet
            attUsedSet.clear()
            entityUsedSet.clear()

    for lang in lange:
        trainData,testData=SplitTrainAndTest(result[lang])
        with open(resultPath+"Logical"+lang+"train.json","w") as f:
            json.dump(trainData,f,indent=4,ensure_ascii=False)
        with open(resultPath+"Logical"+lang+"test.json","w") as f:
            json.dump(testData,f,indent=4,ensure_ascii=False)

def SplitTrainAndTest(data,TrainNum=500,TestNum=50): 
    dataNum=TrainNum+TestNum
    train=[]
    test=[]
    for i in range(len(data)//dataNum):
        train.extend(data[i*dataNum:i*dataNum+TrainNum])
        test.extend(data[i*dataNum+TrainNum:i*dataNum+dataNum])
    return train,test

if __name__ == "__main__":
    Logical()
    print("ok")

    